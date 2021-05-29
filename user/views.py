import random

import requests
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fyp_be.settings import EMAIL_HOST_USER, BASE_DIR, CLIENT_ID, CLIENT_SECRET, BASE_URL
from resources.models import Role, University, Category
from user.models import User, OTP, UserRole, Student, StudentCategory
from user.permissions import IsStudent
from user.serializers import LoginSerializer, UserSerializer, RefreshTokenSerializer, RevokeTokenSerializer, \
    SignUpSerializer, ActivateSerializer, PasswordResetTokenSerializer, PasswordResetSerializer, \
    PasswordChangeSerializer, UserRoleSerializer, StudentGetSerializer, CreateStudentSerializer, \
    StudentCategoryGetSerializer, UpdateStudentSerializer, UpdateUserSerializer


def send_confirmation_email(subject, content, file):
    try:
        body = render_to_string(BASE_DIR + '/templates/' + file + '.html', content)
        send_mail(subject, '', EMAIL_HOST_USER, content['email'], html_message=body, fail_silently=False)
    except Exception as e:
        print(repr(e))


def generateOTP(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return random.randint(lower, upper)


class UserDetails(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = UserSerializer
    role_serialzer = UserRoleSerializer
    student_serializer = StudentGetSerializer
    student_category_serializer = StudentCategoryGetSerializer

    @swagger_auto_schema(response={status.HTTP_200_OK, UserSerializer})
    def get(self, request):
        try:
            user = request.user
            if not user:
                return Response({'error': "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            data = self.serializer_class(user)
            roles_set = UserRole.objects.filter(user=user)
            roles = self.role_serialzer(roles_set, many=True)
            student = Student.objects.filter(user=user)
            response = {}
            response["user_info"] = data.data
            response["user_info"]["roles"] = roles.data
            if not student:
                response["student"] = {}
            else:
                response["student"] = self.student_serializer(student[0]).data
                student_category = StudentCategory.objects.filter(student=student[0])
                categories = self.student_category_serializer(student_category, many=True)
                response["student"]["categories"] = categories.data
            return Response({"data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    @swagger_auto_schema(response={status.HTTP_200_OK, serializer_class})
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                User.objects.filter(id=user.id).update(avatar=data['avatar'], name=data['name'])
                return Response({"data": "Updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


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
                _user = User.objects.filter(email=data['email'])
                if not _user.exists():
                    return Response({"error": {"message": "User not found"}}, status=status.HTTP_404_NOT_FOUND)
                user_not_active = User.objects.filter(email=data['email'], is_active=0)
                if user_not_active.exists():
                    otp = generateOTP(6)
                    OTP.objects.create(user=user_not_active[0], otp=otp, type="signup")
                    subject = "Verify your email"
                    content = {
                        'email': [user_not_active[0].email],
                        'otp': otp,
                        'name': user_not_active[0].name
                    }
                    send_confirmation_email(subject, content, 'confirm_registration_email')
                    return Response({"data": {"message": "Otp sent"}, "code": "USER_NOT_ACTIVE"},
                                    status=status.HTTP_206_PARTIAL_CONTENT)
                user = User.objects.filter(email=data['email'], is_active=1)
                res = requests.post(
                    BASE_URL + 'o/token/',
                    data={
                        'grant_type': 'password',
                        'username': data['email'],  # username for oauth is the login we have.
                        'password': data['password'],
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET,
                    },
                )
                if res.status_code == status.HTTP_200_OK:
                    user.update(last_login=timezone.now())
                    return_data = res.json()
                    return Response({"data": return_data}, status=res.status_code)
                else:
                    return Response(res.json(), status=res.status_code)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
                    BASE_URL + 'o/token/',
                    data={
                        'grant_type': 'refresh_token',
                        'refresh_token': data['refresh_token'],
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET,
                    }
                )
                return Response({"data": res.json()}, status=res.status_code)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
                    BASE_URL + 'o/revoke_token/',
                    data={
                        'token': data['token'],
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET,
                    }
                )
                return Response({"data": {"message": "Token Revoked"}}, status=res.status_code)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                role = Role.objects.get(name=data['role'])
                if not role:
                    return JsonResponse({"error": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)
                custom_user = User(email=data['email'], password=make_password(data['password']),
                                   name=data['name'])
                custom_user.save()
                user_role = UserRole(user=custom_user, role=role)
                user_role.save()
                otp = generateOTP(6)
                OTP.objects.create(user=custom_user, otp=otp, type="signup")
                subject = "Welcome to Auxiliar"
                content = {
                    'email': [custom_user.email],
                    'otp': otp,
                    'name': custom_user.name
                }
                send_confirmation_email(subject, content, 'confirm_registration_email')
                return JsonResponse({"user": custom_user.pk, "message": "Registered successfully"},
                                    status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    permission_classes = [AllowAny]
    serializer_class = ActivateSerializer

    @swagger_auto_schema(request_body=ActivateSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = User.objects.filter(email=data['email'])
                if not user.exists():
                    return Response({"message": "Email id not registered."}, status=status.HTTP_404_NOT_FOUND)
                else:
                    otp_obj = OTP.objects.filter(user=user[0], otp=data['otp'])
                    if not otp_obj.exists():
                        return Response({"message": "Invalid otp."}, status=status.HTTP_400_BAD_REQUEST)
                    _type = otp_obj[0].type
                    otp_obj.delete()
                    user.update(is_active=1)
                    return Response({'message': _type}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
                subject = "Reset your password"
                content = {
                    'email': [user[0].email],
                    'name': user[0].name,
                    'otp': otp
                }
                send_confirmation_email(subject, content, 'reset_password_email')
                return JsonResponse({"data": "Reset your password"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
                users = User.objects.filter(email=data['email'])
                if not users.exists():
                    return Response({"message": "Email id not registered."}, status=status.HTTP_404_NOT_FOUND)
                user = users[0]
                otp_obj = OTP.objects.filter(user=user, otp=data['otp'])
                if not otp_obj.exists():
                    return Response({"message": "Invalid otp."}, status=status.HTTP_400_BAD_REQUEST)
                otp_obj.delete()
                users.update(is_active=1)
                OTP.objects.filter(user=user).delete()
                user.set_password(data['password'])
                user.save()
                return JsonResponse({"message": 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateStudent(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CreateStudentSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                university = University.objects.get(id=data['university'])
                student = Student(user=user, university=university, dateOfBirth=data['dateOfBirth'],
                                  about=data['about'],
                                  facebook=data['facebook'], resumeUrl=data['resumeUrl'], linkedIn=data['linkedIn'],
                                  gender=data['gender'], gmail=data['gmail'], twitter=data['twitter'])
                student.save()
                for cat in data['categories']:
                    category = Category.objects.get(id=cat)
                    category_obj = StudentCategory(category=category, student=student)
                    category_obj.save()
                return JsonResponse({"message": 'Details saved successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateStudent(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = UpdateStudentSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = request.user
                university = University.objects.get(id=data['university'])
                student = Student.objects.filter(id=data['id'])
                student.update(user=user, university=university,
                               dateOfBirth=data['dateOfBirth'],
                               about=data['about'], twitter=data['twitter'],
                               facebook=data['facebook'],
                               resumeUrl=data['resumeUrl'],
                               linkedIn=data['linkedIn'],
                               gender=data['gender'], gmail=data['gmail'])
                StudentCategory.objects.filter(student=student[0]).delete()
                for cat in data['categories']:
                    print("dfdf", cat)

                    category = Category.objects.get(id=cat)
                    print("dfdf")
                    category_obj = StudentCategory(category=category, student=student[0])
                    print("dfdf")

                    category_obj.save()
                return JsonResponse({"message": 'Details saved successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class Resend(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetTokenSerializer

    @swagger_auto_schema(query_serializer=serializer_class)
    def get(self, request):
        try:
            serializer = self.serializer_class(data=request.query_params)
            if serializer.is_valid():
                data = serializer.data
                user = User.objects.filter(email=data['email'])
                if not user.exists():
                    return Response({"message": "Email id not registered."}, status=status.HTTP_404_NOT_FOUND)
                _otp = OTP.objects.filter(email=data['email'])
                if not _otp.exists():
                    otp = generateOTP(6)
                    OTP.objects.create(user=user[0], otp=otp, type="signup")
                else:
                    otp = _otp[0].otp
                subject = "Welcome to Auxiliar"
                content = {
                    'email': [user[0].email],
                    'otp': otp,
                    'name': user[0].name
                }
                send_confirmation_email(subject, content, 'confirm_registration_email')
                return JsonResponse({"data": "Reset your password"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)


class SearchUsers(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request):
        print("heree")
        try:
            search = request.GET.get('search')
            print(search)
            if len(search) > 1:
                users = User.objects.filter(Q(name__contains=search) | Q(email__contains=search))
                data = self.serializer_class(users, many=True)
                return JsonResponse({"data": data.data}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"data": {}}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)
