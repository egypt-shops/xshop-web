from django import forms

PAYING_METHODS_CHOICES = [
    ("cash on delivery", "cash on delivery"),
    ("credit card", "credit card"),
]


class CheckOutForm(forms.Form):
    address = forms.CharField(required=True)
    paying_method = forms.TypedChoiceField(choices=PAYING_METHODS_CHOICES)
