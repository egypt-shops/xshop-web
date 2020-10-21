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


def trigger_error(request):
    1 / 0


api_urlpatterns = [
    path("users/", include("xshop.users.api.urls", namespace="users_api")),
    path("products/", include("xshop.products.api.urls", namespace="products_api")),
    path("shops/", include("xshop.shops.api.urls", namespace="shops_api")),
    path("", include("xshop.pages.api.urls", namespace="pages_api")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("xshop.users.urls", namespace="users")),
    path("users/", include("django.contrib.auth.urls")),
    path("invoices/", include("xshop.invoices.urls", namespace="invoices")),
    path("core/", include("xshop.core.urls", namespace="core")),
    path("api/", include(api_urlpatterns)),  # API urls from above
    path("", include("xshop.pages.urls", namespace="pages")),
    # for testing error alerts
    # path("sentry-debug/", trigger_error),
]

# media & static urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin Site texts
admin.site.site_header = "Egypt Shops administration"
admin.site.site_title = "Egypt Shops Admin Portal"
admin.site.index_title = "Egypt Shops administration"
