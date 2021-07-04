from django.contrib.auth import forms
from phonenumber_field.formfields import PhoneNumberField

from xshop.users.models import User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = (
            "mobile",
            "name",
            "password1",
            "password2",
        )
        field_classes = {"mobile": PhoneNumberField}


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ("mobile",)
        field_classes = {"mobile": PhoneNumberField}


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "mobile",
            "name",
            "password1",
        )

    # def save(self, request):
    #     user = super(SignUpForm, self).save(request)
    #     user.mobile = self.cleaned_data["mobile"]
    #     user.save()
    #     return user
