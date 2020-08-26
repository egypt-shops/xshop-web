from django.contrib.auth import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("mobile",)
        field_classes = {"mobile": PhoneNumberField}


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ("mobile",)
        field_classes = {"mobile": PhoneNumberField}
