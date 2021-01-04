import uuid

from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from resources.models import Role
from user.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def __str__(self):
        return self.user.id


class UserRoles(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)