"""
04/03/2026 - V1
------------------
Arham Shams Sameer
1002078834
------------------
input_generator.py
------------------------------------------------------------------------
generates test input arrays of various sizes and distributions and saves
them to plain text files in the ../inputs/ directory, creating a full
set of inputs used by the benchmark driver.

one integer per line. it is readable by load_input() below.
"""

import os
import random

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "inputs")

def generate_random(size, seed=42, lo=0, hi=1_000_000):
    #random.seed(seed)
    #return random.sample(range(lo, hi), size)
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(size)]

def generate_sorted(size):
    return list(range(size))

def generate_reverse_sorted(size):
    return list(range(size - 1, -1, -1))

def generate_nearly_sorted(size, swaps=None, seed=42):
    rng = random.Random(seed)
    a = list(range(size))
    if swaps is None:
        swaps = max(1, size // 20)            #~5% of the elements
    for _ in range(swaps):
        i = rng.randint(0, size - 2)
        a[i], a[i + 1] = a[i + 1], a[i]
    return a

#import json
#def save_input(data, filename):
#    path = os.path.join(INPUT_DIR, filename)
#    with open(path, "w") as f:
#        json.dump(data, f)

def save_input(data, filename):
    os.makedirs(INPUT_DIR, exist_ok=True)
    path = os.path.join(INPUT_DIR, filename)
    with open(path, "w") as f:
        for x in data:
            f.write(f"{x}\n")
    return path

def load_input(filename):
    path = os.path.join(INPUT_DIR, filename)
    with open(path, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]

def generate_all_benchmark_inputs():
    #sizes that stress-test O(n^2) vs O(n log n) differences
    sizes = [100, 500, 1000, 2000, 5000, 10000]

    for n in sizes:
        save_input(generate_random(n, seed=42),    f"random_{n}.txt")
        save_input(generate_sorted(n),             f"sorted_{n}.txt")
        save_input(generate_reverse_sorted(n),     f"reverse_{n}.txt")
        save_input(generate_nearly_sorted(n),      f"nearly_{n}.txt")

    print(f"Generated {len(sizes) * 4} input files in {INPUT_DIR}")
    print(f"Sizes: {sizes}")
    print("Distributions: random, sorted, reverse, nearly-sorted")

if __name__ == "__main__":
    generate_all_benchmark_inputs()
