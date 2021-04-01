from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from others.models import Task, Forum, ForumCategory, ForumUser
from others.serializers import TaskCreateSerializer, TaskGetSerializer, CreateForumSerializer, GetForumSerializer, \
    UpdateUserOfForumSerializer, UpdateForumSerializer
from resources.models import Category
from user.models import User


class CreateTask(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreateSerializer
    get_serializer_class = TaskGetSerializer

    def get(self, request):
        try:
            user = request.user
            if not user:
                return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            task = Task.objects.filter(user=user)
            data = self.get_serializer_class(task, many=True)
            return JsonResponse({"data": data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                if not user:
                    return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
                task = Task(user=user, task=data['task'], startDate=data['startDate'], endDate=data['endDate'], type=data['type'])
                task.save()
                return JsonResponse({'data': task.id}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateForum(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateForumSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                if not user:
                    return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
                forum = Forum(user=user, name=data['name'], description=data['description'], type=data['type'])
                forum.save()
                for cat in data['categories']:
                    category = Category.objects.get(id=cat)
                    category_obj = ForumCategory(category=category, forum=forum)
                    category_obj.save()
                created = ForumUser(user=user, forum=forum, isAdmin=True)
                created.save()
                return JsonResponse({'data': forum.id}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetForum(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetForumSerializer
    filterset_fields = ['id']

    def get(self, request):
        try:
            id = request.GET.get('id')
            forum = Forum.objects.get(id=id)
            if not forum:
                return JsonResponse({'error': 'Forum Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            data = self.serializer_class(forum)
            forum_users = ForumUser.objects.filter(forum=forum, active=True)
            members = []
            for user in forum_users:
                user_details = user.user_details
                members.append(user_details)
            data.data["members"] = members
            return JsonResponse({"data": data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetForumsUserIsPartOf(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetForumSerializer

    def get(self, request):
        try:
            user = request.user
            if not user:
                return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            forums = ForumUser.objects.filter(user=user, active=True).forum_details
            data = self.get_serializer_class(forums, many=True)
            for forum in data:
                forum["isAdmin"] = ForumUser.objects.get(user=user, forum=forum).isAdmin
            return JsonResponse({"data": data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUsersOfForum(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserOfForumSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                forum = Forum.objects.get(id=data['forum'])
                act_user = User.objects.get(id=data['id'])
                if not forum or not act_user:
                    return JsonResponse({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
                if not user:
                    return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
                request_user_role = ForumUser.objects.filter(user=user, forum=forum)[0].isAdmin
                if not request_user_role:
                    return JsonResponse({'error': 'Cannot save action. User is not an admin.'}, status=status.HTTP_400_BAD_REQUEST)
                if data['type'] == 1:
                    forum.members += 1
                    forum.save()
                    obj, created = ForumUser.objects.update_or_create(user=act_user, forum=forum)
                else:
                    forum.member -= 1
                    forum.save()
                    ForumUser.objects.filter(user=act_user, forum=forum).update(active=False, isAdmin=False)
                return JsonResponse({'data': 'User added'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateForum(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class= UpdateForumSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                forum = Forum.objects.get(id=data['id'])
                admin_status = ForumUser.objects.filter(forum=forum, user=user)[0].isAdmin
                if not admin_status:
                    return JsonResponse({'data': 'User is not an admin'}, status=status.HTTP_200_OK)
                Forum.objects.filter(id=data['id']).update(name=data['name'], description=data['description'], type=data['type'])
                ForumCategory.objects.filter(forum=forum).delete()
                for cat in data['categories']:
                    category = Category.objects.get(id=cat)
                    category_obj = ForumCategory(category=category, forum=forum)
                    category_obj.save()
                return JsonResponse({'data': 'User added'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)
