#  algorithms.py  –  Divide and Conquer: Merge Sort + Binary Search


import time

#  MERGE SORT  (sorts by transaction_id, ascending)
def merge_sort(arr: list, show_steps: bool = False, depth: int = 0) -> list:
    """
    Merge Sort
    DIVIDE  : Split the array into two equal halves
    CONQUER : Recursively sort each half
    COMBINE : Merge the two sorted halves into one


    Parameters
    ----------
    arr        : List of Transaction objects to sort
    show_steps : If True, prints each recursive call
    depth      : Current recursion depth (used for indented trace output).

    Returns
    -------
    A new sorted list (original list is not mutated)

    Time Complexity  : O(n log n)  – all cases
    Space Complexity : O(n)        – auxiliary space for merging
    """

    # BASE CASE - A list with 0 or 1 element is already sorted.
    # This is where the recursion stop calling itself (CONQUER step ends).
    if len(arr) <= 1:
        return arr

    indent = "  " * depth

    if show_steps:
        ids = [t.transaction_id for t in arr]
        print(f"{indent}merge_sort called → {ids}")

    # DIVIDE - Find the midpoint and split the array into two halves.
    mid   = len(arr) // 2
    left  = arr[:mid]
    right = arr[mid:]

    if show_steps:
        print(f"{indent}  DIVIDE  → left={[t.transaction_id for t in left]}  "
              f"right={[t.transaction_id for t in right]}")

    # CONQUER - Recursively sort each half.
    left  = merge_sort(left,  show_steps, depth + 1)
    right = merge_sort(right, show_steps, depth + 1)

    # COMBINE - Merge the two sorted halves into a single sorted list.
    merged = _merge(left, right)

    if show_steps:
        print(f"{indent}  COMBINE → {[t.transaction_id for t in merged]}")

    return merged


def _merge(left: list, right: list) -> list:
    """
    Helper – Merge two sorted lists into one sorted list.

    Compares elements from left and right one by one,
    always picking the smaller transaction_id first.
    Remaining elements from whichever list is not exhausted
    are appended directly (they are already sorted).
    """
    result = []
    i = j = 0

    # Merge by selecting the smaller transaction_id.
    while i < len(left) and j < len(right):
        if left[i].transaction_id <= right[j].transaction_id:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements (already sorted)
    result.extend(left[i:])
    result.extend(right[j:])

    return result



#  BINARY SEARCH  (searches by transaction_id)
def binary_search(arr: list, target_id: int,
                  show_steps: bool = False) -> tuple[int, int]:
    """
    Binary Search.

    DIVIDE  : Split the search range into left and right half.
    CONQUER : Recursively search only the relevant half.
    COMBINE : Return the found index (or -1 if not found).

    The input array MUST be sorted by transaction_id before calling this function

    Parameters
    ----------
    arr        : Sorted list of Transaction objects.
    target_id  : The transaction_id to search for.
    show_steps : If True, prints each probe step.

    Returns
    -------
    (index, comparisons)
      index       : Position of the found element, or -1 if not found.
      comparisons : Number of comparisons made during the search.

    Time Complexity : O(log n)  – average and worst case
                      O(1)      – best case (mid is the target)
    Space Complexity: O(log n)  – recursive call stack
    """
    comparisons = [0]   # mutable container so inner function can update it

    def _search(low: int, high: int) -> int:
        """Recursive helper that narrows the search range."""

        # BASE CASE (CONQUER) - Search range is empty
        if low > high:
            return -1

        #  DIVIDE - check the middle element
        mid = (low + high) // 2
        comparisons[0] += 1

        if show_steps:
            print(f"    Probe: low={low}, mid={mid}, high={high}  "
                  f"→ checking TXN{arr[mid].transaction_id:04d}")

        # CONQUER
        if arr[mid].transaction_id == target_id:
            return mid
        elif arr[mid].transaction_id < target_id:
            #search the righ half
            return _search(mid + 1, high)
        else:
            # search the left half
            return _search(low, mid - 1)

    index = _search(0, len(arr) - 1)
    return index, comparisons[0]


#  LINEAR SEARCH  (for comparison)
def linear_search(arr: list, target_id: int) -> tuple[int, int]:
    """
    Sequential (linear) search through an unsorted or sorted list.

    Scans every element from index 0 until the target is found
    or the end of the list is reached.

    Time Complexity : O(n)  – average and worst case
                      O(1)  – best case (first element)

    Returns
    -------
    (index, comparisons)
    """
    for i, txn in enumerate(arr):
        if txn.transaction_id == target_id:
            return i, i + 1
    return -1, len(arr)


#  PERFORMANCE TIMING UTILITY
def time_operation(fn, *args, repetitions: int = 1000) -> float:
    """
    Run fn(*args) `repetitions` times and return the average
    execution time in microseconds (µs).
    """
    start = time.perf_counter()
    for _ in range(repetitions):
        fn(*args)
    end = time.perf_counter()
    return ((end - start) / repetitions) * 1_000_000
