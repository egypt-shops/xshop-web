from django.urls import reverse
from django.shortcuts import redirect


def redirection(request):
    user = request.user

    if "MANAGER" in user.type:
        return redirect(reverse("dashboard:manager"))
    elif "CASHIER" in user.type:
        return redirect(reverse("dashboard:cashier"))
    else:
        return redirect(reverse("pages:home"))
