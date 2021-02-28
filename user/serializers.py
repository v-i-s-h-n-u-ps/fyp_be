from rest_framework import serializers

from user.models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RevokeTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class SignUpSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['name', 'password', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}


class ActivateSerializer(serializers.Serializer):
    name = serializers.EmailField()
    otp = serializers.IntegerField()


class PasswordResetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    old = serializers.CharField()
    new = serializers.CharField()