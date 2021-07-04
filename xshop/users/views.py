from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from xshop.core.utils import UserGroup
from xshop.users.models import User

from xshop.users.forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def register(request):

    if request.user.is_authenticated:
        return redirect("users")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("name")
            mobile = form.cleaned_data.get("mobile")
            password = form.cleaned_data.get("password1")
            user = authenticate(name=name, mobile=mobile, password=password)
            user.save()
            login(request, user)
            return redirect("login")
        else:
            messages.error(request, "Correct the errors below")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def redirection(request):
    user: User = request.user

    # FIXME update redirection to the admin panel according to user type!
    if UserGroup.GENERAL_MANAGER in user.type:
        return redirect(reverse("admin:index"))
    elif UserGroup.CASHIER in user.type:
        return redirect(reverse("admin:orders_order_add"))
    elif UserGroup.DATA_ENTRY_CLERK in user.type:
        return redirect(reverse("admin:products_product_changelist"))
    elif request.user.is_superuser:
        return redirect(reverse("admin:index"))
    else:
        return redirect(reverse("pages:home"))


class Login(LoginView):
    redirect_authenticated_user = True
