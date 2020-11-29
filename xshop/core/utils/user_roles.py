from enum import Enum


class UserRoles(str, Enum):
    """Source of all custom user roles (groups) in the system"""

    GENERAL_MANAGER = "General Manager"
    MANAGER = "Manager"
    CASHIER = "Cashier"
    DATA_ENTRY_CLERK = "Data Entry Clerk"
    CUSTOMER = "Customer"

    def __str__(self) -> str:
        return str(self)
