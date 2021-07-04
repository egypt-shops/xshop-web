from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from xshop.shops.models import Shop
from xshop.products.models import Product


class ShopDetailView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        shop_id = kwargs["shop_id"]
        shop = Shop.objects.get(id=shop_id)

        products = Product.objects.filter(shop=shop)
        context = {
            "shop": shop.name,
            "products": products,
        }
        return render(request, "pages/shop_detail.html", context)


class ShopsSearchView(TemplateView):
    model = Shop
    template_name = "pages/search_results.html"

    def get(self, request, *args, **kwargs):
        search_by = request.GET.get("search_by")
        shops = Shop.objects.filter(name__icontains=search_by)
        context = {
            "shops": shops,
        }
        return render(request, "pages/search_results.html", context)
