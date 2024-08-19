from rest_framework import serializers
from appinvite.models import Invite
from appuser.models import User


# class ChatUserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
#     """Class for get only user's with access"""
#
#     def get_queryset(self):
#         request = self.context.get("request")
#         user_ = User.objects.get(email=request.user)
#         invite_owners = Invite.objects.filter(owner_id=user_).values('owner_id')
#         list_invite_owner = list()
#         list_invite_owner.append(user_.id)
#         for access_owner in invite_owners:
#             list_invite_owner.append(access_owner['owner_id'])
#         users = User.objects.filter(id__in=list_invite_owner)
#         query = User.objects.filter(id__in=users)
#         return query


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = [
            'id',
            'owner_id',
            'email',
            'date_invite',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'owner_id': {'read_only': True},
            #'email': {'read_only': True},
            'date_invite': {'read_only': True},
        }


