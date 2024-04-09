from .models import ClientDB, Chart, ClientData
from rest_framework import serializers


class ChartSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Chart
       fields = ['id','user_id','clientdb_id','str_query']  # 'date_creation', 'date_change',


class ClientDataSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = ClientData
       fields = ['id','chart','data']


class ClientDBSerializer(serializers.ModelSerializer):
   class Meta:
       model = ClientDB
       fields = ['id','user','connection_name', 'user_name','password','driver','url',
                 'host','port','data_base_type','data_base_name','description',
                 'str_datas_for_connection']
