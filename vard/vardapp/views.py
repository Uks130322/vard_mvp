from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework import permissions
import django_filters
from .models import Users
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import UserSerializer
import json
import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins

class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]