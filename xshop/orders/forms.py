from django import forms

PAYING_METHODS_CHOICES = [
    ("CASH_ON_DELIVERY", "Cash on Delivery"),
    ("CREDIT_CARD", "Credit Card"),
]


class CheckOutForm(forms.Form):
    address = forms.CharField(required=True)
    paying_method = forms.TypedChoiceField(choices=PAYING_METHODS_CHOICES)
