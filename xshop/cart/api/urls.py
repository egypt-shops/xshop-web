from django.urls import path

from . import views

app_name = "cart_api"

urlpatterns = [
    path("", views.AddToCartApi.as_view(), name="add_get_clear_cart"),
    path(
        "<int:product_id>/",
        views.RemoveFromCartApi.as_view(),
        name="remove_product_from_cart",
    ),
]
