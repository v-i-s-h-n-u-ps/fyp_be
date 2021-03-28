import uuid

from django.db import models
from django.db.models import Model

from resources.models import University, Category, Type
from user.models import User


class Project(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    isComplete = models.BooleanField(default=False)
    isDeferred = models.BooleanField(default=False)
    description = models.TextField()
    members = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class ProjectCategory(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.name + " :: " + self.category.name

    @property
    def category_name(self):
        return self.category.name


class ProjectParticipant(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    isLeader = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.name + " :: " + self.student.user.name

    @property
    def name(self):
        return self.student.name

    @property
    def avatar(self):
        return self.student.avatar


class ProjectTask(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dueDate = models.DateField()
    isComplete = models.BooleanField(default=False)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task


class ProjectCount(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    trending_score = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)

    def __str__(self):
        return self.project.name

