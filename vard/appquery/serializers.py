from .models import DataBaseQuery
from rest_framework import serializers


class DataBaseQuerySerializer(serializers.Serializer):
   id = serializers.IntegerField()
   email = serializers.CharField(max_length=255)