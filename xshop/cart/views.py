from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404

from xshop.cart.cart import Cart
from xshop.cart.forms import CartPostProductForm
from xshop.products.models import Product


@login_required
def cart_post(request):
    cart = Cart(request)
    form = CartPostProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = int(cd["quantity"])
        action = cd["actions"]
        product = cd['product']
    else:
        raise form.errors

    if action == "add":
        cart.add(product=product)

        return redirect("cart:cart_details")

    elif action == "update":
        cart.update(
            product=product,
            quantity=quantity,
        )
        return redirect("cart:cart_details")


@login_required
def cart_details(request):
    cart = Cart(request)
    full_price = 0
    for item in cart:
        full_price += item["total_price"]
        item["update_quantity_form"] = CartPostProductForm(
            initial={"quantity": item["quantity"],
                     "actions": "update",
                     "product_id": item['product']['id']}
        )
    context = {
        "cart": cart,
        "full_price": full_price,
        "user": request.user,
    }
    return render(request, "pages/cart.html", context)


@login_required
def cart_remove_clear(request):
    cart = Cart(request)
    if request.POST.get("action") == "remove":
        product_id = int(request.POST.get("productid"))
        cart.remove(product_id)
    
    if request.POST.get("action") == "clear":
        cart.clear()

    return redirect("cart:cart_details")
