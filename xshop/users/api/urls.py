from django.urls import path

from xshop.users.api import views

app_name = "users_api"

urlpatterns = [
    path("token/", views.TokenApi.as_view(), name="token"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("register/", views.registration_view, name="register"),
]
