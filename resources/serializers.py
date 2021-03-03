from rest_framework import serializers

from resources.models import University

class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = ['name', 'id', 'longitude', 'latitude', 'createAt', 'location']