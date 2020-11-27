from enum import Enum


class UserRoles(str, Enum):
    """Source of all custom user roles (groups) in the system"""

    MANAGER = "Manager"
    CASHIER = "Cashier"
    DEC = "Data Entry Clerk"
    CUSTOMER = "Customer"

    def __str__(self) -> str:
        return str(self)
