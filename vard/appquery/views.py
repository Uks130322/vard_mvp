from django.shortcuts import render
from rest_framework import views
from rest_framework import permissions
import django_filters
from .serializers import DataBaseQuerySerializer
#from .dbqueries import DataBaseQuery
from .models import DataBaseQuery
from rest_framework.response import Response


class DBView(views.APIView):
   def get(self, request):
      #a = DataBaseQuery('mysql', 'root', 'P@r0l', '', 'localhost', '', 'baza_test1', '', '','SELECT id,email FROM vardapp_users')
      datas = DataBaseQuery('mysql', 'root', 'P@r0l', '', 'localhost', '', 'baza_test1', '', '','SELECT * FROM vardapp_users').get_query
      #datas = [{"id": 10, "email": "0"}, {"id": 4, "email": "23"}]
      results = DataBaseQuerySerializer(datas, many=True).data
      return Response(datas)





