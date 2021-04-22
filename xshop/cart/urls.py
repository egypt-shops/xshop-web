from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_details, name="cart_details"),
    path("post/<int:product_id>/", views.cart_post, name="cart_ops"),
    path("delete/", views.cart_delete_item, name="cart_delete"),
]
