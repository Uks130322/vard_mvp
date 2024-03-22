from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework import permissions
import django_filters
from .models import DataBaseQuery
from rest_framework.response import Response
from rest_framework.decorators import api_view



class DBView(views.APIView):
   def get(self, request):
      object = DataBaseQuery(1, 'mysql', 'root', 'P@r0l', '', 'localhost', '', 'baza_test1', '', '', '') #SELECT * FROM vardapp_users
      datas = object.get_responces
      return Response(datas)

   def post(self, request):
      networks = request.body.decode('ISO-8859-1')
      object = DataBaseQuery(1, 'mysql', 'root', 'P@r0l', '', 'localhost', '', 'baza_test1', '', '', networks) #SELECT * FROM vardapp_users where id=1
      datas = object.get_responces
      return Response(datas)

   @classmethod
   def get_extra_actions(cls):
      return []

#https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/views
#https://proproprogs.ru/django/drf-bazovyy-klass-apiview-dlya-predstavleniy


