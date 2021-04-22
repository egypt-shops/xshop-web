from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartPostProductForm(forms.Form):
    quantity = forms.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
    actions = forms.CharField(required=False, initial="add", widget=forms.HiddenInput)
