from rest_framework import serializers


class Serializer(serializers.Serializer):
    role = serializers.UUIDField()
    accessPage = serializers.UUIDField()
