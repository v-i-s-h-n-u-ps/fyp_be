from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
from resources.models import University
from resources.serializers import UniversitySerializer


class GetUniversity(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UniversitySerializer

    def get(self, request):
        try:
            universities = University.objects.all()
            print(universities)
            data = self.serializer_class(universities, many=True)
            return JsonResponse({"data": data} , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)