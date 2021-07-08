from django.urls import path

from . import views

app_name = "shops_api"

urlpatterns = [
    path("", views.ShopListApi.as_view(), name="shop_list"),
    path("<slug:shop_subdomain>/", views.ShopDetailApi.as_view(), name="shop_detail"),
]
