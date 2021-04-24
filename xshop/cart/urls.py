from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_details, name="cart_details"),
    path("post/", views.cart_post, name="cart_ops"),
    path("remove/", views.cart_remove_clear, name="cart_remove"),
]
