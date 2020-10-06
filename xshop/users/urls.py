from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
]
