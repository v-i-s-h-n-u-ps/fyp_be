from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from others.models import Task
from others.serializers import TaskCreateSerializer, TaskGetSerializer


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