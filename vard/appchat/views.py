from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appchat.models import Chat, Message
from appchat.permissions import ChatAccessPermission, MessageAccessPermission
from appchat.serializers import ChatSerializer, MessageSerializer
from appuser.models import User, Access


class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chat messages to be viewed or edited.
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    permission_classes = [IsAuthenticated, ChatAccessPermission]

    filterset_fields = ['owner_id__id']

    def get_queryset(self):
        """Superuser can see all messages, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Chat.objects.all()
        else:
            access_owners = Access.objects.filter(user_id=self.request.user).values('owner_id')
            queryset = Chat.objects.filter(Q(owner_id_id__in=access_owners) |
                                           Q(owner_id_id=self.request.user))
        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chat messages to be viewed or edited.
    """
    queryset = Message.objects.filter(is_remove=False).order_by('-date_send')
    serializer_class = MessageSerializer

    filterset_fields = ['chat_id', 'user_id', 'date_send']
    permission_classes = [IsAuthenticated, MessageAccessPermission]

    def get_queryset(self):
        """Superuser can see all messages, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Message.objects.all()
        else:
            access_owners = Access.objects.filter(user_id=self.request.user).values('owner_id')
            queryset = Message.objects.filter(Q(chat_id__owner_id__in=access_owners) |
                                              Q(user_id=self.request.user), is_remove=False).order_by('-date_send')
        return queryset

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id_sender"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        message.is_remove = True
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_context = {'request': request}
            return Response(MessageSerializer(message, context=serializer_context).data, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors
            })