from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from xshop.core.utils import UserGroup
from xshop.dashboard.decorators import allowed_groups


@login_required
@allowed_groups([UserGroup.GENERAL_MANAGER])
def general_manager(request):
    return render(request, "dashboard/general_manager.html")


def cashier(request):
    return render(request, "dashboard/cashier.html")


def data_entry(request):
    return render(request, "dashboard/data_entry.html")
