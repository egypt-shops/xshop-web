from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile', 'password' )

class LoginSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=25)

    class Meta:
        model = User
        fields = ['mobile','password']

    def validate(self, attrs):
        mobile = attrs.get('mobile', '')
        passward = attrs.get('password', '')

        user = auth.authenticate(mobile=mobile, password=password)
        if not user.is_active:
            raise AuthenticationFailed('Inactive account')
        if not user.is_verified:
            raise AuthenticationFailed('unverified account')
        if not user:
            raise AuthenticationFailed('Invaled mobile or password, please try again')
        
        return {
            'name' : user.name,
        }

        return super().validate(attrs)