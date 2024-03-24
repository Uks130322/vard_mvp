from .models import Users
from rest_framework import serializers
from django.contrib.auth.models import User
import json
import datetime

class UserSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Users
       fields = ['name','email','date_creation','date_password_change','password','is_staff','is_superuser']

