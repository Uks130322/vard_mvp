from django.db.models import Q
from rest_framework import serializers

from appchat.models import Chat, Message
from appuser.models import User, Access


class ChatUserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's with access"""

    def get_queryset(self):
        request = self.context.get("request")
        user_ = User.objects.get(email=request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        list_access_owner = list()
        list_access_owner.append(user_.id)
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = User.objects.filter(id__in=users)
        return query


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    # owner_id = ChatUserFilteredPrimaryKeyRelatedField(many=False)

    class Meta:
        model = Chat
        fields = [
            'id',
            'owner_id',
            'user_id',
            'date_send',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
        }


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'chat_id',
            'user_id',
            'date_send',
            'message',
            'doc',
            'is_remove',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
            'is_remove': {'read_only': True},
        }