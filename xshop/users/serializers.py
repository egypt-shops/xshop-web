from rest_framework import serializers
from rest_framework.authtoken.models import Token
from phonenumber_field.serializerfields import PhoneNumberField

from .models import User


class LoginSerializer(serializers.Serializer):
    mobile = PhoneNumberField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(mobile=attrs.get("mobile"))
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"mobile": "user with this mobile does not exist"}
            )

        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "Invalid"})

        token_obj, _ = Token.objects.get_or_create(user=user)
        attrs["token"] = token_obj.key

        return attrs
