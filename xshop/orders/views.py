import uuid

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# from django import forms
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderItem

# from .serializers import OrderSerializer, CheckoutSerializer
from xshop.products.models import Product
from xshop.cart.cart import Cart
from xshop.payments import paymob
from xshop.payments.models import PaymentAttempt
from xshop.orders.forms import CheckOutForm


class CheckOutView(LoginRequiredMixin, TemplateView):
    def post(self, request):

        form = CheckOutForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            address = cd["address"]
            paying_method = cd["paying_method"]
            cart = request.session.get("cart")
            current_shop = request.session.get("current_shop")

            # getting the cart details to make an order
            quantities = []
            product_ids = list(cart[current_shop].keys())
            full_price = 0
            try:
                for key in cart[current_shop].keys():

                    # product_ids.append(list(cart[current_shop].keys()))
                    quantities.append(cart[current_shop][key]["quantity"])
                    full_price += (
                        float(cart[current_shop][key]["price"])
                        * cart[current_shop][key]["quantity"]
                    )
            except Exception as e:
                return Response(
                    {
                        "message": "failure",
                        "error": str(e),
                        "hint": "make sure that you created cart first (cart exists for the user)",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            products = Product.objects.filter(id__in=product_ids)
            order = Order.objects.create(
                user=request.user,
                shop=products[0].shop,
                address=address,
                paying_method=paying_method,
            )

            # making orderItem for every product
            for i in range(len(quantities)):
                OrderItem.objects.create(
                    order=order, product=products[i], quantity=quantities[i]
                )

            if paying_method == "CASH_ON_DELIVERY":
                return redirect(
                    f"{reverse('payments:result')}?paying_method={paying_method}&order_id={order.id}"
                )

            # Handle card payment
            payment_attempt = PaymentAttempt.objects.create(
                mutual_reference=str(uuid.uuid4()), order=order
            )
            iframe_url = paymob.issue_payment(
                int(order.total_price.amount * 100),  # total price in cents
                payment_attempt.mutual_reference,
                items=[],
                billing_data={
                    "apartment": "NA",
                    "email": "NA",
                    "floor": "NA",
                    "first_name": "NA",
                    "street": "NA",
                    "building": "NA",
                    "phone_number": "NA",
                    "shipping_method": "NA",
                    "postal_code": "NA",
                    "city": "NA",
                    "country": "NA",
                    "last_name": "NA",
                    "state": "NA",
                },
            )
            return redirect(iframe_url)

    def get(self, request):
        form = CheckOutForm
        cart = Cart(request)
        full_price = 0
        product_ids = []
        for item in cart:
            full_price += item["total_price"]
            product_ids.append(item["product"]["id"])
        products = Product.objects.filter(id__in=product_ids)
        context = {
            "cart_len": len(list(products)),
            "full_price": full_price,
            "products": products,
            # "user": request.user,
            # "quantity_range": range(1, 10),
            # "ui": range(12),
            "form": form,
        }
        return render(request, "pages/checkout.html", context)
