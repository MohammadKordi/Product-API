from django_regex.validators import RegexValidator
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=250, allow_null=False)
    last_name = serializers.CharField(max_length=250, allow_null=False)
    mobile = serializers.CharField(max_length=11, allow_null=False)
    username = serializers.CharField(max_length=125, allow_null=False)
    password = serializers.CharField()
    email = serializers.EmailField()
