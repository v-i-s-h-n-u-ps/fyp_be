import uuid

from django.db import models
from django.db.models import Model


class Role(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Type(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name


class University(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=350)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



