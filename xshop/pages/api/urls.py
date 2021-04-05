from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "pages_api"


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="pages_api:schema"),
        name="swagger",
    ),
]
