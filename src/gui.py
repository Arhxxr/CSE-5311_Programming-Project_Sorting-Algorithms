"""
04/11/2026 - V1
04/15/2026 - V2
04/16/2026 - V2.5
04/17/2026 - V3
------------------
Arham Shams Sameer
1002078834
------
gui.py
----------------------------------------------------------------------------------------------------------
Tkinter GUI for the sorting-algorithms project (for bonus deliverable).

Features:
  . Select one algorithm and measure its running time on a chosen input size.
  . Compare TWO OR MORE algorithms side-by-side (tick the boxes).
  . Choose the input distribution: random, sorted, reverse, nearly-sorted.
  . See the results as both a table and a bar chart.
  . Planned implementation of animated sorting algorithms but couldn't implement it in time.

requires matplotlib (for the embedded chart)
| > python gui.py
"""

import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sorting_algorithms import ALGORITHMS
from input_generator import (
    generate_random, generate_sorted,
    generate_reverse_sorted, generate_nearly_sorted,
)

DISTRIBUTIONS = {
    "random":   generate_random,
    "sorted":   generate_sorted,
    "reverse":  generate_reverse_sorted,
    "nearly":   generate_nearly_sorted,
}


class SortingBenchmarkGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sorting Algorithm Benchmark")
        self.geometry("1000x700")
        self.minsize(900, 600)

        #state
        self.algo_vars = {name: tk.BooleanVar(value=False) for name in ALGORITHMS}
        self.size_var = tk.StringVar(value="2000")
        self.dist_var = tk.StringVar(value="random")

        self._build_ui()

    #UI layout
    def _build_ui(self):
        #top frame: controls
        controls = ttk.LabelFrame(self, text="Configuration", padding=10)
        controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        #algorithm checkboxes
        #radio buttons first can only select one at a time
        #switched to checkboxes
        # algo_frame = ttk.LabelFrame(controls, text="Pick algorithm", padding=5)
        # self.algo_var = tk.StringVar(value="Bubble Sort")
        # for i, name in enumerate(ALGORITHMS):
        #     rb = ttk.Radiobutton(algo_frame, text=name, variable=self.algo_var, value=name)
        #     rb.grid(row=i, column=0, sticky="w")

        algo_frame = ttk.LabelFrame(controls, text="Algorithms (select 1 or more)", padding=5)
        algo_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 10))
        for i, name in enumerate(ALGORITHMS):
            cb = ttk.Checkbutton(algo_frame, text=name, variable=self.algo_vars[name])
            cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        #size entry
        ttk.Label(controls, text="Input size (n):").grid(row=0, column=1, sticky="e", padx=5)
        size_entry = ttk.Entry(controls, textvariable=self.size_var, width=10)
        size_entry.grid(row=0, column=2, sticky="w", padx=5)
        ttk.Label(controls, text="(100 – 50000)", foreground="gray").grid(
            row=0, column=3, sticky="w"
        )

        #distribution dropdown
        ttk.Label(controls, text="Distribution:").grid(row=1, column=1, sticky="e", padx=5)
        dist_combo = ttk.Combobox(
            controls, textvariable=self.dist_var,
            values=list(DISTRIBUTIONS.keys()), state="readonly", width=12,
        )
        dist_combo.grid(row=1, column=2, sticky="w", padx=5)

        #buttons
        btn_frame = ttk.Frame(controls)
        btn_frame.grid(row=2, column=1, columnspan=3, sticky="w", pady=(10, 0))
        self.run_btn = ttk.Button(btn_frame, text="Run Benchmark", command=self._run_clicked)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Select All", command=self._select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear",      command=self._clear_all).pack(side=tk.LEFT, padx=5)

        #status bar
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN,
                  anchor="w").pack(side=tk.BOTTOM, fill=tk.X)

        #results: table + chart
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        #tried a Listbox for results but Treeview has columns :<
        #self.results_list = tk.Listbox(table_frame, width=40, height=12)
        #self.results_list.pack(fill=tk.BOTH, expand=True)

        #results table
        table_frame = ttk.LabelFrame(paned, text="Results", padding=5)
        paned.add(table_frame, weight=1)
        self.tree = ttk.Treeview(
            table_frame,
            columns=("algo", "time_s", "time_ms"),
            show="headings", height=12,
        )
        self.tree.heading("algo",    text="Algorithm")
        self.tree.heading("time_s",  text="Time (s)")
        self.tree.heading("time_ms", text="Time (ms)")
        self.tree.column("algo",    width=200, anchor="w")
        self.tree.column("time_s",  width=100, anchor="e")
        self.tree.column("time_ms", width=100, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True)

        #embedded matplotlib chart
        chart_frame = ttk.LabelFrame(paned, text="Comparison chart", padding=5)
        paned.add(chart_frame, weight=2)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Run Benchmark to see results")
        self.ax.set_ylabel("Time (seconds)")
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #button handlers
    def _select_all(self):
        for v in self.algo_vars.values():
            v.set(True)

    def _clear_all(self):
        for v in self.algo_vars.values():
            v.set(False)

    def _run_clicked(self):
        #validate algorithm selection
        selected = [n for n, v in self.algo_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning("No algorithm",
                                   "Please select at least one algorithm.")
            return

        #validate size
        try:
            size = int(self.size_var.get())
            if size < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid size",
                                 "Input size must be a positive integer.")
            return

        if size > 50000 and any(a in {"Bubble Sort", "Selection Sort", "Insertion Sort"}
                                for a in selected):
            if not messagebox.askyesno(
                "Large input warning",
                f"You selected one or more O(n^2) algorithms with n={size}.\n"
                "This may take a long time. Continue?"):
                return

        dist = self.dist_var.get()

        #the whole window would freeze until it finished
        # for name in selected:
        #     fn = ALGORITHMS[name]
        #     start = time.perf_counter()
        #     fn(data)
        #     elapsed = time.perf_counter() - start
        #     self._append_row(name, elapsed)

        self.run_btn.config(state=tk.DISABLED)
        self.status_var.set(f"Running {len(selected)} algorithm(s) on "
                            f"{dist} input of size {size}...")
        self.tree.delete(*self.tree.get_children())

        thread = threading.Thread(
            target=self._run_benchmark_thread,
            args=(selected, size, dist),
            daemon=True,
        )
        thread.start()

    #worker thread
    def _run_benchmark_thread(self, selected, size, dist):
        try:
            #generate one input array and use it for every algorithm
            data = DISTRIBUTIONS[dist](size) if dist != "nearly" \
                else generate_nearly_sorted(size)

            results = []
            for name in selected:
                fn = ALGORITHMS[name]
                start = time.perf_counter()
                out = fn(data)
                elapsed = time.perf_counter() - start
                ok = (out == sorted(data))
                results.append((name, elapsed, ok))
                #push partial results to the UI as we go
                self.after(0, self._append_row, name, elapsed)

            self.after(0, self._finish_run, results, dist, size)
        except Exception as exc:
            self.after(0, self._report_error, exc)

    #main-thread UI updates (called via self.after)
    def _append_row(self, name, elapsed):
        self.tree.insert("", tk.END, values=(
            name, f"{elapsed:.4f}", f"{elapsed * 1000:.2f}"
        ))

    def _finish_run(self, results, dist, size):
        #redraw chart
        self.ax.clear()
        names   = [r[0] for r in results]
        times   = [r[1] for r in results]
        bars = self.ax.bar(range(len(names)), times, color="steelblue")
        self.ax.set_xticks(range(len(names)))
        self.ax.set_xticklabels(names, rotation=25, ha="right", fontsize=8)
        self.ax.set_ylabel("Time (seconds)")
        self.ax.set_title(f"n = {size}, distribution = {dist}")
        #label each bar with its time
        for bar, t in zip(bars, times):
            self.ax.annotate(
                f"{t*1000:.1f} ms" if t < 1 else f"{t:.2f} s",
                xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 3), textcoords="offset points",
                ha="center", fontsize=8,
            )
        self.fig.tight_layout()
        self.canvas.draw()

        #declare winner
        results_sorted = sorted(results, key=lambda r: r[1])
        winner_name, winner_time, _ = results_sorted[0]
        all_correct = all(r[2] for r in results)
        status = f"Done. Fastest: {winner_name} ({winner_time*1000:.2f} ms)."
        if not all_correct:
            status = "WARNING: at least one algorithm produced incorrect output! " + status
        self.status_var.set(status)
        self.run_btn.config(state=tk.NORMAL)

    def _report_error(self, exc):
        messagebox.showerror("Error", str(exc))
        self.status_var.set(f"Error: {exc}")
        self.run_btn.config(state=tk.NORMAL)

#animation
    #gave up on this, maybe come back to it later | FuncAnimation doesn't work with tkinter | threading errors and the bars wouldn't update right
    # from matplotlib.animation import FuncAnimation
    #
    # class SortingAnimator:
    #     def __init__(self, master, data, algorithm_name):
    #         self.master = master
    #         self.data = list(data)
    #         self.n = len(self.data)
    #         self.algorithm_name = algorithm_name
    #
    #         self.window = tk.Toplevel(master)
    #         self.window.title(f"Sorting Animation - {algorithm_name}")
    #         self.window.geometry("800x500")

    #         self.fig = Figure(figsize=(8, 4), dpi=100)
    #         self.ax = self.fig.add_subplot(111)
    #         self.bars = self.ax.bar(range(self.n), self.data, color="steelblue")
    #         self.ax.set_title(f"{algorithm_name} - sorting {self.n} elements")
    #         self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
    #         self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    #
    #     def _bubble_sort_generator(self):
    #         a = self.data
    #         n = len(a)
    #         for i in range(n - 1):
    #             for j in range(n - i - 1):
    #                 if a[j] > a[j + 1]:
    #                     a[j], a[j + 1] = a[j + 1], a[j]
    #                 #this is where it breaks, need to yield
    #                 #the current state but the bars dont update
    #                 yield a, j, j + 1
    #     def _update_frame(self, frame):
    #         a, idx1, idx2 = frame
    #         for i, (bar, val) in enumerate(zip(self.bars, a)):
    #             bar.set_height(val)
    #             if i == idx1 or i == idx2:
    #                 bar.set_color("red")
    #             else:
    #                 bar.set_color("steelblue")
    #     def animate(self):
    #         gen = self._bubble_sort_generator()
    #         self.anim = FuncAnimation(self.fig, self._update_frame,
    #                                   frames=gen, interval=50,
    #                                   repeat=False, blit=False)
    #         self.canvas.draw()
    #
    # def _run_animation(self, algo_name, data):
    #     animator = SortingAnimator(self, data, algo_name)
    #     animator.animate()


if __name__ == "__main__":
    app = SortingBenchmarkGUI()
    app.mainloop()
