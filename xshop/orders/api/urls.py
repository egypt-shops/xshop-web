from django.urls import path

from . import views

app_name = "orders_api"

urlpatterns = [
    path(
        "<int:order_id>/",
        views.OrderDetailPatchApi.as_view(),
        name="order_detail_patch",
    ),
    path("", views.OrderListCreateApi.as_view(), name="order_list_create"),
    path("checkout/", views.CheckoutApi.as_view(), name="checkout_operations"),
]
