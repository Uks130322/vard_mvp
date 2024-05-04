from django.conf import settings
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_writable_nested import WritableNestedModelSerializer

from vardapp.models import (User, Access, File, Chart, ClientData, Dashboard,
                            Feedback, ChartDashboard, Comment, ReadComment, ClientDB)
from appchat.models import Chat
from appquery.serializers import ClientDataSerializer
from APIapp.utils import load_csv, load_json
from .hash_md import get_hash_md5


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'is_superuser',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
        }


class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        fields = '__all__'
        extra_kwargs = {
            'owner_id': {'read_only': True},
        }

    def create(self, validated_data, **kwargs):
        qs = Access.objects.filter(owner_id=validated_data['owner_id']).filter(user_id=validated_data['user_id'])
        if not qs.exists():
            access = Access.objects.create(**validated_data)
        else:
            access = Access.objects.get(**validated_data)
        return access


class FileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.URLField(source='load_by_url', write_only=True, allow_blank=True)

    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {
            'date_delete': {'read_only': True},
            'user_id': {'read_only': True},
            'type_id': {'read_only': True},
        }

    def load_by_url(self, validated_data):
        try:
            validated_data = load_json(self, validated_data)
            return validated_data
        except BaseException as error:
            try:
                validated_data = load_csv(self, validated_data)
                return validated_data
            except BaseException as error:
                raise ValidationError(error)

    def create(self, validated_data):
        if validated_data['load_by_url']:
            validated_data = self.load_by_url(validated_data)

        validated_data.pop('load_by_url', None)
        file = File(**validated_data)
        if not file.name:
            file.name = file.link.name
        file_type = file.link.name.split('.')[-1].upper()
        file.type_id = File.FilesType[file_type].value
        file.save()

        path_instance = f'{settings.BASE_DIR}{settings.MEDIA_URL}files/{file.link}'.replace('\\', '/')
        hash_instance = get_hash_md5(path_instance)
        files = File.objects.filter(user_id=validated_data['user_id']).exclude(id=file.id)

        for file_ in files:
            path_file = f'{settings.BASE_DIR}{settings.MEDIA_URL}files/{file_.link}'.replace('\\', '/')
            hash_file = get_hash_md5(path_file)
            if hash_instance == hash_file:
                file.link.delete()
                file.delete()
                file = file_
        return file


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class ChartClientdbFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's clientdb to add it to the chart"""
    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)
        query = ClientDB.objects.filter(user_id=user_)
        return query

class ChartUserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user to add it to the chart"""
    def get_queryset(self):
        request = self.context.get("request")
        query = User.objects.filter(email=request.user)
        return query

class ChartSerializer(serializers.HyperlinkedModelSerializer):
    clientdb_id = ChartClientdbFilteredPrimaryKeyRelatedField(many=False)
    user_id = ChartUserFilteredPrimaryKeyRelatedField(many=False)
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
            'clientdata': {'read_only': True},
        }

    @transaction.atomic
    def create(self, validated_data, **kwargs):
        #print('**validated_data',validated_data['clientdb_id'])
        clientdata = ClientData.objects.create(user_id=validated_data['user_id'], data='')
        # for i in validated_data['clientdb_id']:
        #     clientdb_ids = ClientDB.objects.get(id=validated_data['clientdb_id'])
        # print('clientdb_id',clientdb_ids)
        #chart = Chart.objects.create(user_id=validated_data['user_id'], clientdata=clientdata, clientdb_id=validated_data['clientdb_id'], str_query=validated_data['str_query'])
        chart = Chart.objects.create(**validated_data, clientdata=clientdata)
        return chart


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class ReadCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadComment
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }



class ChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id',
            'user_id_owner',
            'user_id_sender',
            'date_send',
            'message'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id_sender': {'read_only': True},
        }


class ChartDashboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChartDashboard
        fields = ['id', 'chart', 'dashboard']


class ChartDashboardFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's charts to add it to the dashboard"""
    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)

        if request.parser_context['kwargs'].get('pk',False):
            id_obj = request.parser_context['kwargs']['pk']
            obj = Dashboard.objects.get(id = id_obj)
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
