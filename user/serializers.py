from rest_framework import serializers

from user.models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserRoleSerializer(serializers.ModelSerializer):
    roleName = serializers.ReadOnlyField()

    class Meta:
        model = UserRole
        fields = '__all__'
        extra_fields = ['roleName']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'avatar']


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
    email = serializers.EmailField()
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


class StudentGetSerializer(serializers.ModelSerializer):
    universityDetails = serializers.ReadOnlyField()

    class Meta:
        model = Student
        exclude = ['university']
        extra_fields = ['universityDetails']


class CreateStudentSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())

    class Meta:
        model = Student
        exclude = ['id', 'createdAt', 'user']
        extra_fields = ['categories']


class UpdateStudentSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())
    id = serializers.UUIDField()

    class Meta:
        model = Student
        exclude = ['createdAt', 'user']
        extra_fields = ['id', 'categories']


class StudentCategoryGetSerializer(serializers.ModelSerializer):
    categoryName = serializers.ReadOnlyField()

    class Meta:
        model = StudentCategory
        fields = ['id', 'category', 'categoryName']


class UpdateUserSerializer(serializers.Serializer):
    avatar = serializers.CharField()
    name = serializers.CharField()
