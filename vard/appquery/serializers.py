from vardapp.models import ClientDB, ClientData
from rest_framework import serializers


class ClientDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientData
        fields = [
            'id',
            'chart',
            'data'
        ]


class ClientDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDB
        fields = [
            'id',
            'user',
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
            'connection_name': {'write_only': True},
            'user_name': {'write_only': True},
            'password': {'write_only': True},
            'driver': {'write_only': True},
            'url': {'write_only': True},
            'host': {'write_only': True},
            'port': {'write_only': True},
            'data_base_type': {'write_only': True},
            'data_base_name': {'write_only': True},

            'str_datas_for_connection': {'read_only': True},
        }
