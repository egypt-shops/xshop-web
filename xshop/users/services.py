from typing import Optional

from .models import Cashier, Customer, DataEntryClerk, Manager, SubManager, User


def user_create(
    *,
    name: Optional[str] = "",
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
    mobile: str,
    password: str,
    email: Optional[str] = None,
) -> User:
    user = User.objects.create_user(
        name=name,
        mobile=mobile,
        email=email,
        is_active=is_active,
        is_staff=is_staff,
        password=password,
    )

    return user


def customer_create(
    *,
    name: Optional[str] = "",
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
    mobile: str,
    password: str,
    email: Optional[str] = None,
) -> Customer:
    user = Customer.objects.create(
        name=name,
        mobile=mobile,
        email=email,
        is_active=is_active,
        is_staff=is_staff,
        password=password,
    )

    return user


def cashier_create(
    *,
    name: Optional[str] = "",
    is_active: bool = True,
    is_staff: bool = True,
    is_superuser: bool = False,
    mobile: str,
    password: str,
    email: Optional[str] = None,
    type: User.Types = User.Types.CASHIER,
) -> Cashier:
    user = Cashier.objects.create(
        name=name,
        mobile=mobile,
        email=email,
        is_active=is_active,
        is_staff=is_staff,
        password=password,
        type=type,
    )

    return user


def data_entry_create(
    *,
    name: Optional[str] = "",
    is_active: bool = True,
    is_staff: bool = True,
    is_superuser: bool = False,
    mobile: str,
    password: str,
    email: Optional[str] = None,
    type: User.Types = User.Types.DATA_ENTRY_CLERK,
) -> DataEntryClerk:
    user = DataEntryClerk.objects.create(
        name=name,
        mobile=mobile,
        email=email,
        is_active=is_active,
        is_staff=is_staff,
        password=password,
        type=type,
    )

    return user


def manager_create(
    *,
    name: Optional[str] = "",
    is_active: bool = True,
    is_staff: bool = True,
    is_superuser: bool = False,
    mobile: str,
    password: str,
    email: Optional[str] = None,
    type: User.Types = User.Types.MANAGER,
) -> Manager:
    user = Manager.objects.create(
        name=name,
        mobile=mobile,
        email=email,
        is_active=is_active,
        is_staff=is_staff,
        password=password,
        type=type,
    )

    return user


def sub_manager_create(
    *,
    name: Optional[str] = "",
    is_active: bool = True,
    is_staff: bool = True,
    is_superuser: bool = False,
    mobile: str,
    password: str,
    email: Optional[str] = None,
    type: User.Types = User.Types.SUB_MANAGER,
) -> Manager:
    user = SubManager.objects.create(
        name=name,
        mobile=mobile,
        email=email,
        is_active=is_active,
        is_staff=is_staff,
        password=password,
        type=type,
    )

    return user
