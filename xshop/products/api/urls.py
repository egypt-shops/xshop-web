from django.urls import path

from . import views

app_name = "products_api"

urlpatterns = [
    path(
        "<int:product_id>/",
        views.ProductDetailPatchApi.as_view(),
        name="product_detail_patch",
    ),
    path("", views.ProductListCreateApi.as_view(), name="product_list_create"),
]
