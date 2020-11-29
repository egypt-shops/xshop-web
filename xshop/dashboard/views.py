from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from xshop.core.utils.user_roles import UserRoles
from xshop.dashboard.decorators import allowed_users


@login_required
@allowed_users([UserRoles.GENERAL_MANAGER])
def general_manager(request):
    return render(request, "dashboard/general_manager.html")


def cashier(request):
    return render(request, "dashboard/cashier.html")


def data_entry(request):
    return render(request, "dashboard/data_entry.html")
