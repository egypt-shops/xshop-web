from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


@login_required
def redirection(request):
    user = request.user

    if "MANAGER" in user.type:
        return redirect(reverse("dashboard:manager"))
    elif "CASHIER" in user.type:
        return redirect(reverse("dashboard:cashier"))
    elif "DATA_ENTRY_CLERK" in user.type:
        return redirect(reverse("dashboard:data_entry"))
    elif request.user.is_superuser:
        return redirect(reverse("admin:index"))
    else:
        return redirect(reverse("pages:home"))


class Login(LoginView):
    redirect_authenticated_user = True
