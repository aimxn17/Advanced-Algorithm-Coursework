# medicine.py– Entity class for a Pharmacy Product

class Medicine:
    """Represents a single pharmacy product stored in the system."""

    # Allowed product categories
    VALID_TYPES = {"Tablet", "Syrup", "Supplement"}

    def __init__(self, medicine_id: str, name: str, medicine_type: str,
                 price: float, quantity: int, expiry_date: str):
        """
        Parameters
        ----------
        medicine_id   : Unique product code, used as the hash-table key (e.g. 'MED001')
        name          : Product name (e.g. 'Paracetamol 500mg')
        medicine_type : Category – must be one of VALID_TYPES
        price         : Retail price RM
        quantity      : Units in stock
        expiry_date   : Expiry date string in DD/MM/YYYY format
        """
        if medicine_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid type '{medicine_type}'. "
                f"Must be one of: {', '.join(sorted(self.VALID_TYPES))}"
            )
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.medicine_id = medicine_id.upper().strip()
        self.name = name.strip()
        self.medicine_type = medicine_type.strip()
        self.price = round(float(price), 2)
        self.quantity = int(quantity)
        self.expiry_date = expiry_date.strip()

    # ----------------------------------------------------------
    #  Representation helpers
    # ----------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"[{self.medicine_id}] {self.name} | "
            f"Type: {self.medicine_type} | "
            f"Price: RM{self.price:.2f} | "
            f"Qty: {self.quantity} | "
            f"Expiry: {self.expiry_date}"
        )

    def __repr__(self) -> str:
        return (
            f"Medicine(id={self.medicine_id!r}, name={self.name!r}, "
            f"type={self.medicine_type!r}, price={self.price}, "
            f"quantity={self.quantity}, expiry={self.expiry_date!r})"
        )

    #  Convenience: export as a plain dict (useful for display)
    def to_dict(self) -> dict:
        return {
            "ID": self.medicine_id,
            "Name": self.name,
            "Type": self.medicine_type,
            "Price (RM)": f"{self.price:.2f}",
            "Quantity": self.quantity,
            "Expiry Date": self.expiry_date,
        }
