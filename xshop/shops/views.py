from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from xshop.shops.models import Shop
from xshop.products.models import Product


class ShopDetailView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        shop_id = kwargs["shop_id"]
        shop = Shop.objects.get(id=shop_id)
        if request.POST.get("action") == "search":
            breakpoint()
            search_by = request.POST.get("search_by")
            products = Product.objects.filter(name__search=search_by)
            context = {
                "shop": shop.name,
                "products": products,
            }
            return render(request, "pages/shop_detail.html", context)

        products = Product.objects.filter(shop=shop)
        context = {
            "shop": shop.name,
            "products": products,
        }
        return render(request, "pages/shop_detail.html", context)
