from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse

from xshop.core.utils import UserGroup
from xshop.users.models import User


@login_required
def redirection(request):
    user: User = request.user

    # FIXME update redirection to the admin panel according to user type!
    if UserGroup.GENERAL_MANAGER in user.type:
        return redirect(reverse("admin:index"))
    elif UserGroup.CASHIER in user.type:
        return redirect(reverse("dashboard:cashier"))
    elif UserGroup.DATA_ENTRY_CLERK in user.type:
        return redirect(reverse("dashboard:data_entry"))
    elif request.user.is_superuser:
        return redirect(reverse("admin:index"))
    else:
        return redirect(reverse("pages:home"))


class Login(LoginView):
    redirect_authenticated_user = True
