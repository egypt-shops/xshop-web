from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from xshop.products.models import Product, Rating
from xshop.shops.models import Shop
from .forms import RatingForm


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
    def get(self, request, shop_id, *args, **kwargs):
        search_by = request.GET.get("search_by")
        products = Product.objects.filter(name__icontains=search_by, shop_id=shop_id)
        shop = Shop.objects.get(id=shop_id)
        context = {
            "products": products,
            "products_len": len(products),
            "shop": shop,
        }
        return render(request, "pages/products_search_results.html", context)


def add_rating(request, id):
    product = get_object_or_404(Product, pk=id)
    # pro = Product.objects.get(id=id)
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data["product"]
            user = form.cleaned_data["user"]
            rating = form.cleaned_data["rating"]

            product = (request.POST.get("product", ""),)
            user = (request.POST.get("user", ""),)
            rating = (request.POST.get("rating", ""),)

            obj = Rating(product=product, user=user, rating=rating)
            obj.save()
            context = {"obj": obj}
            return render(request, "pages/product_detail.html", context)
        else:
            form = RatingForm()
        return HttpResponse("Please rate the product")
