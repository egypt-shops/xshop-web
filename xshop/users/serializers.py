from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField


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

        attrs["token"] = user.auth_token.key
        return attrs
