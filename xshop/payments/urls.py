from django.urls import path
from xshop.payments import views

urlpatterns = [
    path("callback", views.callback, name="callback"),
    path("redirect", views.redirect, name="redirect"),
]
