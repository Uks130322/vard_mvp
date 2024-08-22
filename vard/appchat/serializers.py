from django.db.models import Q
from rest_framework import serializers

from appchat.models import Chat, Message
from appuser.models import User, Access


class ChatUserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Class for get only user's with access"""

    def get_queryset(self):
        request = self.context.get("request")
        user = User.objects.get(email=request.user)
        access_owners = Access.objects.filter(Q(user_id=user) |
                                              Q(owner_id=user)).values('owner_id')
        chats = Chat.objects.filter(owner_id__in=access_owners).values('id')
        return chats


class ChatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Chat
        fields = [
            'id',
            'owner_id',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'owner_id': {'read_only': True},
        }


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    # chat_id = ChatUserFilteredPrimaryKeyRelatedField(many=False)
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