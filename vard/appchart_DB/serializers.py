from django.db import transaction
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from appchart_DB.models import Chart, ClientDB, ClientData, ChartDashboard, Dashboard
from appuser.models import User


class ChartClientdbFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's clientdb to add it to the chart"""

    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)

        if request.parser_context['kwargs'].get('pk', False):
            id_obj = request.parser_context['kwargs']['pk']
            obj = Chart.objects.get(id=id_obj)
            if obj.user_id == user_:
                query = ClientDB.objects.filter(user_id=user_)
            else:
                query = ClientDB.objects.filter(user_id=obj.user_id)
        else:
            query = ClientDB.objects.filter(user_id=user_)
        return query


class ChartSerializer(serializers.HyperlinkedModelSerializer):
    clientdb_id = ChartClientdbFilteredPrimaryKeyRelatedField(many=False)

    class Meta:
        model = Chart
        fields = [
            'id',
            'user_id',
            'date_creation',
            'date_change',
            'clientdb_id',
            'str_query',
            'clientdata'
        ]
        extra_kwargs = {
            'user_id': {'read_only': True},
            'clientdata': {'read_only': True},
        }

    @transaction.atomic
    def create(self, validated_data, **kwargs):
        clientdata = ClientData.objects.create(user_id=validated_data['user_id'], data='')
        chart = Chart.objects.create(**validated_data, clientdata=clientdata)
        return chart





class ChartDashboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChartDashboard
        fields = ['id', 'chart', 'dashboard']


class ChartDashboardFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's charts to add it to the dashboard"""
    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)

        if request.parser_context['kwargs'].get('pk', False):
            id_obj = request.parser_context['kwargs']['pk']
            obj = Dashboard.objects.get(id=id_obj)
            if obj.user_id == user_:
                query = Chart.objects.filter(user_id=user_)
            else:
                query = Chart.objects.filter(user_id=obj.user_id)
        else:
            query = Chart.objects.filter(user_id=user_)
        return query


class DashboardSerializer(WritableNestedModelSerializer):
    chart = ChartDashboardFilteredPrimaryKeyRelatedField(many=True)

    class Meta:
        model = Dashboard
        fields = [
            'id',
            'user_id',
            'date_creation',
            'date_change',
            'chart'
        ]

        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class ClientDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientData
        fields = [
            'id',
            'data'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'data': {'read_only': True},
        }


class ClientDBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientDB
        fields = [
            'id',
            'user_id',
            'connection_name',
            'user_name',
            'password',
            'driver',
            'url',
            'host',
            'port',
            'data_base_type',
            'data_base_name',
            'description',
            'str_datas_for_connection'
        ]
        extra_kwargs = {
            # 'user': {'write_only': True},
            'user_id': {'read_only': True},
            'connection_name': {'write_only': False},
            'user_name': {'write_only': False},
            'password': {'write_only': False},
            'driver': {'write_only': False},
            'url': {'write_only': False},
            'host': {'write_only': False},
            'port': {'write_only': False},
            'data_base_type': {'write_only': False},
            'data_base_name': {'write_only': False},

            'str_datas_for_connection': {'read_only': True},
        }
