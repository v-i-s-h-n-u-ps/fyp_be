import uuid

from django.db import models
from django.db.models import Model

from resources.models import Category, Type
from user.models import User


class Forum(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)
    members = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class ForumUser(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.forum.name + "::" + self.user.name


class ForumCategory(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.forum.name + "::" + self.category.name


class Task(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    startDate = models.DateField()
    endDate = models.DateField()
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.task

