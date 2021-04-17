from django.views.generic import TemplateView
from django.shortcuts import render
from xshop.cart.cart import Cart


class CartView(TemplateView):
    def get(self, *args, **kwargs):

        user_cart = Cart
        context = {
            "carts": user_cart,
        }

        return render(self.request, "pages/cart.html", context)
