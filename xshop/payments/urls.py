from django.urls import path
from xshop.payments import views

urlpatterns = [
    path("redirect", views.redirect, name="redirect"),
]
