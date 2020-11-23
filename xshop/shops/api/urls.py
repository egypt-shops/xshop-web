from django.urls import path

from . import views

app_name = "shops_api"

urlpatterns = [
    path("", views.ShopListApi.as_view(), name="shop_list"),
    path("products/", views.ShopProductListApi.as_view(), name="product_list"),
    path("<int:shop_id>/", views.ShopDetailApi.as_view(), name="shop_detail"),
]
