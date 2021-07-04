from django.views.generic import TemplateView
from django.views.generic.base import TemplateView as TV
from django.shortcuts import render
from xshop.products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductDetailView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product = Product.objects.get(id=product_id)
        price = str(product.price)[4:]
        context = {
            "product": product,
            "price": price,
        }
        return render(request, "pages/product_detail.html", context)


class ProductsSearchView(TemplateView):
    def get(self, request, *args, **kwargs):
        search_by = request.GET.get("search_by")
        products = Product.objects.filter(name__icontains=search_by)
        context = {"products": products, "products_len": len(products)}
        return render(request, "pages/products_search_results.html", context)
