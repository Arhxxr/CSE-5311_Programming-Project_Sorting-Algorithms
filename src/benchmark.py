"""
04/03/2026 - V1
04/17/2026 - V2
------------------
Arham Shams Sameer
1002078834
------------
benchmark.py
-------------------------------------------------------------------
runs every sorting algorithm on every input file, records
the running time, writes a CSV of the raw results, and produces
PNG charts that visualize how each algorithm scales with input size
and how the algorithms compare to each other.
-------------------------------------------------------------------
The charts and CSV are the experimental results section required in
the project report.
"""

import csv
import os
import time

import matplotlib
matplotlib.use("Agg") #write PNGs directly
import matplotlib.pyplot as plt

from sorting_algorithms import ALGORITHMS
from input_generator import load_input, generate_all_benchmark_inputs, INPUT_DIR

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

SIZES = [100, 500, 1000, 2000, 5000, 10000]
DISTRIBUTIONS = ["random", "sorted", "reverse", "nearly"]

def time_algorithm(sort_fn, data):
    #time.time() wasn't precise enough for the fast algorithms
    #showing up as 0.0 seconds
    # start = time.time()
    # result = sort_fn(data)
    # elapsed = time.time() - start

    start = time.perf_counter()
    result = sort_fn(data)
    elapsed = time.perf_counter() - start
    #correctness check - failing if anything has wrong result
    assert result == sorted(data), "SORT PRODUCED WRONG OUTPUT"
    return elapsed

def run_benchmarks():
    #storing results as a flat list of tuples was annoying to look up
    #later for the charts
    # results = []
    # for dist in DISTRIBUTIONS:
    #     for size in SIZES:
    #         for name, func in ALGORITHMS.items():
    #             elapsed = time_algorithm(func, load_input(f"{dist}_{size}.txt"))
    #             results.append((dist, name, size, elapsed))

    #nested dict is easier to query
    results = {dist: {name: {} for name in ALGORITHMS} for dist in DISTRIBUTIONS}

    total_runs = len(DISTRIBUTIONS) * len(ALGORITHMS) * len(SIZES)
    run_num = 0

    for dist in DISTRIBUTIONS:
        for size in SIZES:
            filename = f"{dist}_{size}.txt"
            data = load_input(filename)
            for name, func in ALGORITHMS.items():
                run_num += 1
                #sorted/nearly-sorted input is pathological for regular
                #quicksort - still runs, just slowly
                elapsed = time_algorithm(func, data)
                results[dist][name][size] = elapsed
                print(f"[{run_num:3d}/{total_runs}] "
                      f"{dist:8s} n={size:5d} {name:22s} {elapsed:8.4f}s")
    return results

def save_results_csv(results):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["distribution", "algorithm", "size", "seconds"])
        for dist in DISTRIBUTIONS:
            for algo in ALGORITHMS:
                for size in SIZES:
                    secs = results[dist][algo].get(size, "")
                    writer.writerow([dist, algo, size, f"{secs:.6f}" if secs != "" else ""])
    print(f"Wrote {path}")

def plot_distribution(results, dist, use_log=False):
    #bar charts looked messy with 7 algorithms
    #line charts show the scaling better
    # fig, ax = plt.subplots(figsize=(10, 6))
    # x = range(len(SIZES))
    # width = 0.12
    # for i, name in enumerate(ALGORITHMS):
    #     ys = [results[dist][name][s] for s in SIZES]
    #     ax.bar([xi + i*width for xi in x], ys, width, label=name)

    plt.figure(figsize=(10, 6))
    for name in ALGORITHMS:
        xs = SIZES
        ys = [results[dist][name][s] for s in SIZES]
        plt.plot(xs, ys, marker="o", label=name, linewidth=2)

    plt.xlabel("Input size (n)")
    plt.ylabel("Running time (seconds)")
    title = f"Sorting algorithms on {dist} input"
    if use_log:
        plt.yscale("log")
        title += " (log scale)"
    plt.title(title)
    plt.legend(loc="best", fontsize=9)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()

    suffix = "_log" if use_log else ""
    out_path = os.path.join(RESULTS_DIR, f"chart_{dist}{suffix}.png")
    plt.savefig(out_path, dpi=120)
    plt.close()
    print(f"Wrote {out_path}")

def plot_fast_algorithms_only(results):
    #just the O(n log n) ones
    fast = ["Merge Sort", "Heap Sort",
            "Quick Sort (regular)", "Quick Sort (median-3)"]
    plt.figure(figsize=(10, 6))
    for name in fast:
        ys = [results["random"][name][s] for s in SIZES]
        plt.plot(SIZES, ys, marker="o", label=name, linewidth=2)
    plt.xlabel("Input size (n)")
    plt.ylabel("Running time (seconds)")
    plt.title("O(n log n) algorithms on random input")
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, "chart_fast_only.png")
    plt.savefig(out_path, dpi=120)
    plt.close()
    print(f"Wrote {out_path}")

def plot_quicksort_comparison(results):
    plt.figure(figsize=(10, 6))
    for dist in ["random", "sorted", "reverse"]:
        ys_reg = [results[dist]["Quick Sort (regular)"][s] for s in SIZES]
        ys_m3  = [results[dist]["Quick Sort (median-3)"][s] for s in SIZES]
        plt.plot(SIZES, ys_reg, marker="o", linestyle="--",
                 label=f"Regular ({dist})")
        plt.plot(SIZES, ys_m3, marker="s",
                 label=f"Median-3 ({dist})")
    plt.xlabel("Input size (n)")
    plt.ylabel("Running time (seconds)")
    plt.title("Regular quicksort vs median-of-3 quicksort")
    plt.yscale("log")
    plt.legend(loc="best", fontsize=9)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, "chart_quicksort_comparison.png")
    plt.savefig(out_path, dpi=120)
    plt.close()
    print(f"Wrote {out_path}")

def main():
    #making sure inputs exist
    if not os.path.isdir(INPUT_DIR) or not os.listdir(INPUT_DIR):
        print("Generating inputs...")
        generate_all_benchmark_inputs()

    print("\n=== Running benchmarks ===\n")
    results = run_benchmarks()

    print("\n=== Saving results ===\n")
    save_results_csv(results)

    print("\n=== Generating charts ===\n")
    for dist in DISTRIBUTIONS:
        plot_distribution(results, dist, use_log=False)
        plot_distribution(results, dist, use_log=True)
    plot_fast_algorithms_only(results)
    plot_quicksort_comparison(results)

    print("\nDone. See ../results/ for CSV and PNG charts.")


if __name__ == "__main__":
    main()
