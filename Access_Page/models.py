from uuid import uuid4
from django.db import models
from Roles.models import Roles


class AccessPage(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    page = models.CharField(max_length=1000, null=False)
    method = models.CharField(max_length=1000, null=False)

