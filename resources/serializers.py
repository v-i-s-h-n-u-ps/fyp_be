from rest_framework import serializers

from resources.models import University, Role, Type, Category



class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['name', 'id', 'longitude', 'latitude', 'createAt', 'location']


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name']


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
