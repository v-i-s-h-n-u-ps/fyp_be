from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

from projects.models import Project, ProjectCategory, ProjectParticipant, ProjectCount, ProjectTask
from projects.serializers import CreateProjectSerializer, ProjectParticipantSerializer, UpdateProjectDetailsSerializer, \
    ProjectCategorySerializer, ProjectCountSerializer, GetProjectDetailsSerializer, GetProjectSummarySerializer, \
    ManageProjectParticipantSerializer, AddProjectTaskSerializer, UpdateProjectTaskSerializer, GetProjectTaskSerializer
from resources.models import University, Category, Type
from user.models import User
from user.permissions import IsStudent


class ResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CreateProject(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsStudent]
    serializer_class = CreateProjectSerializer

    @swagger_auto_schema(request_body=CreateProjectSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                if not user:
                    return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
                location = University.objects.get(id=data['location'])
                project = Project(user=user, name=data['name'], location=location, startDate=data['startDate'],
                                  endDate=data['endDate'], description=data['description'])
                project.save()
                for cat in data['categories']:
                    category = Category.objects.get(id=cat)
                    category_obj = ProjectCategory(category=category, project=project)
                    category_obj.save()
                created = ProjectParticipant(student=user, project=project, isLeader=True)
                created.save()
                return JsonResponse({'data': project.id}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetProject(APIView):
    permission_classes = [AllowAny]
    serializer_class = GetProjectDetailsSerializer
    category_serializer = ProjectCategorySerializer
    count_serializer = ProjectCountSerializer
    filterset_fields = ['id']

    def get(self, request):
        try:
            id = request.GET.get('id')
            project = Project.objects.get(id=id)
            if not project:
                return JsonResponse({'error': 'Project Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            data = self.serializer_class(project)
            category = ProjectCategory.objects.filter(project=project)
            data_category = self.category_serializer(instance=category, many=True)
            count = ProjectCount.objects.get(project=project)
            data_count = self.count_serializer(instance=count)
            return_obj = data.data | data_count.data
            return_obj['categories'] = data_category.data
            return JsonResponse({"data": return_obj}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetProjectParticipants(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectParticipantSerializer
    filterset_fields = ['id']

    @swagger_auto_schema(responses={200: ProjectParticipantSerializer(many=True)})
    def get(self, request):
        try:
            id = request.GET.get('id')
            project = Project.objects.get(id=id)
            if not project:
                return JsonResponse({'error': 'Project Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            users = ProjectParticipant.objects.filter(project=project)
            data_users = self.participant_serializer(instance=users, many=True)
            return JsonResponse({"data": data_users.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProject(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = UpdateProjectDetailsSerializer

    @swagger_auto_schema(request_body=UpdateProjectDetailsSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                project = Project.objects.get(id=data['id'])
                admin_status = ProjectParticipant.objects.filter(project=project, student=user)[0].isLeader
                location = University.objects.get(id=data['location'])
                if not admin_status:
                    return JsonResponse({'data': 'This is not your project'}, status=status.HTTP_200_OK)
                Project.objects.filter(id=data['id']).update(name=data['name'], location=location,
                                                             startDate=data['startDate'],
                                                             endDate=data['endDate'], description=data['description'])
                ProjectCategory.objects.filter(project=project).delete()
                for cat in data['categories']:
                    category = Category.objects.get(id=cat)
                    category_obj = ProjectCategory(category=category, project=project)
                    category_obj.save()
                return JsonResponse({'data': 'Project updated'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetMyProjects(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = GetProjectSummarySerializer

    @swagger_auto_schema(responses={200: GetProjectSummarySerializer(many=True)})
    def get(self, request):
        try:
            user = request.user
            if not user:
                return JsonResponse({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
            my_projects = ProjectParticipant.filter(student=user).order_by('isLeader')
            return_obj = []
            for proj in my_projects:
                project = Project.objects.get(id=proj.id)
                project_data = self.serializer_class(instance=project)
                return_obj.append(project_data.data)
            return JsonResponse({"data": return_obj}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListProjects(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetProjectSummarySerializer
    pagination_class = ResultsSetPagination
    filterset_fields = ['page']

    @swagger_auto_schema(responses={200: GetProjectSummarySerializer(many=True)})
    def get(self, request):
        try:
            page = request.GET.get('page')
            project = Project.objects.all().order_by('startDate')
            _projects = self.pagination_class(project)
            try:
                project = self.pagination_class.page(page)
            except PageNotAnInteger:
                project = self.pagination_class.page(1)
            except EmptyPage:
                project = self.pagination_class.page(self.pagination_class.num_pages)
            data = self.serializer_class(project, many=True)
            response = self.pagination_class.get_paginated_response(data.data)
            return JsonResponse({"data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class ManageProjectParticipant(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = ManageProjectParticipantSerializer

    @swagger_auto_schema(request_body=ManageProjectParticipantSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                project = Project.objects.filter(id=data['project'], user=user)
                if not project:
                    return JsonResponse({'error': "This is not your project"}, status=status.HTTP_400_BAD_REQUEST)
                _user = User.objects.get(id=data['user'])
                if not _user:
                    return JsonResponse({'error': "User not found"}, status=status.HTTP_400_BAD_REQUEST)
                if data['action'] == 1:
                    participant = ProjectParticipant(project=project, student=_user)
                    participant.save()
                else:
                    ProjectParticipant.objects.filter(project=project, student=_user).delete()
                return JsonResponse({'data': "Users updated"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddProjectTask(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = AddProjectTaskSerializer

    @swagger_auto_schema(request_body=AddProjectTaskSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                project = Project.objects.filter(id=data['project'])
                if not project:
                    return JsonResponse({'error': "This is not your project"}, status=status.HTTP_400_BAD_REQUEST)
                participant = ProjectParticipant.objects.filter(project=project, user=user)
                if not participant:
                    return JsonResponse({'error': "You're not part of this project"}, status=status.HTTP_400_BAD_REQUEST)
                _type = Type.objects.get(name=data['type'])
                task = ProjectTask(task=data['task'], type=_type, project=project, user=user, dueDate=data['dueDate'])
                task.save()
                return JsonResponse({'data': task.id}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProjectTask(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = UpdateProjectTaskSerializer

    @swagger_auto_schema(request_body=UpdateProjectTaskSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                task = ProjectTask.objects.filter(id=data['id'], user=user)
                if not task:
                    return JsonResponse({'error': "This is not your task"}, status=status.HTTP_400_BAD_REQUEST)
                _type = Type.objects.get(name=data['type'])
                task.update(task=data['task'], type=_type, dueDate=data['dueDate'], isComplete=data['isComplete'])
                return JsonResponse({'data': "Updated"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetProjectTask(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = GetProjectTaskSerializer
    pagination_class = ResultsSetPagination
    filterset_fields = ['page', 'project']

    @swagger_auto_schema(responses={200: GetProjectTaskSerializer(many=True)})
    def get(self, request):
        try:
            user = request.user
            id = request.GET.get('project')
            page = request.GET.get('page')
            if not id:
                tasks = ProjectTask.objects.filter(user=user).order_by('dueDate', 'createdAt')
            else:
                project = Project.objects.get(id=id)
                tasks = ProjectTask.objects.filter(user=user, project=project).order_by('dueDate', 'createdAt')
            _projects = self.pagination_class(tasks)
            try:
                tasks = self.pagination_class.page(page)
            except PageNotAnInteger:
                tasks = self.pagination_class.page(1)
            except EmptyPage:
                tasks = self.pagination_class.page(self.pagination_class.num_pages)
            data = self.serializer_class(tasks, many=True)
            response = self.pagination_class.get_paginated_response(data.data)
            return JsonResponse({"data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)
