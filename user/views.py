import requests
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from fyp_be import settings
from user.serializers import *


class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    user_serializer = UserSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                data = serializer.data
                user = User.objects.filter(email=data['email'], is_active=1)
                if not user.exists():
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                res = requests.post(
                    settings.BASE_URL + 'o/token/',
                    data={
                        'grant_type': 'password',
                        'username': data['email'],  # username for oauth is the login we have.
                        'password': data['password'],
                        'client_id': settings.CLIENT_ID,
                        'client_secret': settings.CLIENT_SECRET,
                    }
                )
                if res.status_code == status.HTTP_200_OK:
                    user.update(last_login=timezone.now())
                    user_data = self.user_serializer(user[0]).data
                    return_data = res.json()
                    return_data['user_info'] = user_data
                    return Response(return_data, status=res.status_code)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                res = requests.post(
                    settings.BASE_URL + 'o/token/',
                    data={
                        'grant_type': 'refresh_token',
                        'refresh_token': data['refresh_token'],
                        'client_id': settings.CLIENT_ID,
                        'client_secret': settings.CLIENT_SECRET,
                    }
                )
                return Response(res.json(), status=res.status_code)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class RevokeToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = RevokeTokenSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                res = requests.post(
                    settings.BASE_URL + 'o/revoke_token/',
                    data={
                        'token': data['token'],
                        'client_id': settings.CLIENT_ID,
                        'client_secret': settings.CLIENT_SECRET,
                    }
                )
                return Response({"message": "Token Revoked"}, status=res.status_code)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                custom_user = User(email=data['email'], password=make_password(data['password']),
                                   name=data['name'])
                custom_user.save()
                return JsonResponse({"user": custom_user.pk}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)
