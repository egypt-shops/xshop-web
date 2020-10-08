from django.urls import path
from rest_framework.schemas import get_schema_view

from .views import SwaggerUi

app_name = "pages_api"

schema_view = get_schema_view(
    title="XShop Web API",
    description="API for XShop web to be integrated with mobile application and website",
    version="1.0.0",
)

urlpatterns = [
    path("schema/", schema_view, name="schema"),
    path("swagger/", SwaggerUi.as_view(), name="swagger"),
]
