from django.urls import path
from . import views


app_name = "core_api"

urlpatterns = [
    path(
        "product/<int:product_id>/",
        views.ProductDetailPatchApi.as_view(),
        name="product_detail_patch",
    ),
    path("product/", views.ProductListCreateApi.as_view(), name="product_list_create"),
]
