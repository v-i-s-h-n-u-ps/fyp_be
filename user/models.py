import uuid

from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from resources.models import Role, University, Category
from user.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.TextField(default="")
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
        return str(self.user.id)


class UserRole(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + "::" + self.role.name


class Student(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    dateOfBirth = models.DateTimeField()
    gender = models.CharField(max_length=10)
    activeProjects = models.PositiveIntegerField(default=0)
    about = models.TextField()
    facebook = models.TextField()
    resumeUrl = models.TextField()
    linkedIn = models.TextField()
    gmail = models.TextField()

    def __str__(self):
        return self.user.name + "" + self.university.name


class StudentCategory(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.student.user.name + "::" + self.category.name
