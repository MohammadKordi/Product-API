from uuid import uuid4
from django.db import models
from Roles.models import Roles
from Access_Page.models import AccessPage


class Access_Page_Role(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True)
    AccessPage = models.ForeignKey(AccessPage, on_delete=models.CASCADE, null=True)
