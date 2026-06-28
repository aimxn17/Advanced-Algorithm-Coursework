#  dataset.py  –  Predefined Transaction Dataset (unsorted)
#  10 transactions - ID out of order to demonstrate sorting.

from transaction import Transaction

def get_dataset() -> list:

    return [
        Transaction(1047, "Ahmad Razif",      "Wireless Earbuds",       199.90, "08/05/2026"),
        Transaction(1012, "Nur Qasrina",     "MSI Monitor 32in 240hz",  1779.50, "10/02/2026"),
        Transaction(1083, "Lee Chong Yu",    "Logitech Mechanical Keyboard", 349.00, "28/06/2026"),
        Transaction(1005, "Michael Scofield",        "USB-C Charging Hub",       55.00, "01/01/2026"),
        Transaction(1061, "Harry Khalifah",     "Stanley Tumbler 20oz",  229.00, "05/06/2026"),
        Transaction(1029, "Jon Snow",       "Laptop Stand", 115.00, "18/04/2026"),
        Transaction(1074, "Thomas Shelby",        "Night Lamp", 18.50, "11/06/2026"),
        Transaction(1038, "Emilia Targaryen",  "Bluetooth Speaker",       229.00, "27/04/2026"),
        Transaction(1016, "Leonal Das",      "Yoga Mat Premium",         88.00, "19/03/2026"),
        Transaction(1055, "Hafizuddin Omar",  "Nike Vomero 18plus UK 8.5",    759.00, "22/05/2026"),
    ]
