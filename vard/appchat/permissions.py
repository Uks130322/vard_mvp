from django.db.models import Q
from rest_framework.permissions import BasePermission, SAFE_METHODS

from appuser.models import Access


class ChatAccessPermission(BasePermission):
    # TODO: add commentator
    """
    All users witn any access by owner can see  owner's chat
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        is_reader = Access.objects.filter(user_id=request.user.id, owner_id=obj.owner_id).exists()
        is_owner = request.user == obj.owner_id
        is_editor = Access.objects.filter(user_id=request.user.id,
                                          owner_id=obj.owner_id).filter(user_id=obj.user_id).exists()
        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_editor]):
            return True
        elif request.method == "DELETE" and any([is_owner, is_editor]):
            return True
        elif request.method == "PUT" and any([is_owner, is_editor]):
            return True
        else:
            return False

class MessageAccessPermission(BasePermission):
    """
    All users witn any access by owner can see  owner's messages
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        is_reader = Access.objects.filter(user_id=request.user.id, owner_id=obj.chat_id.owner_id).exists()
        is_owner = request.user == obj.chat_id.owner_id
        is_editor = Access.objects.filter(user_id=request.user.id,
                                          owner_id=obj.chat_id.owner_id).filter(user_id=obj.user_id).exists()
        is_sender = obj.user_id == request.user
        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_editor, is_sender]):
            return True
        elif request.method == "DELETE" and any([is_owner, is_sender]):
            return True
        elif request.method == "PUT" and any([is_owner, is_sender]):
            return True
        else:
            return False