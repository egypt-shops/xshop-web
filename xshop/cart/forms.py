from django import forms

from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer


class CartPostProductForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"class": "form-control-lg", "id": "quantity_input"}
        )
    )
    actions = forms.CharField(required=False, initial="add", widget=forms.HiddenInput)
    product_id = forms.IntegerField(required=True, widget=forms.HiddenInput)

    def clean(self):
        attrs = super().clean()
        quantity = attrs.get("quantity")
        action = attrs.get("actions")
        product_id = attrs.get("product_id")

        if action == "clear":
            return attrs

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise forms.ValidationError({"product_id": "Not found"})
        if action == "update" and quantity is None:
            raise forms.ValidationError({"quantity": "invalid, must provide quantity"})
        if action == "update" and product.stock < quantity:
            raise forms.ValidationError(
                {"quantity": f"Invalid. available stock {product.stock}"}
            )

        attrs["product"] = ProductSerializer(product).data
        return attrs
