from .models import ClientDB
from rest_framework import serializers
from django.contrib.auth.models import User
import json
import datetime


class ClientSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = ClientDB
       fields = ['id','user','user_name','password','driver','url','host','port','data_base_type','data_base_name','description','str_query']

   # def create(self, validated_data):
   #     return ClientDB.objects.create(**validated_data)


# class ClientDBSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ClientDB
#        fields = ['id','user','user_name','password','driver','url','host','port','data_base_type','data_base_name','description','str_query']
#
#
# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """
#
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)
#
#         # Instantiate the superclass normally
#         super().__init__(*args, **kwargs)
#
#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
#
# class UserSerializer(DynamicFieldsModelSerializer):
#     class Meta:
#         model = ClientDB
#         fields = ['str_query','id']




# r[1]
# keys_list = list(ClientDB.result_query.keys())