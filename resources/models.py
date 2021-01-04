from django.db import models
from django.db.models import Model


class Role(Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
