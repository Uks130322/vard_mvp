from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from appquery import views



app_name = "appquery"
urlpatterns = [
    path('db/', views.DBView.as_view(), name="appquery1"),
]



