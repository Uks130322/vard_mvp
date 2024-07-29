from django.db.models import Q
from rest_framework import serializers

from appchart_DB.models import Chart, Dashboard
from appcomment.models import Comment, ReadComment
from appfile.models import File
from appuser.models import Access, User
from vard.settings import DEBUG


class CommentChartFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Only for demonstrate. Don't use it in production"""
    def get_queryset(self):
        request = self.context.get("request")
        user_ = request.user
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        list_access_owner.append(user_.id)
        users = User.objects.filter(id__in=list_access_owner)
        query = Chart.objects.filter(user_id__in=users)
        return query


class CommentFileFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Only for demonstrate. Don't use it in production"""
    def get_queryset(self):
        request = self.context.get("request")
        user_ = request.user
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = File.objects.filter(user_id__in=users)
        return query


class CommentDashboardFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Only for demonstrate. Don't use it in production"""
    def get_queryset(self):
        request = self.context.get("request")
        user_ = email = request.user
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = Dashboard.objects.filter(user_id__in=users)
        return query


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    if DEBUG:
        file_id = CommentFileFilteredPrimaryKeyRelatedField(many=False, allow_null=True)
        chart_id = CommentChartFilteredPrimaryKeyRelatedField(many=False, allow_null=True)
        dashboard_id = CommentDashboardFilteredPrimaryKeyRelatedField(many=False, allow_null=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'file_id',
            'chart_id',
            'dashboard_id',
            'user_id',
            'date_send',
            'date_remove',
            'date_delivery',
            'comment'
        ]
        extra_kwargs = {
            'user_id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class ReadCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadComment
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }
