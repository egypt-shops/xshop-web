from django.urls import path
from xshop.payments import views

app_name = "payments"

urlpatterns = [
    path("result", views.result, name="result"),
]
