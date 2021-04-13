import random

import requests
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fyp_be import settings
from resources.models import Role
from user.models import User, OTP, UserRole
from user.permissions import IsStudent
from user.serializers import LoginSerializer, UserSerializer, RefreshTokenSerializer, RevokeTokenSerializer, \
    SignUpSerializer, ActivateSerializer, PasswordResetTokenSerializer, PasswordResetSerializer, \
    PasswordChangeSerializer


def generateOTP(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return random.randint(lower, upper)


class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    user_serializer = UserSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
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
                else:
                    return Response(res.json(), status=res.status_code)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
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

    @swagger_auto_schema(request_body=RevokeTokenSerializer)
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

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            print(serializer)
            if serializer.is_valid():
                data = serializer.data
                custom_user = User(email=data['email'], password=make_password(data['password']),
                                   name=data['name'])
                role = Role.objects.get(name=data['role'])
                custom_user.save()
                user_role = UserRole(user=custom_user, role=role)
                print(custom_user, role)
                user_role.save()
                return JsonResponse({"user": custom_user.pk, "message": "Registered successfully"}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    permission_classes = [AllowAny]
    serializer_class = ActivateSerializer

    @swagger_auto_schema(request_body=ActivateSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.query_params)
            if serializer.is_valid():
                data = serializer.data
                user = User.objects.filter(email=data['email'])
                if not user.exists():
                    return Response({"message": "Email id not registered."}, status=status.HTTP_404_NOT_FOUND)
                else:
                    otp_obj = OTP.objects.filter(user=user[0], otp=data['otp'])
                    if not otp_obj.exists():
                        return Response({"message": "Invalid otp."}, status=status.HTTP_400_BAD_REQUEST)
                    otp_obj.delete()
                    user.update(is_active=1)
                    return Response({'message': otp_obj[0].type}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetTokenSerializer

    @swagger_auto_schema(query_serializer=PasswordResetTokenSerializer)
    def get(self, request):
        try:
            serializer = self.serializer_class(data=request.query_params)
            if serializer.is_valid():
                data = serializer.data
                user = User.objects.filter(email=data['email'])
                if not user.exists():
                    return Response({"message": "Email id not registered."}, status=status.HTTP_404_NOT_FOUND)
                otp = generateOTP(6)
                OTP.objects.create(user=user[0], otp=otp, type="reset password")
                return JsonResponse({"data": "Reset your password"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                users = User.objects.filter(email=data['email'], is_active=1)
                if not users.exists():
                    return Response({"message": "Email id not registered."}, status=status.HTTP_404_NOT_FOUND)
                user = users[0]
                otp_obj = OTP.objects.filter(user=user, otp=data['otp'])
                if not otp_obj.exists():
                    return Response({"message": "Invalid otp."}, status=status.HTTP_400_BAD_REQUEST)
                otp_obj.delete()
                user.set_password(data['password'])
                user.save()
                return JsonResponse({"message": 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = PasswordChangeSerializer

    @swagger_auto_schema(request_body=PasswordChangeSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                if not user.check_password(data['old']):
                    return Response({"message": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(data['new'])
                user.save()
                return JsonResponse({"message": 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)

