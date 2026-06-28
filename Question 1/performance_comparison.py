# performance_comparison.py - Hash Table (Linear Probing)  vs  1-D Array  –  Search Speed


import time
from medicine import Medicine
from hash_table import HashTable

#  Shared sample data  (identical in both structures)

SAMPLE_MEDICINES = [
    Medicine("MED001", "Paracetamol 500mg",       "Tablet",     2.50,  120, "12/2026"),
    Medicine("MED002", "Ibuprofen 400mg",          "Tablet",     4.80,   85, "06/2026"),
    Medicine("MED003", "Amoxicillin 250mg",        "Tablet",     9.90,   60, "03/2027"),
    Medicine("MED004", "Piriton Syrup",            "Syrup",      6.50,   40, "09/2026"),
    Medicine("MED005", "Cough Relief Syrup",       "Syrup",      8.20,   35, "11/2026"),
    Medicine("MED006", "Vitamin C 1000mg",         "Supplement", 15.90,  75, "01/2028"),
    Medicine("MED007", "Omega-3 Fish Oil Softgel", "Supplement", 22.50,  50, "08/2027"),
]

# Mix of existing and non-existing keys
SEARCH_KEYS = [
    ("MED001", True),
    ("MED004", True),
    ("MED007", True),
    ("MED099", False),
    ("MED000", False),
    ("MEDXYZ", False),
]

REPETITIONS = 1_000

#  Structure builders

def build_hash_table() -> HashTable:
    ht = HashTable()
    for med in SAMPLE_MEDICINES:
        ht.insert(med)
    return ht


def build_array() -> list:
    return list(SAMPLE_MEDICINES)


#  Search implementations
def array_search(arr: list, key: str):
    """
    Linear search through a 1-D array.
    Scans every element from index 0 until match or end.
    Time complexity: O(n) average and worst case.
    """
    key = key.upper().strip()
    for med in arr:
        if med.medicine_id == key:
            return med
    return None


# timing utility
def time_search(fn, *args) -> float:
    """Run fn(*args) REPETITIONS times; return average time in µs."""
    start = time.perf_counter()
    for _ in range(REPETITIONS):
        fn(*args)
    end = time.perf_counter()
    return ((end - start) / REPETITIONS) * 1_000_000


# Direct comparison on pharmacy data (n = 7)
DIVIDER     = "=" * 78
SUB_DIVIDER = "-" * 78


def run_comparison(ht: HashTable, arr: list) -> list:
    results = []
    for key, exists in SEARCH_KEYS:
        ht_time  = time_search(ht.search, key)
        arr_time = time_search(array_search, arr, key)
        if ht_time < arr_time:
            winner = "Hash Table"
            speedup = arr_time / ht_time
        else:
            winner = "Array"
            speedup = ht_time / arr_time
        results.append({
            "key": key, "exists": exists,
            "ht_time": ht_time, "arr_time": arr_time, "winner": winner, "speedup": speedup,
        })
    return results


def print_results(results: list) -> None:
    print(f"\n{DIVIDER}")
    print("  DIRECT COMPARISON: Hash Table (Linear Probing) vs 1-D Array")
    print(f"  Pharmacy dataset: n = 7 records  |  {REPETITIONS:,} repetitions per key")
    print(DIVIDER)
    print(f"  {'Key':<10} {'Status':<12} {'Hash Table (µs)':>18} {'Array (µs)':>12} {'Winner':>12} {'Speedup':>10}")
    print(f"  {SUB_DIVIDER}")

    ht_total = arr_total = 0.0
    for r in results:
        status  = "EXISTS" if r["exists"] else "NOT FOUND"
        speedup = f"{r['speedup']:.2f}x"

        print(
            f"  {r['key']:<10} {status:<12}"
            f"{r['ht_time']:>18.4f} {r['arr_time']:>12.4f}"
            f" {r['winner']:>12} {speedup:>10}"
        )
        ht_total  += r["ht_time"]
        arr_total += r["arr_time"]

    n = len(results)
    avg_ht = ht_total / n
    avg_arr = arr_total / n
    if avg_ht < avg_arr:
        avg_winner = "Hash Table"
        avg_speedup = avg_arr / avg_ht
    else:
        avg_winner = "Array"
        avg_speedup = avg_ht / avg_arr
    print(f"  {SUB_DIVIDER}")
    print(
        f"  {'AVERAGE':<10} {'':<12}"
        f"{avg_ht:>18.4f} {avg_arr:>12.4f}"
        f" {avg_winner:>12} {avg_speedup:>10.2f}x")
    print(DIVIDER)

#  Entry point
def main() -> None:
    print(DIVIDER)
    print("  Pharmacy Inventory – Performance Comparison")
    print(f"  Running {REPETITIONS:,} searches per key on n=7 pharmacy records...")
    print(DIVIDER)

    ht  = build_hash_table()
    arr = build_array()
    results = run_comparison(ht, arr)
    print_results(results)

if __name__ == "__main__":
    main()
