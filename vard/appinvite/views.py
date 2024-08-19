from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appinvite.models import Invite
#from appinvite.permissions import ChatAccessPermission, MessageAccessPermission
from appinvite.serializers import InviteSerializer
from appuser.models import User
from django.shortcuts import render
import hashlib
import uuid

class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer

    def perform_create(self, serializer):
        datas = serializer.validated_data
        print('datas ', datas)
        id = hashlib.sha3_512(f'{uuid.uuid4()}'.encode('utf-8')).hexdigest()
        #link = hashlib.sha3_512(f'{self.request.user}'.encode('utf-8')).hexdigest()
        return serializer.save(owner_id=self.request.user, id=id, **datas)







