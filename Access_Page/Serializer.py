from rest_framework import serializers


class Serializer(serializers.Serializer):
    page = serializers.CharField(max_length=1000)
    method = serializers.CharField(max_length=1000)
