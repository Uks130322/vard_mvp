import re

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, drop_database, database_exists

from appchart_DB.models import Dashboard, Chart, ClientData, ChartDashboard
from appchart_DB.permissions import DataAccessPermission, DataAccessPermissionSafe, get_custom_queryset
from appchart_DB.serializers import (DashboardSerializer, ChartSerializer,
                                     ChartDashboardSerializer, ClientDataSerializer, ClientDBSerializer)

from appchart_DB.models import ClientDB, ClientData, Chart
from appuser.models import User
from appchart_DB.sql_alhimia import Work


class DashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    filterset_fields = ['user_id__id']

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Superuser can see all dashboards, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Dashboard.objects.all()
        else:
            queryset = get_custom_queryset(Dashboard, self.request.user, self.kwargs)
        return queryset


class ChartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows charts to be viewed or edited.
    """
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    filterset_fields = ['user_id__id', 'clientdata__id']

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Superuser can see all charts, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Chart.objects.all()
        else:
            queryset = get_custom_queryset(Chart, self.request.user, self.kwargs)
        return queryset

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        chart = self.get_object()
        clientdata = ClientData.objects.get(id=chart.clientdata.id)
        chartserializer = ChartSerializer(chart, data=request.data, partial=True)
        clientdataserializer = ClientDataSerializer(clientdata, data=request.data, partial=True)
        if chartserializer.is_valid() and clientdataserializer.is_valid():
            clientdata.delete()
            chart.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message_chart': chartserializer.errors,
                'message_clientdata': clientdataserializer.errors
            })



class ChartDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = ChartDashboard.objects.all()
    serializer_class = ChartDashboardSerializer
    permission_classes = [IsAuthenticated]


class ClientDBViewSet(viewsets.ModelViewSet):
    queryset = ClientDB.objects.all()
    serializer_class = ClientDBSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientDB.objects.all()
        else:
            user_ = User.objects.get(email=self.request.user)
            query = ClientDB.objects.filter(user_id=user_)
            return query

    def get_str_connect_sqlalchemy(self, user_name, password, url, host, port, data_base_name):
        password_new = password.replace('@', '%40')
        password_new = re.escape(password_new)
        str_connect = Work(data_base_type=2, url="", user_name=user_name, password=password_new,
                           host=host, port=port, data_base_name=data_base_name, str_query="", extension="").set_url()
        return str_connect

    def get_query(self, user_name, password, url, host, port, data_base_name, str_query, user_id):
        password_new = password.replace('@', '%40')
        password_new = re.escape(password_new)
        str_connect = Work(data_base_type=2, url="", user_name=user_name, password=password_new, host=host, port=port,
                           data_base_name=data_base_name, str_query=str_query, extension="")
        rows = str_connect.get_result()
        user = [{'user_id': user_id}]
        result = user + rows
        return result

    def perform_create(self, serializer):
        # serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        url = self.get_str_connect_sqlalchemy(
            datas['user_name'],
            datas['password'],
            datas['url'],
            datas['host'],
            datas['port'],
            datas['data_base_name']
        )
        return serializer.save(
            user_id=self.request.user,
            url=url
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Updating str_datas_for_connection in case of updating ClientDB object"""
        clientdb = self.get_object()
        serializer = ClientDBSerializer(clientdb, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            id = request.parser_context['kwargs']['pk']
            clientdbinstance = ClientDB.objects.get(id=id)
            url = self.get_str_connect_sqlalchemy(
                clientdbinstance.user_name,
                clientdbinstance.password,
                clientdbinstance.url,
                clientdbinstance.host,
                clientdbinstance.port,
                clientdbinstance.data_base_name
            )
            clientdbinstance.url = url
            clientdbinstance.save()
            return serializer
        else:
            return Response({
                'message': serializer.errors
            })


class ClientDataViewSet(viewsets.ModelViewSet):
    queryset = ClientData.objects.all()
    serializer_class = ClientDataSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermissionSafe]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientData.objects.all()
        else:
            return get_custom_queryset(ClientData, self.request.user, self.kwargs)

    def list(self, request, *args, **kwargs):
        L = []
        result = []
        error = ''
        old_response_data = super(ClientDataViewSet, self).list(request, *args, **kwargs)
        client_data = get_custom_queryset(ClientData, self.request.user, self.kwargs)
        for i, j in zip(client_data, old_response_data.data):
            obj = Chart.objects.get(id=i.chart.id)
            str_query = obj.str_query
            extension = obj.extension
            url = ClientDB.objects.get(id=obj.clientdb_id.id).url
            try:
                x = Work(data_base_type=2, url="mysql+pymysql://root:rootmysql@localhost:6001/bdmysql?charset=utf8mb4", user_name="", password="", host="", port="",
                         data_base_name="", str_query=str_query, extension=extension)
                result = x.get_result()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
            if not error:
                j['data'] = result
            else:
                j['error'] = error
            L.append(j)
        new_response_data = L
        return Response(new_response_data)

    def retrieve(self, request, pk, *args, **kwargs):
        L = []
        result = []
        error = ''
        old_response_data = super(ClientDataViewSet, self).list(request, *args, **kwargs)
        self.kwargs.pop('pk', None)
        client_data = get_custom_queryset(ClientData, self.request.user, self.kwargs).filter(pk=pk)
        for i, j in zip(client_data, old_response_data.data):
            obj = Chart.objects.get(id=i.chart.id)
            str_query = obj.str_query
            extension = obj.extension
            url = ClientDB.objects.get(id=obj.clientdb_id.id).url
            try:
                x = Work(data_base_type=2, url=url,
                         user_name="", password="", host="", port="",
                         data_base_name="", str_query=str_query, extension=extension)
                result = x.get_result()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
            if not error:
                j['data'] = result
            else:
                j['error'] = error
            L.append(j)
        if not L:
            L = [{'error': 'access denied'}]
        new_response_data = L
        return Response(new_response_data)

