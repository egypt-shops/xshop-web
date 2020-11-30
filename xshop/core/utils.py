from enum import Enum


class UserGroup(str, Enum):
    """Source of all user groups in the system"""

    CUSTOMER = "Customer"
    CASHIER = "Cashier"
    DATA_ENTRY_CLERK = "Data Entry Clerk"
    MANAGER = "Manager"
    GENERAL_MANAGER = "General Manager"

    def __str__(self) -> str:
        return str(self)
