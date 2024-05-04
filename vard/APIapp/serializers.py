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
from django.db.models import Q


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


class CommentChartFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        list_access_owner.append(user_.id)
        users = User.objects.filter(id__in=list_access_owner)
        query = Chart.objects.filter(user_id__in=users)
        return query


class CommentFileFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = File.objects.filter(user_id__in=users)
        return query


class CommentDashboardFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = Dashboard.objects.filter(user_id__in=users)
        return query


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    file_id = CommentFileFilteredPrimaryKeyRelatedField(many=False, allow_null=True)
    chart_id = CommentChartFilteredPrimaryKeyRelatedField(many=False, allow_null=True)
    dashboard_id = CommentDashboardFilteredPrimaryKeyRelatedField(many=False, allow_null=True)
    class Meta:
        model = Comment
        fields = ['id','file_id','chart_id','dashboard_id','user_id','date_send','date_remove','date_delivery','comment']
        extra_kwargs = {
            'user_id': {'read_only': True},
        }

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.file_id != data_user['file_id'],
                instance_user.chart_id != data_user['chart_id'],
                instance_user.dashboard_id != data_user['dashboard_id'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'отклонено':'нельзя изменить комментируемый объект'})
        return data


class ReadCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadComment
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class ChatUserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's clientdb to add it to the chart"""

    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = User.objects.filter(id__in=users)
        return query

class ChatSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = ChatUserFilteredPrimaryKeyRelatedField(many=False)
    class Meta:
        model = Chat
        fields = [
            'id',
            'owner_id',
            'user_id',
            'date_send',
            'message'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
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
