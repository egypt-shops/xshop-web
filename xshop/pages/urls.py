from django.urls import path
from .views import Home,LandingPage

app_name = "pages"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("landingpage/", LandingPage.as_view(), name="landingpage"),

]
