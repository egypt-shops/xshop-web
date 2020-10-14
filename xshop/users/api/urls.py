from django.urls import path
from . import views


app_name = "users_api"

urlpatterns = [
    path("token/", views.TokenApi.as_view(), name="token"),
]
