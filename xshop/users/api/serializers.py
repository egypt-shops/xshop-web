from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import User


class TokenApiSerializer(serializers.Serializer):
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
        attrs["name"] = user.name
        attrs["mobile"] = str(user.mobile)
        attrs["email"] = user.email
        attrs["type"] = user.type
        return attrs


class UserSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    email = serializers.CharField()
    type = serializers.ListField()


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()
