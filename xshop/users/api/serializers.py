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


class TokenUserSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    email = serializers.CharField()
    type = serializers.ListField()


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = TokenUserSerializer()


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["mobile", "name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = User(
            mobile=self.validated_data["mobile"],
            name=self.validated_data["name"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user
