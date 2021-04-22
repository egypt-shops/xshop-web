from django.shortcuts import render, redirect

from xshop.cart.cart import Cart
from xshop.cart.forms import CartPostProductForm


def cart_post(request, product_id):
    cart = Cart(request)
    form = CartPostProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = int(cd["quantity"])
        action = cd["actions"]

    if action == "add":
        product = {"id": product_id}
        cart.add(product=product)
        return redirect("cart: cart_details")

    elif action == "update":
        product = {"id": product_id}
        cart.update(
            product=product,
            quantity=quantity,
        )
        return redirect("cart:cart_details")

    elif action == "remove":
        cart.remove(product_id)
        return redirect("cart: cart_details")

    elif action == "clear":
        cart.clear()
        redirect("cart: cart_details")


def cart_details(request):
    cart = Cart(request)
    full_price = 0
    for item in cart:
        full_price += item["total_price"]
        item["update_quantity_form"] = CartPostProductForm(
            initial={"quantity": item["quantity"], "actions": "update"}
        )
    context = {
        "cart": cart,
        "full_price": full_price,
    }
    return render(request, "pages/cart.html", context)


def cart_delete_item(request):
    cart = Cart(request)
    if request.POST.get("action") == "delete":
        product_id = int(request.POST.get("productid"))
        cart.remove(product_id)

    return redirect("cart:cart_details")
