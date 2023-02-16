from rest_framework import serializers
from .models import Roles


class Roles_Serializers(serializers.Serializer):
    role_name = serializers.CharField(max_length=250)
