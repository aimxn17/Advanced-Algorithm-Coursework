#  transaction.py - Entity Class for a Customer Transaction


class Transaction:
    """
    Attributes--
    transaction_id   : Unique numeric ID used as the sort/search key (int)
    customer_name    : Name of customer (str)
    product_name     : Name of the product purchased (str)
    amount           : Product price in RM (float)
    transaction_date : Date of transaction in DD/MM/YYYY format (str)
    """

    def __init__(self, transaction_id: int, customer_name: str,
                 product_name: str, amount: float, transaction_date: str):

        if not isinstance(transaction_id, int) or transaction_id <= 0:
            raise ValueError("transaction_id must be a positive integer.")
        if amount < 0:
            raise ValueError("amount cannot be negative.")

        self.transaction_id   = transaction_id
        self.customer_name    = customer_name.strip()
        self.product_name     = product_name.strip()
        self.amount           = round(float(amount), 2)
        self.transaction_date = transaction_date.strip()


    #  Comparison operators (used by sort / search on ID)
    def __lt__(self, other): return self.transaction_id <  other.transaction_id
    def __le__(self, other): return self.transaction_id <= other.transaction_id
    def __eq__(self, other): return self.transaction_id == other.transaction_id
    def __gt__(self, other): return self.transaction_id >  other.transaction_id


    #  Display helpers
    def __str__(self) -> str:
        return (f"[TXN{self.transaction_id:04d}] {self.customer_name:<20} "
                f"{self.product_name:<25} RM{self.amount:>8.2f}  {self.transaction_date}")

    def __repr__(self) -> str:
        return (f"Transaction(id={self.transaction_id}, customer={self.customer_name!r}, "
                f"product={self.product_name!r}, amount={self.amount}, date={self.transaction_date!r})")

    def to_dict(self) -> dict:
        return {
            "Transaction ID" : f"TXN{self.transaction_id:04d}",
            "Customer Name"  : self.customer_name,
            "Product Name"   : self.product_name,
            "Amount (RM)"    : f"{self.amount:.2f}",
            "Date"           : self.transaction_date,
        }
