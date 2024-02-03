from django.db import models
from django.contrib.auth.models import User


class ResourceType(models.Model):
    name = models.CharField(max_length=256)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
