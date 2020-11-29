from django.urls import path

from xshop.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("general-manager/", views.general_manager, name="general_manager"),
    path("cashier/", views.cashier, name="cashier"),
    path("data-entry/", views.data_entry, name="data_entry"),
]
