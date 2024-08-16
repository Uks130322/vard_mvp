import re

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, drop_database, database_exists

from appchart_DB.models import Dashboard, Chart, ClientData, ChartDashboard, ClientDB
from appchart_DB.permissions import DataAccessPermission, DataAccessPermissionSafe, get_custom_queryset
from appchart_DB.plot_utils import create_plot
from appchart_DB.serializers import (DashboardSerializer, ChartSerializer,
                                     ChartDashboardSerializer, ClientDataSerializer, ClientDBSerializer)

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        """If x_data and y_data are provided, a plot is creating"""
        instance = self.get_object()
        datas = self.request.data
        try:
            connection_obj = Work(
                data_base_type=int(instance.clientdb_id.data_base_type),
                url=instance.clientdb_id.url,
                user_name="",
                password="",
                host="",
                port="",
                data_base_name="",
                str_query=instance.str_query,
                extension=1
            )
            chart_data = connection_obj.get_result()['result']
            if datas['x_data'] and datas['y_data']:
                plot=create_plot(
                    key_x=datas['x_data'],
                    key_y=datas['y_data'],
                    chart_data=chart_data,
                    image_format=Chart.ImageFormat(int(datas["image_format"])).name,
                    x_label=datas['x_label'],
                    y_label=datas['y_label'],
                    color=Chart.Color(datas['color']).name,
                    title=datas['title'],
                    plot_type=Chart.PlotType(int(datas["plot_type"])).name
                )
            else:
                plot = None
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(plot=plot)

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

    def get_str_connect_sqlalchemy(self, data_base_type, user_name, password, url, host, port, data_base_name):
        # password_new = password.replace('@', '%40')
        # password_new = re.escape(password_new)
        str_connect = Work(
            data_base_type=data_base_type,
            url=url,
            user_name=user_name,
            password=password,
            host=host,
            port=port,
            data_base_name=data_base_name,
            str_query="",
            extension=""
        ).set_url()
        return str_connect

    def get_query(self, data_base_type, user_name, password, url, host, port, data_base_name, str_query, user_id):
        # password_new = password.replace('@', '%40')
        # password_new = re.escape(password_new)
        str_connect = Work(
            data_base_type=data_base_type,
            url="",
            user_name=user_name,
            password=password,
            host=host,
            port=port,
            data_base_name=data_base_name,
            str_query=str_query,
            extension=""
        )
        rows = str_connect.get_result()
        user = [{'user_id': user_id}]
        result = user + rows
        return result

    def perform_create(self, serializer):
        # serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        url = self.get_str_connect_sqlalchemy(
            data_base_type=int(datas['data_base_type']),
            user_name=datas['user_name'],
            password=datas['password'],
            url=datas['url'],
            host=datas['host'],
            port=datas['port'],
            data_base_name=datas['data_base_name']
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
            clientdb_instance = ClientDB.objects.get(id=id)
            url = self.get_str_connect_sqlalchemy(
                data_base_type=int(clientdb_instance.data_base_type),
                user_name=clientdb_instance.user_name,
                password=clientdb_instance.password,
                url=clientdb_instance.url,
                host=clientdb_instance.host,
                port=clientdb_instance.port,
                data_base_name=clientdb_instance.data_base_name
            )
            clientdb_instance.url = url
            clientdb_instance.save()
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
        new_data_list = []
        result = []
        error = ''
        old_response_data = super(ClientDataViewSet, self).list(request, *args, **kwargs)
        client_data = get_custom_queryset(ClientData, self.request.user, self.kwargs)
        for i, j in zip(client_data, old_response_data.data):
            obj = Chart.objects.get(id=i.chart.id)
            str_query = obj.str_query
            extension = obj.extension
            url = ClientDB.objects.get(id=obj.clientdb_id.id).url
            data_base_type = int(ClientDB.objects.get(id=obj.clientdb_id.id).data_base_type)
            try:
                connection_obj = Work(
                    data_base_type=data_base_type,
                    url=url,
                    user_name="",
                    password="",
                    host="",
                    port="",
                    data_base_name="",
                    str_query=str_query,
                    extension=extension
                )
                result = connection_obj.get_result()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
            if not error:
                j['data'] = result
            else:
                j['error'] = error
            new_data_list.append(j)
        new_response_data = new_data_list
        return Response(new_response_data)

    def retrieve(self, request, pk, *args, **kwargs):
        new_data_list = []
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
            data_base_type = int(ClientDB.objects.get(id=obj.clientdb_id.id).data_base_type)
            try:
                connection_obj = Work(
                    data_base_type=data_base_type,
                    url=url,
                    user_name="",
                    password="",
                    host="",
                    port="",
                    data_base_name="",
                    str_query=str_query,
                    extension=extension
                )
                result = connection_obj.get_result()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
            if not error:
                j['data'] = result
            else:
                j['error'] = error
            new_data_list.append(j)
        if not new_data_list:
            new_data_list = [{'error': 'access denied'}]
        new_response_data = new_data_list
        return Response(new_response_data)
