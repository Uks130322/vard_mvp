from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from appinvite.models import Invite
#from appinvite.permissions import ChatAccessPermission, MessageAccessPermission
from appinvite.serializers import InviteSerializer
from appuser.models import User, Access
from django.shortcuts import render
import hashlib
import uuid


class InviteViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = InviteSerializer

    def get_queryset(self):
        pk = self.request.parser_context.get('kwargs').get('pk')
        Invite.objects.filter(id=pk).delete()
        queryset = ''
        return queryset

    def perform_create(self, serializer):
        datas = serializer.validated_data
        id = hashlib.sha3_512(f'{uuid.uuid4()}'.encode('utf-8')).hexdigest()
        user_exist = User.objects.filter(email=datas.get('email'))
        if user_exist:
            user_id = User.objects.get(email=datas.get('email'))
            owner_id = User.objects.get(id=self.request.user.id)
            access = Access.objects.filter(user_id=user_id, owner_id=self.request.user.id)
            if not access:
                Access.objects.create(user_id=user_id, owner_id=owner_id, access_type_id=datas.get('access_type_id'))
        if not user_exist:
            return serializer.save(owner_id=self.request.user, id=id, **datas)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'message': "приглашение отправлено"
        })








