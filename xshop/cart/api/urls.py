from django.urls import path

from . import views

app_name = "cart_api"

urlpatterns = [
    path("", views.CartApi.as_view(), name="cart_operations"),
]
