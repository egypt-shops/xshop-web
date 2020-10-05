from django.urls import path
from . import views

urlpatterns = [
    path("", views.LoginAPIView.as_view()),
]
