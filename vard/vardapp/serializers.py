from .models import User
from rest_framework import serializers
from django.contrib.auth.models import User
import json
import datetime

class UserSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = User
       fields = ['name', 'email', 'date_creation', 'date_password_change', 'password', 'is_staff',
                 'is_superuser']

