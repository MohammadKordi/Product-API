from uuid import uuid4
from django.db import models


# Create your models here.

class Roles(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    role_name = models.CharField(max_length=250, null=False, unique=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True)
    datetime_updated = models.DateTimeField(auto_now=True, null=True)
