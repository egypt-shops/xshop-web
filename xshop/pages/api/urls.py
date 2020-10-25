from django.urls import path
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

app_name = "pages_api"

schema_view = get_schema_view(
    openapi.Info(
        title="XShop Web API",
        default_version="v1",
        description="API for XShop web to be integrated with mobile application and website",
    ),
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
