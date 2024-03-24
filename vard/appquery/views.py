from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework import permissions
import django_filters
from .models import DataBaseQuery, ClientDB
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import ClientSerializer #,ClientDBSerializer, UserSerializer
from vardapp.models import Users
import json
import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins

class ClientViewset(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = ClientDB.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        L=[]
        old_response_data = super(ClientViewset, self).list(request, *args, **kwargs)
        client_connect = ClientDB.objects.all()
        for i,j in zip(client_connect, old_response_data.data):
            result = i.update_responce(i.id)
            j['result_query'] = result
            L.append(j)
        new_response_data = L
        return Response(new_response_data)

    def retrieve(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        queryset = ClientDB.objects.all()
        result = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(result, context=serializer_context)
        client_query = result.update_responce(pk)
        dict_result = serializer.data
        dict_result['result_query'] = client_query
        return Response(dict_result)

    def perform_create(self, serializer):
        print('self.request',self.request.data['user'][32:][:-1])
        user = get_object_or_404(Users, id=self.request.data['user'][32:][:-1])
        print('!!!!!!!костыль!!!!!!user',user)
        return serializer.save(user=user)

    #
    # def update(self, request, pk=None):
    #     pass
    #
    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

#
# class ClientDBListAPIView(generics.ListAPIView):
#     queryset = ClientDB.objects.all().values_list('str_query','id')
#     serializer_class = UserSerializer  #ClientDBSerializer
#     lookup_field = 'user__id'
#     lookup_url_kwarg = 'user'
#
#     def get_queryset(self):
#         username = self.request.user
#         user = Users.objects.get(email = username)
#         ids = ClientDB.objects.get(user__email = username)
#         client_connect = ClientDB.objects.get(user__email = username) #user__email = username
#         return super().get_queryset().filter(user__email=username).values('str_query','id')
#
#     def list(self, request, *args, **kwargs):
#         username = self.request.user
#         client_connect = ClientDB.objects.get(id=1)
#         result = client_connect.update_responce()
#         return Response(result)
#
#
# #from appquery.models import *
# #u1 = Users.objects.get(id = 1)
# #d1 = ClientDB.objects.create(user=u1,user_name = 'root', password = 'P@r0l', driver = 1, url = None, host = 'localhost', port = None, data_base_type = None, data_base_name = 'baza_test1', description = None, str_query = 'SELECT * FROM vardapp_users')
# #d1.save()
# #d1 = ClientDB.objects.get(id = 1)
# #d1.get_responces
# #
# #
#
# class DBView(views.APIView):
#    def get(self, request):
#       object = DataBaseQuery(None, 'mysql', 'root', 'P@r0l', '', 'localhost', '', 'baza_test1', '', '', '') #SELECT * FROM vardapp_users
#       datas = object.get_responces
#       return Response(datas)
#
#    def post(self, request):
#       try:
#          query_body = request.body.decode('UTF-8')
#          query = eval(query_body.replace("null", "None"))
#          object = DataBaseQuery(query.get("user_id"), query.get("driver"), query.get("user_name"),
#                                 query.get("password"), query.get("url"), query.get("host"),
#                                 query.get("port"), query.get("data_base_name"), query.get("data_base_type"),
#                                 query.get("description"), query.get("str_query")
#                                 ) # SELECT * FROM vardapp_users where id=1
#          if query.get("method") == "select":
#              datas = object.get_responces
#          elif query.get("method") == "create db":
#              datas = object.create_data_base()
#          elif query.get("method") == "create db":
#              datas = object.drop_data_base()
#          return Response(datas)
#       except Exception as error:
#          return Response([{'error': f'{error}'}])
#
#
#
#    @classmethod
#    def get_extra_actions(cls):
#       return []

#https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/views
#https://proproprogs.ru/django/drf-bazovyy-klass-apiview-dlya-predstavleniy


