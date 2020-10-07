"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from xshop.pages.views import Home, SwaggerApi


def trigger_error(request):
    1 / 0


schema_view = get_schema_view(
    title="XShop Web API",
    description="API for XShop web to be integrated with mobile application and website",
    version="1.0.0",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("users/", include("xshop.users.urls", namespace="users")),
    path("schema/", schema_view, name="schema"),
    path("swagger/", SwaggerApi.as_view(), name="swagger"),
    # for testing error alerts
    # path("sentry-debug/", trigger_error),
]

# media & static urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin Site texts
admin.site.site_header = "Egypt Shops administration"
admin.site.site_title = "Egypt Shops Admin Portal"
admin.site.index_title = "XShop administration"
