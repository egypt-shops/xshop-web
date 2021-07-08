from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path(
        "search/<slug:shop_subdomain>/",
        views.ProductsSearchView.as_view(),
        name="product_search",
    ),
    path(
        "<int:product_id>/", views.ProductDetailView.as_view(), name="product_details"
    ),
]
