from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path(
        "<int:product_id>/", views.ProductDetailView.as_view(), name="product_details"
    ),
    path(
        "search/<int:shop_id>/",
        views.ProductsSearchView.as_view(),
        name="product_search",
    ),
]
