from rest_framework import serializers

from others.models import Task, Forum


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task', 'startDate', 'endDate', 'type']


class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = 'all'


class CreateForumSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())

    class Meta:
        model = Forum
        fields = ['name', 'description', 'type', 'categories']


class GetForumSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField()

    class Meta:
        model = Forum
        fields = ['all', 'user_name']


class UpdateForumSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())

    class Meta:
        model = Forum
        fields = ['id', 'name', 'description', 'type', 'categories']


class UpdateUserOfForumSerializer(serializers.Serializer):
    forum = serializers.UUIDField()
    user = serializers.UUIDField()
    type = serializers.CharField(help_text="1: add/0: remove")
