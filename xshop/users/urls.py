from django.urls import path

from xshop.users import views

app_name = "users"

urlpatterns = [
    path("redirection/", views.redirection, name="redirection"),
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.register, name="register"),
]
