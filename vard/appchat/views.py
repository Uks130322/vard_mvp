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
    queryset = Chat.objects.filter(is_remove=False).order_by('-date_send')
    serializer_class = ChatSerializer

    # should be added some special permissions
    permission_classes = [IsAuthenticated, ChatAccessPermission]

    filterset_fields = ['owner_id__id', 'user_id__id', 'date_send']

    def destroy(self, request, *args, **kwargs):
        chat = self.get_object()
        chat.is_remove = True
        serializer = ChatSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_context = {'request': request}
            return Response(ChatSerializer(chat, context=serializer_context).data, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors
            })

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id_sender"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_queryset(self):
        """Superuser can see all messages, others can see theirs own and all with access"""
        user_ = User.objects.get(email=self.request.user)
        if self.request.user.is_superuser:
            queryset = Chat.objects.all()
        else:
            access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
            queryset = Chat.objects.filter(Q(owner_id_id__in=access_owners) |
                                           Q(owner_id_id=self.request.user), is_remove=False).order_by('-date_send')
        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chat messages to be viewed or edited.
    """
    queryset = Message.objects.filter(is_remove=False).order_by('-date_send')
    serializer_class = MessageSerializer

    filterset_fields = ['chat_id__id', 'user_id__id', 'date_send']
    permission_classes = [IsAuthenticated, MessageAccessPermission]

    def get_queryset(self):
        """Superuser can see all messages, others can see theirs own and all with access"""
        user_ = User.objects.get(email=self.request.user)
        if self.request.user.is_superuser:
            queryset = Message.objects.all()
        else:
            access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
            queryset = Message.objects.filter(Q(chat_id__owner_id_id__in=access_owners) |
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