#  main.py  –  Command-Line Pharmacy Inventory System

from medicine import Medicine
from hash_table import HashTable, load_sample_data


#  Display helpers
DIVIDER      = "=" * 72
SUB_DIVIDER  = "-" * 72

def _header(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)

def _print_medicine_row_header() -> None:
    print(f"  {'ID':<10} {'Name':<28} {'Type':<12} {'Price':>8} {'Qty':>6}  {'Expiry'}")
    print("  " + SUB_DIVIDER)

def _print_medicine_row(med: Medicine) -> None:
    print(
        f"  {med.medicine_id:<10} {med.name:<28} {med.medicine_type:<12} "
        f"RM{med.price:>6.2f} {med.quantity:>6}  {med.expiry_date}"
    )

def _pause() -> None:
    input("\n  Press Enter to return to the menu...")


#  Menu actions
def display_all(ht: HashTable) -> None:
    """Display every live record in the hash table."""
    _header("ALL INVENTORY RECORDS")
    records = ht.get_all()

    if not records:
        print("  No records found in the inventory.")
        _pause()
        return

    _print_medicine_row_header()
    for med in records:
        _print_medicine_row(med)

    print(f"\n  Total records: {len(records)}  |  "
          f"Table load: {ht.load_factor():.1%}  |  "
          f"Free slots: {ht.TABLE_SIZE - ht._count}")
    _pause()


def search_medicine(ht: HashTable) -> None:
    """Search for a medicine by its ID and display the result."""
    _header("SEARCH MEDICINE")
    key = input("  Enter Medicine ID to search (e.g. MED001): ").strip().upper()

    if not key:
        print("  No ID entered. Returning to menu.")
        _pause()
        return

    result = ht.search(key)
    probes = ht.get_last_probe_count()

    if result:
        print(f"\n  ✔  Record found (probes used: {probes})\n")
        _print_medicine_row_header()
        _print_medicine_row(result)
    else:
        print(f"\n  ✘  '{key}' not found in inventory. (probes used: {probes})")

    _pause()


def insert_medicine(ht: HashTable) -> None:
    """Prompt the user for details and insert a new Medicine record."""
    _header("INSERT NEW MEDICINE")

    if ht.load_factor() >= ht.LOAD_LIMIT:
        print(f"  ✘  Table is at {ht.load_factor():.0%} capacity. Cannot insert more records.")
        _pause()
        return

    print("  Fill in the details below (or press Enter to cancel at any prompt).\n")

    #Medicine ID
    med_id = input("  Medicine ID (e.g. MED008): ").strip().upper()
    if not med_id:
        print("  Cancelled.")
        _pause()
        return

    # Check duplicate before continuing
    if ht.search(med_id):
        print(f"  ✘  ID '{med_id}' already exists. Use Edit to modify it.")
        _pause()
        return

    #Name
    name = input("  Name: ").strip()
    if not name:
        print("  Cancelled.")
        _pause()
        return

    #Type
    print(f"  Type options: {', '.join(sorted(Medicine.VALID_TYPES))}")
    med_type = input("  Type: ").strip().capitalize()
    if not med_type:
        print("  Cancelled.")
        _pause()
        return
    if med_type not in Medicine.VALID_TYPES:
        print(f"  ✘  Invalid type '{med_type}'. Must be one of: "
              f"{', '.join(sorted(Medicine.VALID_TYPES))}")
        _pause()
        return

    #Price
    try:
        price = float(input("  Price (RM): ").strip())
        if price < 0:
            raise ValueError
    except ValueError:
        print("  ✘  Invalid price. Must be a non-negative number.")
        _pause()
        return

    #Quantity
    try:
        qty = int(input("  Quantity: ").strip())
        if qty < 0:
            raise ValueError
    except ValueError:
        print("  ✘  Invalid quantity. Must be a non-negative whole number.")
        _pause()
        return

    #Expiry Date
    expiry = input("  Expiry Date (MM/YYYY): ").strip()
    if not expiry:
        print("  Cancelled.")
        _pause()
        return

    # Build and insert
    new_med = Medicine(med_id, name, med_type, price, qty, expiry)
    success = ht.insert(new_med)

    if success:
        print(f"\n  ✔  '{med_id}' inserted successfully.")
        _print_medicine_row_header()
        _print_medicine_row(new_med)
    else:
        print(f"\n  ✘  Insert failed for '{med_id}'.")

    _pause()


def edit_medicine(ht: HashTable) -> None:
    """Edit fields of an existing medicine record."""
    _header("EDIT MEDICINE")
    key = input("  Enter Medicine ID to edit (e.g. MED001): ").strip().upper()

    if not key:
        print("  No ID entered. Returning to menu.")
        _pause()
        return

    existing = ht.search(key)
    if not existing:
        print(f"  ✘  '{key}' not found. Nothing to edit.")
        _pause()
        return

    print(f"\n  Current record:")
    _print_medicine_row_header()
    _print_medicine_row(existing)
    print("\n  Enter new values (press Enter to keep the current value).\n")

    # Keep existing values if user presses Enter
    name_in = input(f"  Name [{existing.name}]: ").strip()
    name = name_in if name_in else existing.name

    print(f"  Type options: {', '.join(sorted(Medicine.VALID_TYPES))}")
    type_in = input(f"  Type [{existing.medicine_type}]: ").strip().capitalize()
    med_type = type_in if type_in else existing.medicine_type
    if med_type not in Medicine.VALID_TYPES:
        print(f"  ✘  Invalid type. Keeping original: {existing.medicine_type}")
        med_type = existing.medicine_type

    price_in = input(f"  Price (RM) [{existing.price:.2f}]: ").strip()
    try:
        price = float(price_in) if price_in else existing.price
        if price < 0:
            raise ValueError
    except ValueError:
        print("  ✘  Invalid price. Keeping original.")
        price = existing.price

    qty_in = input(f"  Quantity [{existing.quantity}]: ").strip()
    try:
        qty = int(qty_in) if qty_in else existing.quantity
        if qty < 0:
            raise ValueError
    except ValueError:
        print("  ✘  Invalid quantity. Keeping original.")
        qty = existing.quantity

    expiry_in = input(f"  Expiry Date [{existing.expiry_date}]: ").strip()
    expiry = expiry_in if expiry_in else existing.expiry_date

    # Confirm before saving
    updated = Medicine(key, name, med_type, price, qty, expiry)
    print(f"\n  Updated record preview:")
    _print_medicine_row_header()
    _print_medicine_row(updated)

    confirm = input("\n  Save changes? (y/n): ").strip().lower()
    if confirm == 'y':
        ht.update(updated)
        print("  ✔  Record updated successfully.")
    else:
        print("  Edit cancelled. No changes made.")

    _pause()


def delete_medicine(ht: HashTable) -> None:
    """Delete a medicine record from the hash table."""
    _header("DELETE MEDICINE")
    key = input("  Enter Medicine ID to delete (e.g. MED001): ").strip().upper()

    if not key:
        print("  No ID entered. Returning to menu.")
        _pause()
        return

    existing = ht.search(key)
    if not existing:
        print(f"  ✘  '{key}' not found. Nothing to delete.")
        _pause()
        return

    print(f"\n  Record to delete:")
    _print_medicine_row_header()
    _print_medicine_row(existing)

    confirm = input("\n  Are you sure you want to delete this record? (y/n): ").strip().lower()
    if confirm == 'y':
        ht.delete(key)
        print(f"  ✔  '{key}' deleted from inventory.")
    else:
        print("  Delete cancelled.")

    _pause()


def show_hash_table_layout(ht: HashTable) -> None:
    """Show the raw internal slot layout of the hash table."""
    _header("RAW HASH TABLE LAYOUT")
    ht.display_table()
    _pause()


#  Main menu loop
def print_menu() -> None:
    print(f"\n{DIVIDER}")
    print("  PHARMACY INVENTORY SYSTEM  –  Main Menu")
    print(DIVIDER)
    print("  [1] Display all inventory")
    print("  [2] Search medicine by ID")
    print("  [3] Insert new medicine")
    print("  [4] Edit existing medicine")
    print("  [5] Delete medicine")
    print("  [6] Show raw hash table layout")
    print("  [0] Exit")
    print(SUB_DIVIDER)


def main() -> None:
    print(DIVIDER)
    print("  Welcome to the Pharmacy Inventory System")
    print("  Data structure: Hash Table with Linear Probing")
    print(DIVIDER)

    # Initialise hash table and load predefined sample data
    ht = HashTable()
    load_sample_data(ht)

    menu_actions = {
        "1": display_all,
        "2": search_medicine,
        "3": insert_medicine,
        "4": edit_medicine,
        "5": delete_medicine,
        "6": show_hash_table_layout,
    }

    while True:
        print_menu()
        choice = input("  Enter your choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! Exiting Pharmacy Inventory System.\n")
            break
        elif choice in menu_actions:
            menu_actions[choice](ht)
        else:
            print("  ✘  Invalid choice. Please enter 0–6.")


if __name__ == "__main__":
    main()
