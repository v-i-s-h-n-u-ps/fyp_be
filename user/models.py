from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(max_length=13)
    last_login = models.DateTimeField(auto_now=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name + ": " + self.email

