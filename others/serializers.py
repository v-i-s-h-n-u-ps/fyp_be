from rest_framework import serializers

from others.models import Task, Forum, ForumCategory


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task', 'startDate', 'endDate', 'type']


class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CreateForumSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())

    class Meta:
        model = Forum
        fields = ['name', 'description', 'type', 'categories']


class GetForumSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField()
    avatar = serializers.ReadOnlyField()

    class Meta:
        model = Forum
        fields = '__all__'
        extra_fields = ['user_name', 'avatar']


class UpdateForumSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())
    id = serializers.UUIDField()

    class Meta:
        model = Forum
        fields = ['id', 'name', 'description', 'type', 'categories']


class UpdateUserOfForumSerializer(serializers.Serializer):
    forum = serializers.UUIDField()
    user = serializers.UUIDField()
    type = serializers.IntegerField(help_text="1: add/0: remove")


class ForumCategorySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        model = ForumCategory
        exclude = ['forum']
        extra_fields = ['name']
