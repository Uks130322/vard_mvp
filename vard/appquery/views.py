from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework import permissions
import django_filters
from .models import DataBaseQuery, ClientDB, Chart, ClientData
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import ClientSerializer, ClientDBSerializer, UserSerializer, ChartSerializer, ClientDataSerializer
from vardapp.models import Users
import json
import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import serializers
import re
from rest_framework import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy import exc


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer


class ClientDBViewSet(viewsets.ModelViewSet):
    queryset = ClientDB.objects.all()
    serializer_class = ClientDBSerializer

    def get_host(self, url, host, port):
        if host == 'localhost' or host == '127.0.0.1':
            result = host
        elif port == '' or port is None or not port:
            result = f'{url}:3306'
        else:
            result = f'{url}:{port}'
        return result

    def get_str_connect_sqlalchemy(self, user_name, password, url, host, port, data_base_name):
        password_new = password.replace('@', '%40')
        password_new = re.escape(password_new)
        host_new = self.get_host(url, host, port)
        str_connect = f"mysql://{user_name}:{password_new}@{host_new}/{data_base_name}"
        return str_connect

    def get_engine(self, user_name, password, url, host, port, data_base_name):
        str_connect_new = self.get_str_connect(user_name, password, url, host, port, data_base_name)
        engine = create_engine(f"{str_connect_new}", echo=False)
        return engine

    def create_data_base(self, user_name, password, url, host, port, data_base_name):
        str_connect_new = self.get_str_connect(user_name, password, url, host, port, data_base_name)
        if not database_exists(f"{str_connect_new}"):
            create_database(f"{str_connect_new}")
            return f'{data_base_name} создана'
        else:
            return f'{data_base_name} уже существует'

    def drop_data_base(self, user_name, password, url, host, port, data_base_name):
        str_connect_new = self.get_str_connect(user_name, password, url, host, port, data_base_name)
        if database_exists(f"{str_connect_new}"):
            drop_database(f"{str_connect_new}")
            return f'{data_base_name} удалена'
        else:
            return f'{data_base_name} не найдена'

    def get_query(self, user_name, password, url, host, port, data_base_name, str_query, user_id):
        engine = self.get_engine(user_name, password, url, host, port, data_base_name)
        Session = sessionmaker(autoflush=False, bind=engine)
        with Session(autoflush=False, bind=engine) as db:
            rows = db.execute(text(str_query)).fetchall()
            user = [{'user_id':user_id}]
            result = user + [r._asdict() for r in rows]
        return result

    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        str_connection = self.get_str_connect_sqlalchemy(datas['user_name'], datas['password'], datas['url'],
                                                         datas['host'],datas['port'], datas['data_base_name'])
        return serializer.save(user=self.request.user, str_connection=str_connection)

    def get_queryset(self):
        #queryset = super(ClientDBViewSet, self).get_queryset()
        queryset = ClientDB.objects.filter(user_id=self.request.user)
        return queryset

class ClientDataViewSet(viewsets.ModelViewSet):
    queryset = ClientData.objects.all()
    serializer_class = ClientDataSerializer

    def list(self, request, *args, **kwargs):
        L = []
        old_response_data = super(ClientDataViewSet, self).list(request, *args, **kwargs)
        client_data = ClientData.objects.all()
        for i, j in zip(client_data, old_response_data.data):
        #for i in client_data:
            obj = Chart.objects.get(id=i.chart.id)
            str_query = obj.str_query
            str_connection = ClientDB.objects.get(id=obj.clientdb_id.id).str_connection
            try:
                engine = create_engine(f"{str_connection}", echo=False)
                Session = sessionmaker(autoflush=False, bind=engine)
                with Session(autoflush=False, bind=engine) as db:
                    rows = db.execute(text(str_query)).fetchall()
                    result = [r._asdict() for r in rows]
                    if not ClientData.objects.filter(id=i.chart.id):
                        ClientData.objects.filter(id=i.chart.id).update(data=result)
            except exc.SQLAlchemyError as e:
                #error = str(e.__dict__['orig'])
                print('error',e)
            j['data'] = result
            L.append(j)
        new_response_data = L
        #queryset = ClientData.objects.all()
        return Response(new_response_data)
# def list(self, request, *args, **kwargs):
    #     L=[]
    #     old_response_data = super(ClientViewset, self).list(request, *args, **kwargs)
    #     client_connect = ClientDB.objects.all()
    #     for i,j in zip(client_connect, old_response_data.data):
    #         result = i.update_responce(i.id)
    #         j['result_query'] = result
    #         L.append(j)
    #     new_response_data = L
    #     return Response(new_response_data)



# class ClientViewset(mixins.RetrieveModelMixin,
#                     mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     mixins.ListModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = ClientDB.objects.all()
#     serializer_class = ClientSerializer
#     permission_classes = [permissions.AllowAny]

    # def list(self, request, *args, **kwargs):
    #     L=[]
    #     old_response_data = super(ClientViewset, self).list(request, *args, **kwargs)
    #     client_connect = ClientDB.objects.all()
    #     for i,j in zip(client_connect, old_response_data.data):
    #         result = i.update_responce(i.id)
    #         j['result_query'] = result
    #         L.append(j)
    #     new_response_data = L
    #     return Response(new_response_data)
    #
    #
    # def retrieve(self, request, pk=None):
    #     serializer_context = {
    #         'request': request,
    #     }
    #     queryset = ClientDB.objects.all()
    #     result = get_object_or_404(queryset, pk=pk)
    #     serializer = ClientSerializer(result, context=serializer_context)
    #     client_query = result.update_responce(pk)
    #     dict_result = serializer.data
    #     dict_result['result_query'] = client_query
    #     return Response(dict_result)
    #
    # def perform_create(self, serializer):
    #     print('self.request',self.request.data['user'][32:][:-1])
    #     user = get_object_or_404(Users, id=self.request.data['user'][32:][:-1])
    #     print('!!!!!!!костыль!!!!!!user',user)
    #     return serializer.save(user=user)

    #
    # def update(self, request, pk=None):
    #     pass
    #
    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


# class ClientDBListAPIView(generics.ListAPIView):
#     queryset = ClientDB.objects.all().values_list('str_query','id')
#     serializer_class = UserSerializer  #ClientDBSerializer
#     # lookup_field = 'user__id'
#     # lookup_url_kwarg = 'user'
#
#     def get_queryset(self):
#         username = self.request.user
#         user = Users.objects.get(email = username)
#         ids = ClientDB.objects.get(user__email = username)
#         print('username',username)
#         client_connect = ClientDB.objects.filter(user__email = username) #user__email = username
#         return super().get_queryset().filter(user__email=username).values('str_query','id')
#
#     def list(self, request, *args, **kwargs):
#         username = self.request.user
#         client_connect = ClientDB.objects.get(id=1)
#         result = client_connect.update_responce()
#         return Response(result)


#from appquery.models import *
#u1 = Users.objects.get(id = 1)
#d1 = ClientDB.objects.create(user=u1,user_name = 'root', password = 'P@r0l', driver = 1, url = None, host = 'localhost', port = None, data_base_type = None, data_base_name = 'baza_test1', description = None, str_query = 'SELECT * FROM vardapp_users')
#d1.save()
#d1 = ClientDB.objects.get(id = 1)
#d1.get_responces
#
#

class DBView(views.APIView):
   def get(self, request, *args, **kwargs):
       L = []
       username = self.request.user
       #print('username',username.id)
       client_connect = ClientDB.objects.filter(user_id=username.id)
       #print('client_connect',client_connect)
       for i in client_connect:
           result = i.update_responce(i.id)
           print('result',result)
           L.append(result)
       new_response_data = L
       return Response(new_response_data)
   def post(self, request):
      try:
         query_body = request.body.decode('UTF-8')
         query = eval(query_body.replace("null", "None"))
         object = DataBaseQuery(query.get("user_id"), query.get("driver"), query.get("user_name"),
                                query.get("password"), query.get("url"), query.get("host"),
                                query.get("port"), query.get("data_base_name"), query.get("data_base_type"),
                                query.get("description"), query.get("str_query")
                                ) # SELECT * FROM vardapp_users where id=1
         if query.get("method") == "select":
             datas = object.get_responces
         elif query.get("method") == "create db":
             datas = object.create_data_base()
         elif query.get("method") == "create db":
             datas = object.drop_data_base()
         return Response(datas)
      except Exception as error:
         return Response([{'error': f'{error}'}])

   @classmethod
   def get_extra_actions(cls):
      return []



