from rest_framework import serializers

from resources.models import University, Role, Type, Category



class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
<<<<<<< HEAD
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
=======
        fields = ['id', 'name', 'longitude', 'latitude', 'createAt', 'location']
>>>>>>> 2e6d9df4953781042726c228ed3fa5de846d3db7
