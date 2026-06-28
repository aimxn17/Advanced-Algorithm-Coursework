#  hash_table.py  –  Hash Table using Linear Probing


from medicine import Medicine


# Sentinel object to mark a slot as "deleted"
# (needed so searches don't stop early at an empty-after-delete slot)
_DELETED = object()


class HashTable:
    """
    Fixed-size hash table with LINEAR PROBING for collision resolution.

    Key   → medicine_id  (string, e.g. 'MED001')
    Value → Medicine object
    """

    TABLE_SIZE   = 11   # Prime number keeps distribution even
    LOAD_LIMIT   = 0.7  # Refuse inserts once 70 % of slots are occupied

    def __init__(self):
        # Each slot is one of: None | _DELETED | Medicine
        self._table: list = [None] * self.TABLE_SIZE
        self._count  = 0   # Number of live records
        self._probes = 0   # Diagnostic: total probes since last reset

    #  Hash function
    def _hash(self, key: str) -> int:
        """
        Simple additive hash:
            index = (sum of ASCII values) mod TABLE_SIZE

        Using the medicine_id characters (all uppercase after normalisation)
        gives a reasonably spread distribution for short IDs like 'MED001'.
        """
        return sum(ord(ch) for ch in key.upper()) % self.TABLE_SIZE

    #  Core operations
    def insert(self, medicine: Medicine) -> bool:
        """
        Insert a Medicine record.

        Returns True on success, False if the table is full or the key
        already exists (use update() to overwrite).

        Linear-probing step: index = (hash + i) mod TABLE_SIZE
        """
        if self.load_factor() >= self.LOAD_LIMIT:
            print(f"  [HashTable] Table is at {self.load_factor():.0%} capacity – insert rejected.")
            return False

        key   = medicine.medicine_id
        index = self._hash(key)

        first_deleted = None   # Remember first _DELETED slot for reuse

        for i in range(self.TABLE_SIZE):
            probe = (index + i) % self.TABLE_SIZE
            slot  = self._table[probe]

            if slot is None:
                # Empty slot → insert here (or at the earlier deleted slot)
                target = first_deleted if first_deleted is not None else probe
                self._table[target] = medicine
                self._count += 1
                return True

            if slot is _DELETED:
                if first_deleted is None:
                    first_deleted = probe   # Mark, keep scanning for duplicates

            elif slot.medicine_id == key:
                print(f"  [HashTable] Duplicate key '{key}' – use update() to overwrite.")
                return False

        # All slots scanned, none free → full (shouldn't reach here with LOAD_LIMIT)
        if first_deleted is not None:
            self._table[first_deleted] = medicine
            self._count += 1
            return True

        return False

    def search(self, key: str) -> Medicine | None:
        """
        Search for a Medicine by its ID.

        Uses the same linear-probing sequence as insert().
        Returns the Medicine object or None if not found.
        Also updates self._probes for performance analysis.
        """
        key   = key.upper().strip()
        index = self._hash(key)
        self._probes = 0

        for i in range(self.TABLE_SIZE):
            probe = (index + i) % self.TABLE_SIZE
            slot  = self._table[probe]
            self._probes += 1

            if slot is None:
                # Unoccupied slot → key cannot exist beyond this point
                return None

            if slot is _DELETED:
                continue   # Skip tombstones, keep probing

            if slot.medicine_id == key:
                return slot   # Found!

        return None   # Full table traversal, not found

    def delete(self, key: str) -> bool:
        """
        Soft-delete: replace the slot with the _DELETED sentinel.
        This preserves the probing chain for subsequent searches.
        Returns True if deleted, False if key not found.
        """
        key   = key.upper().strip()
        index = self._hash(key)

        for i in range(self.TABLE_SIZE):
            probe = (index + i) % self.TABLE_SIZE
            slot  = self._table[probe]

            if slot is None:
                return False   # Key not in table

            if slot is _DELETED:
                continue

            if slot.medicine_id == key:
                self._table[probe] = _DELETED   # Tombstone
                self._count -= 1
                return True

        return False

    def update(self, medicine: Medicine) -> bool:
        """
        Overwrite an existing record with new Medicine data.
        Returns True on success, False if the key does not exist.
        """
        key   = medicine.medicine_id
        index = self._hash(key)

        for i in range(self.TABLE_SIZE):
            probe = (index + i) % self.TABLE_SIZE
            slot  = self._table[probe]

            if slot is None:
                return False   # Key not found

            if slot is _DELETED:
                continue

            if slot.medicine_id == key:
                self._table[probe] = medicine
                return True

        return False

    #  Utility / display helpers
    def load_factor(self) -> float:
        return self._count / self.TABLE_SIZE

    def get_last_probe_count(self) -> int:
        """Return the number of probes made during the last search() call."""
        return self._probes

    def get_all(self) -> list[Medicine]:
        """Return a list of all live Medicine records (order = slot order)."""
        return [slot for slot in self._table
                if slot is not None and slot is not _DELETED]

    def display_table(self) -> None:
        """
        Print the internal layout of the hash table slot-by-slot.
        Useful for debugging and understanding probe sequences.
        """
        print("\n" + "=" * 65)
        print(f"  HASH TABLE STATE  (size={self.TABLE_SIZE}, "
              f"records={self._count}, "
              f"load={self.load_factor():.1%})")
        print("=" * 65)
        print(f"  {'Slot':<6} {'Status':<10} {'Key':<10} {'Name'}")
        print("  " + "-" * 60)
        for i, slot in enumerate(self._table):
            if slot is None:
                print(f"  [{i:>2}]   {'EMPTY':<10} {'—':<10} —")
            elif slot is _DELETED:
                print(f"  [{i:>2}]   {'DELETED':<10} {'—':<10} —")
            else:
                print(f"  [{i:>2}]   {'OCCUPIED':<10} {slot.medicine_id:<10} {slot.name}")
        print("=" * 65 + "\n")


#  Sample data loader

def load_sample_data(ht: HashTable) -> None:
    """
    Insert 7 predefined pharmacy records into the hash table.
    Covers all three product types: Tablet, Syrup, Supplement.
    """
    samples = [
        Medicine("MED001", "Paracetamol 500mg",      "Tablet",     2.50,  120, "12/2026"),
        Medicine("MED002", "Ibuprofen 400mg",         "Tablet",     4.80,   85, "06/2026"),
        Medicine("MED003", "Amoxicillin 250mg",       "Tablet",     9.90,   60, "03/2027"),
        Medicine("MED004", "Piriton Syrup",           "Syrup",      6.50,   40, "09/2026"),
        Medicine("MED005", "Cough Relief Syrup",      "Syrup",      8.20,   35, "11/2026"),
        Medicine("MED006", "Vitamin C 1000mg",        "Supplement", 15.90,  75, "01/2028"),
        Medicine("MED007", "Omega-3 Fish Oil Softgel","Supplement", 22.50,  50, "08/2027"),
    ]

    print("\n  Loading sample pharmacy records into hash table...")
    print(f"  {'Key':<10} {'Hash Index':<14} {'Result'}")
    print("  " + "-" * 45)

    for med in samples:
        idx     = ht._hash(med.medicine_id)
        success = ht.insert(med)
        status  = "Inserted" if success else "FAILED"
        print(f"  {med.medicine_id:<10} index={idx:<8}     {status}")

    print(f"\n  Done – {ht._count} records loaded.\n")
