"""
04/03/2026 - V1
04/07/2026 - V2
04/11/2026 - V3
------------------
Arham Shams Sameer
1002078834
---------------------
sorting_algorithms.py
---------------------------------------------------------------------------------------------
implementations of 6+1 sorting algorithms with no library sort calls. 
Each function returns a new sorted list so the original isn't changed.

Algorithms implemented:
    1. Bubble Sort
    2. Selection Sort
    3. Insertion Sort
    4. Merge Sort
    5. Heap Sort
    6. Quick Sort (regular)
    7. Quick Sort (median-of-3)
"""

import sys

#python's default recursion limit (1000) was too low for recursive quicksort
#on large inputs, I bumped it up so I can benchmark up to 50k elements.
#in the higher end, the runtime goes over a minute due to bubble sort
#usually taking around 90 seconds on 50k random.
sys.setrecursionlimit(200000)

#1. bubble sort
def bubble_sort(arr):
    #was way too slow on sorted input without early exit
    # a = list(arr)
    # n = len(a)
    # for i in range(n - 1):
    #     for j in range(n - i - 1):
    #         if a[j] > a[j + 1]:
    #             a[j], a[j + 1] = a[j + 1], a[j]
    # return a

    a = list(arr)
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

#2. selection sort
def selection_sort(arr):
    
    a = list(arr)
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return a

#3. insertion sort
def insertion_sort(arr):
    
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        #sliding larger elements one position to the right
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


#4. merge sort

#was creating too many copies and the indexing got confusing
# def merge_sort(arr):
#     if len(arr) <= 1:
#         return arr
#     mid = len(arr) // 2
#     left = merge_sort(arr[:mid])
#     right = merge_sort(arr[mid:])
#     merged = []
#     i = j = 0
#     while i < len(left) and j < len(right):
#         if left[i] <= right[j]:
#             merged.append(left[i])
#             i += 1
#         else:
#             merged.append(right[j])
#             j += 1
#     merged.extend(left[i:])
#     merged.extend(right[j:])
#     return merged

def merge_sort(arr):
    a = list(arr)
    _merge_sort_helper(a, 0, len(a) - 1)
    return a

def _merge_sort_helper(a, left, right):
    if left < right:
        mid = (left + right) // 2
        _merge_sort_helper(a, left, mid)
        _merge_sort_helper(a, mid + 1, right)
        _merge(a, left, mid, right)

def _merge(a, left, mid, right):
    left_half = a[left:mid + 1]
    right_half = a[mid + 1:right + 1]

    i = j = 0
    k = left
    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            a[k] = left_half[i]
            i += 1
        else:
            a[k] = right_half[j]
            j += 1
        k += 1

    #leftover elements
    while i < len(left_half):
        a[k] = left_half[i]
        i += 1
        k += 1
    while j < len(right_half):
        a[k] = right_half[j]
        j += 1
        k += 1

#5. heap sort
def heap_sort(arr):
    a = list(arr)
    n = len(a)

    #bottom-up was more efficient
    # for i in range(1, n):
    #     child = i
    #     while child > 0:
    #         parent = (child - 1) // 2
    #         if a[child] > a[parent]:
    #             a[child], a[parent] = a[parent], a[child]
    #             child = parent
    #         else:
    #             break

    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i)

    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        _heapify(a, i, 0)
    return a


def _heapify(a, heap_size, root):
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < heap_size and a[left] > a[largest]:
        largest = left
    if right < heap_size and a[right] > a[largest]:
        largest = right

    if largest != root:
        a[root], a[largest] = a[largest], a[root]
        _heapify(a, heap_size, largest)


#6a. quick sort - regular (last element as pivot)

#last element was easier to follow
# def _partition_first(a, low, high):
#     pivot = a[low]
#     i = high + 1
#     for j in range(high, low, -1):
#         if a[j] >= pivot:
#             i -= 1
#             a[i], a[j] = a[j], a[i]
#     a[i - 1], a[low] = a[low], a[i - 1]
#     return i - 1

def quick_sort(arr):
    a = list(arr)
    _quick_sort_helper(a, 0, len(a) - 1)
    return a

def _quick_sort_helper(a, low, high):
    if low < high:
        p = _partition_last(a, low, high)
        _quick_sort_helper(a, low, p - 1)
        _quick_sort_helper(a, p + 1, high)

def _partition_last(a, low, high):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


#6b. quick sort - median-of-three pivot
def quick_sort_median3(arr):

    a = list(arr)
    _quick_sort_m3_helper(a, 0, len(a) - 1)
    return a


def _quick_sort_m3_helper(a, low, high):
    if low < high:
        p = _partition_median3(a, low, high)
        _quick_sort_m3_helper(a, low, p - 1)
        _quick_sort_m3_helper(a, p + 1, high)


def _median_of_three(a, low, high):
    #returned the VALUE not the INDEX which broke everything
    # mid = (low + high) // 2
    # triple = [a[low], a[mid], a[high]]
    # triple.sort()
    # return triple[1]

    mid = (low + high) // 2
    if a[low] > a[mid]:
        a[low], a[mid] = a[mid], a[low]
    if a[low] > a[high]:
        a[low], a[high] = a[high], a[low]
    if a[mid] > a[high]:
        a[mid], a[high] = a[high], a[mid]
    return mid

def _partition_median3(a, low, high):
    median_idx = _median_of_three(a, low, high)
    a[median_idx], a[high] = a[high], a[median_idx]
    return _partition_last(a, low, high)


#registry - used by the driver and the GUI

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Heap Sort": heap_sort,
    "Quick Sort (regular)": quick_sort,
    "Quick Sort (median-3)": quick_sort_median3,
}


#self-test - running `python sorting_algorithms.py` to verify correctness

if __name__ == "__main__":
    import random
    random.seed(42)

    test_cases = [
        [],
        [1],
        [2, 1],
        [5, 2, 8, 1, 9, 3, 7, 4, 6],
        list(range(20)),                   #already sorted
        list(range(20, 0, -1)),            #reverse sorted
        [random.randint(0, 1000) for _ in range(100)],
        [7] * 50,                          #all duplicates
    ]

    for name, func in ALGORITHMS.items():
        print(f"Testing {name}...", end=" ")
        for case in test_cases:
            result = func(case)
            assert result == sorted(case), f"FAILED on {case[:10]}..."
        print("OK")
    print("\nAll algorithms passed all tests.")
