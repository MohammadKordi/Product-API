from uuid import uuid4
from Roles.models import Roles
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    mobile = models.CharField(max_length=11)
    username = models.CharField(editable=True, unique=True, max_length=125)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'username'
