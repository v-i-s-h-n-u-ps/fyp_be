import uuid

from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from resources.models import Role, University, Category
from resources.serializers import UniversitySerializer
from user.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.TextField(default="https://fyp-images-narvitaa.s3.ap-south-1.amazonaws.com/default_avatar.png")
    name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.IntegerField(default=0, help_text="0: inactive, 1: active, 2: disabled")
    last_login = models.DateTimeField(auto_now=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class OTP(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    type = models.CharField(default="activate user", help_text="activate user, reset password", max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + " " + self.user.email


class UserRole(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + "::" + self.role.name

    @property
    def roleName(self):
        return self.role.name


class Student(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=10)
    activeProjects = models.PositiveIntegerField(default=0)
    about = models.TextField()
    facebook = models.TextField(null=True, blank=True)
    resumeUrl = models.TextField()
    linkedIn = models.TextField(null=True, blank=True)
    gmail = models.TextField(null=True, blank=True)
    twitter = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.name + "" + self.university.name

    @property
    def universityDetails(self):
        return UniversitySerializer(self.university).data


class StudentCategory(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.student.user.name + "::" + self.category.name

    @property
    def categoryName(self):
        return self.category.name
