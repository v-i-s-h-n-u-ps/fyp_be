from rest_framework import serializers

from projects.models import Project, ProjectParticipant, ProjectCount, ProjectTask, ProjectCategory
from user.models import User


class CreateProjectSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())

    class Meta:
        model = Project
        fields = ['name', 'location', 'startDate', 'endDate', 'description', 'categories']


class UpdateProjectDetailsSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.UUIDField())
    id = serializers.UUIDField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'location', 'startDate', 'endDate', 'description', 'categories', 'isComplete']


class ProjectParticipantSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    avatar = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    userId = serializers.ReadOnlyField()

    class Meta:
        model = ProjectParticipant
        fields = ['id', 'name', 'avatar', 'isLeader', 'createdAt', 'email', 'userId']


class ProjectCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField()

    class Meta:
        model = ProjectCategory
        fields = ['id', 'category_name', 'createdAt', 'category']


class ProjectCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCount
        fields = '__all__'


class GetProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        ordering = ['startDate']


class GetProjectSummarySerializer(serializers.ModelSerializer):
    createdBy = serializers.ReadOnlyField()
    avatar = serializers.ReadOnlyField()
    created_id = serializers.ReadOnlyField()
    university = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'createdBy', 'avatar', 'startDate', 'endDate', 'description', 'isComplete', 'isDeferred',
                  'created_id', 'university', 'email']


class ManageProjectParticipantSerializer(serializers.Serializer):
    project = serializers.UUIDField()
    user = serializers.UUIDField()
    action = serializers.IntegerField(help_text="1: add/ 0: remove")


class IdSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class AddProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = ['task', 'project', 'dueDate', 'type']


class UpdateProjectTaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = ProjectTask
        fields = ['id', 'task', 'type', 'dueDate', 'isComplete']


class GetProjectTaskSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()

    class Meta:
        model = ProjectTask
        fields = '__all__'
        extra_fields = ['type_name', 'username']

