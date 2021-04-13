from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

# Create your views here.
from resources.models import University, Role, Type, Category
from resources.serializers import UniversitySerializer, RoleSerializer, TypeSerializer, CategorySerializer


class GetUniversity(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UniversitySerializer

    @swagger_auto_schema(responses={200: UniversitySerializer(many=True)})
    def get(self, request):
        try:
            universities = University.objects.all()
            data = self.serializer_class(universities, many=True)
            return JsonResponse({"data": data.data} , status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetRole(APIView):
    permission_classes = [AllowAny]
    serializer_class = RoleSerializer

    @swagger_auto_schema(responses={200: RoleSerializer(many=True)})
    def get(self, request):
        try:
            role = Role.objects.all()
            data = self.serializer_class(role, many=True)
            return JsonResponse({"data": data.data} , status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetType(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TypeSerializer

    @swagger_auto_schema(responses={200: TypeSerializer(many=True)})
    def get(self, request):
        try:
            types = Type.objects.all()
            data = self.serializer_class(types, many=True)
            return JsonResponse({"data": data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetCategory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request):
        try:
            category = Category.objects.all()
            data = self.serializer_class(category, many=True)
            return JsonResponse({"data": data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)
