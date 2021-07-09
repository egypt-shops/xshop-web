from django.urls import path
from django.views.generic.base import TemplateView

from .views import Home

app_name = "pages"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="footer_pages/about.html"),
        name="about",
    ),
    path(
        "thankyou/",
        TemplateView.as_view(template_name="pages/thankyou.html"),
        name="thankyou",
    ),
    path(
        "terms/",
        TemplateView.as_view(template_name="footer_pages/terms.html"),
        name="terms",
    ),
    path(
        "privacy_policy/",
        TemplateView.as_view(template_name="footer_pages/privacy_policy.html"),
        name="privacy_policy",
    ),
    path(
        "services/",
        TemplateView.as_view(template_name="footer_pages/services.html"),
        name="services",
    ),
]
