from rest_framework import serializers

from vardapp.models import ClientDB, ClientData


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
