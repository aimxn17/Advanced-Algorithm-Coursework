#main.py- Customer Transaction System

from transaction import Transaction
from algorithms  import (merge_sort, binary_search,
                          linear_search, time_operation)
from dataset     import get_dataset


#  Display helpers
DIVIDER     = "=" * 78
SUB_DIVIDER = "-" * 78

def _header(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)

def _row_header() -> None:
    print(f"  {'#':<4} {'TXN ID':<10} {'Customer':<22} "
          f"{'Product':<27} {'Amount (RM)':>11}  {'Date'}")
    print("  " + SUB_DIVIDER)

def _row(idx: int, txn: Transaction) -> None:
    print(f"  {idx:<4} TXN{txn.transaction_id:04d}   {txn.customer_name:<22} "
          f"{txn.product_name:<27} {txn.amount:>11.2f}  {txn.transaction_date}")

def _display_list(transactions: list) -> None:
    _row_header()
    for i, txn in enumerate(transactions, 1):
        _row(i, txn)
    print(f"\n  Total records: {len(transactions)}")

def _pause() -> None:
    input("\n  Press Enter to return to the menu...")


#  State
class SystemState:
    """Holds the live transaction list and tracks sort status."""
    def __init__(self):
        self.transactions: list = get_dataset()
        self.is_sorted: bool    = False
        self.next_id: int       = 1090   # for dynamic inserts

state = SystemState()


#  Menu actions
def display_all() -> None:
    """Feature (a): Display all transactions in current order."""
    _header("ALL TRANSACTIONS")
    status = "SORTED by Transaction ID" if state.is_sorted else "UNSORTED"
    print(f"  Current order: {status}\n")
    _display_list(state.transactions)
    _pause()


def sort_merge_sort() -> None:
    """Feature (b): Sort transactions using Merge Sort."""
    _header("MERGE SORT  (Divide and Conquer)")

    print("  ── Before Sorting ──")
    _display_list(state.transactions)

    show = input("\n  Show recursive call steps? (y/n): ").strip().lower() == 'y'

    print(f"\n  ── Applying Merge Sort {'(with trace)' if show else ''} ──\n")
    import time
    t0 = time.perf_counter()
    sorted_list = merge_sort(state.transactions, show_steps=show)
    elapsed = (time.perf_counter() - t0) * 1_000_000

    state.transactions = sorted_list
    state.is_sorted    = True

    print(f"\n  ── After Sorting ──")
    _display_list(state.transactions)
    print(f"\n  Merge Sort completed in {elapsed:.2f} µs")
    _pause()


def search_binary() -> None:
    """Feature (c): Search using Binary Search (requires sorted data)."""
    _header("BINARY SEARCH  (Divide and Conquer)")

    if not state.is_sorted:
        print("    Data is NOT sorted. Binary Search requires sorted data.")
        print("     Please run Merge Sort first (Option 2).")
        _pause()
        return

    raw = input("  Enter Transaction ID to search (numeric only, e.g. 1047): ").strip()
    if not raw.isdigit():
        print("  X Invalid input. Please enter a numeric ID.")
        _pause()
        return

    target = int(raw)
    print(f"\n  Searching for TXN{target:04d}...\n")
    print(f"  {'Probe steps':}")
    print("  " + "-" * 50)

    index, comps = binary_search(state.transactions, target, show_steps=True)

    print()
    if index != -1:
        txn = state.transactions[index]
        print(f"  /  Found at index {index}  (comparisons made: {comps})\n")
        _row_header()
        _row(index + 1, txn)
    else:
        print(f"  X  TXN{target:04d} not found in the dataset.  "
              f"(comparisons made: {comps})")
    _pause()


def search_linear() -> None:
    """Feature (d): Search using Linear Search (works on unsorted data)."""
    _header("LINEAR SEARCH  (Sequential – for comparison)")

    raw = input("  Enter Transaction ID to search (numeric only, e.g. 1047): ").strip()
    if not raw.isdigit():
        print("  X  Invalid input. Please enter a numeric ID.")
        _pause()
        return

    target = int(raw)
    print(f"\n  Scanning from index 0 for TXN{target:04d}...")

    index, comps = linear_search(state.transactions, target)

    if index != -1:
        txn = state.transactions[index]
        print(f"\n  /  Found at index {index}  (comparisons made: {comps})\n")
        _row_header()
        _row(index + 1, txn)
    else:
        print(f"\n  X  TXN{target:04d} not found.  "
              f"(comparisons made: {comps} – full list scanned)")
    _pause()


def insert_transaction() -> None:
    """Advanced Feature (a): Insert a new transaction dynamically."""
    _header("INSERT NEW TRANSACTION")

    print(f"  New Transaction ID will be auto-assigned: TXN{state.next_id:04d}\n")
    print("  Fill in the details below (press Enter to cancel at any prompt).\n")

    name = input("  Customer Name  : ").strip()
    if not name: print("  Cancelled."); _pause(); return

    product = input("  Product Name   : ").strip()
    if not product: print("  Cancelled."); _pause(); return

    try:
        amount = float(input("  Amount (RM)    : ").strip())
        if amount < 0: raise ValueError()
    except ValueError:
        print("  X  Invalid amount."); _pause(); return

    date = input("  Date (DD/MM/YYYY): ").strip()
    if not date: print("  Cancelled."); _pause(); return

    new_txn = Transaction(state.next_id, name, product, amount, date)
    state.transactions.append(new_txn)
    state.next_id  += 1
    state.is_sorted = False   # list is unsorted after insert

    print(f"\n  /  TXN{new_txn.transaction_id:04d} inserted successfully.")
    print(f"     Note: List is now unsorted. Run Merge Sort to re-sort.")
    _row_header()
    _row(len(state.transactions), new_txn)
    _pause()


def performance_comparison() -> None:
    """Compare Merge Sort vs Binary Search execution times."""
    _header("PERFORMANCE COMPARISON")

    # Ensure we have a sorted copy for binary search
    original = list(state.transactions)
    sorted_copy = merge_sort(list(original))

    REPS = 500
    print(f"  Measuring over {REPS} repetitions each...\n")

    # Time Merge Sort
    ms_time = time_operation(
        merge_sort, list(original), repetitions=REPS
    )

    # Time Binary Search (existing key – TXN1047)
    existing_id = state.transactions[0].transaction_id
    bs_exist_time = time_operation(
        binary_search, sorted_copy, existing_id, repetitions=REPS
    )

    # Time Binary Search (non-existing key)
    bs_miss_time = time_operation(
        binary_search, sorted_copy, 9999, repetitions=REPS
    )

    # Time Linear Search (existing)
    ls_exist_time = time_operation(
        linear_search, sorted_copy, existing_id, repetitions=REPS
    )

    # Time Linear Search (non-existing)
    ls_miss_time = time_operation(
        linear_search, sorted_copy, 9999, repetitions=REPS
    )

    n = len(state.transactions)

    print(f"  Dataset size: n = {n} transactions")
    print(f"\n  {'Operation':<40} {'Avg Time (µs)':>15}  {'Complexity'}")
    print("  " + SUB_DIVIDER)
    print(f"  {'Merge Sort (full sort)':<40} {ms_time:>15.4f}  O(n log n)")
    print(f"  {'Binary Search – existing key':<40} {bs_exist_time:>15.4f}  O(log n)")
    print(f"  {'Binary Search – non-existing key':<40} {bs_miss_time:>15.4f}  O(log n)")
    print(f"  {'Linear Search – existing key':<40} {ls_exist_time:>15.4f}  O(n)")
    print(f"  {'Linear Search – non-existing key':<40} {ls_miss_time:>15.4f}  O(n)")
    print("  " + SUB_DIVIDER)


#  Main menu loop

def print_menu() -> None:
    status = "/ SORTED" if state.is_sorted else "X UNSORTED"
    print(f"\n{DIVIDER}")
    print(f"  CUSTOMER TRANSACTION SYSTEM  [{status}]  –  Main Menu")
    print(DIVIDER)
    print("  [1]  Display all transactions")
    print("  [2]  Sort using Merge Sort")
    print("  [3]  Search using Binary Search  (requires sorted data)")
    print("  [4]  Search using Linear Search")
    print("  [5]  Insert new transaction [Advanced]")
    print("  [6]  Performance comparison")
    print("  [0]  Exit")
    print(SUB_DIVIDER)


def main() -> None:
    print(DIVIDER)
    print("  Welcome to the Customer Transaction System")
    print("  Algorithms: Merge Sort  |  Binary Search  |  Linear Search")
    print(DIVIDER)
    print(f"\n  {len(state.transactions)} transaction records loaded (unsorted).")

    actions = {
        "1": display_all,
        "2": sort_merge_sort,
        "3": search_binary,
        "4": search_linear,
        "5": insert_transaction,
        "6": performance_comparison,
    }

    while True:
        print_menu()
        choice = input("  Enter your choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! Exiting Transaction System.\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  X  Invalid choice. Please enter 0–6.")


if __name__ == "__main__":
    main()
