from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from xshop.shops.models import Shop
from xshop.products.models import Product


class ShopView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):  # class based view def post, def get

        return render(request, "pages/shop_details.html")

    def get(self, request, *args, **kwargs):
        shop_id = kwargs["shop_id"]
        shop = Shop.objects.get(id=shop_id)
        products = Product.objects.filter(shop=shop)
        context = {
            "products": products,
        }
        return render(request, "pages/shop_details.html", context)
