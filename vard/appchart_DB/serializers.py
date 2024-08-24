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
    # clientdb_id = ChartClientdbFilteredPrimaryKeyRelatedField(many=False)

    class Meta:
        model = Chart
        fields = [
            'id',
            'user_id',
            'date_creation',
            'date_change',
            'clientdb_id',
            'str_query',
            'clientdata',
            'x_data',
            'y_data',
            'x_label',
            'y_label',
            'title',
            'plot_type',
            'color',
            'image_format',
            'plot',
            'extension',
        ]
        extra_kwargs = {
            'user_id': {'read_only': True},
            'clientdata': {'read_only': True},
            'plot': {'read_only': True},
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
    # chart = ChartDashboardFilteredPrimaryKeyRelatedField(many=True)

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
            'url',
            'host',
            'port',
            'data_base_type',
            'data_base_name',
            'description',
        ]
        extra_kwargs = {
            'user_id': {'read_only': True},
        }
