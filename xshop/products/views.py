from django.views.generic.base import TemplateView
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
        shops = Product.objects.filter(name__icontains=search_by)
        context = {
            "shops": shops,
        }
        return render(request, "pages/search_results.html", context)

    template_name = "pages/search_results.html"
