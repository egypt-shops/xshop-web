from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from xshop.shops.models import Shop
from xshop.products.models import Product


class ShopDetailView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        shop_subdomain = kwargs["shop_subdomain"]
        shop = get_object_or_404(Shop, subdomain=shop_subdomain)
        products = Product.objects.filter(shop=shop)
        context = {
            "shop": shop,
            "products": products,
        }
        return render(request, "pages/shop_detail.html", context)


class ShopsSearchView(TemplateView):
    def get(self, request, *args, **kwargs):
        search_by = request.GET.get("search_by")
        shops = Shop.objects.filter(name__icontains=search_by)
        context = {
            "shops": shops,
        }
        return render(request, "pages/shops_search_results.html", context)
