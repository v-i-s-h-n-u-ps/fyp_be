from rest_framework import serializers

from others.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task', 'startDate', 'endDate', 'type']


class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = 'all'


