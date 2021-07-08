from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.ShopsSearchView.as_view(), name="shop_search"),
    path("<slug:shop_subdomain>/", views.ShopDetailView.as_view(), name="shop_details"),
]
