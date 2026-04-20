#CSE 5311 - Programming Project : 1. Sorting Algorithms
Arham Shams Sameer - 1002078834

Requirements:
    Python 3.12+
    matplotlib (pip install matplotlib)

Setup:
    python -m venv venv
    venv\Scripts\activate
    pip install matplotlib

Run:
    python src\sorting_algorithms.py      (self-test)
    python src\input_generator.py         (generates 24 input files in inputs/)
    python src\benchmark.py               (runs benchmarks, outputs CSV + charts to results/)
    python src\gui.py                     (launches GUI - bonus)

    Or just run: run.bat

Files:
    src\sorting_algorithms.py   - 7 sorting algorithm implementations
    src\input_generator.py      - input file generator (random, sorted, reverse, nearly-sorted)
    src\benchmark.py            - benchmark driver, CSV + chart generation
    src\gui.py                  - Tkinter GUI for interactive benchmarking (bonus)
    inputs\                     - generated input files (24 total)
    results\                    - benchmark_results.csv + 10 PNG charts
    run.bat                     - runs everything in order
