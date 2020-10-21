from django.urls import path

from . import views

app_name = "shops_api"

urlpatterns = [
    path("", views.ShopListApi.as_view(), name="shop_list"),
]
