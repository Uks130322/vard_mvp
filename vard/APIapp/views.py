from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from vardapp.models import *
from .permissions import DataAccessPermission, CommentAccessPermission, get_custom_queryset, DataAccessPermissionSafe
from appchat.models import Chat
from .serializers import (UserSerializer, AccessSerializer, FileSerializer, DashboardSerializer,
                          ChartSerializer, CommentSerializer, FeedbackSerializer, ChartDashboardSerializer,
                          ReadCommentSerializer, ChatSerializer)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Superuser can see all users, others can see only themselves"""
        if self.request.user.is_superuser:
            queryset = User.objects.all().order_by('name')
        else:
            queryset = User.objects.filter(email=self.request.user)  # one authorized user
        return queryset


class AccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Access to be viewed or edited. Only Owner can change access level.
    """
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
    filterset_fields = ['user_id__id', 'owner_id__id']

    def perform_create(self, serializer):
        """The creator is automatically assigned as owner_id"""
        datas = serializer.validated_data
        return serializer.save(owner_id=self.request.user, **datas)

    permission_classes = [IsAuthenticated]

# if we want to show only access objects of authorized user:
    def get_queryset(self):
        user_ = User.objects.get(email=self.request.user)
        query = Access.objects.filter(owner_id=user_)
        return query


class FileViewSet(viewsets.ModelViewSet):
    """
    User should see the list of all his files. If he got permission, he can see others users'
    files by detail, not the list
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['user_id__id']

    def create(self, request, *args, **kwargs):
        try:
            serializer = FileSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except TypeError as error:
            return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Wrong file type, it should be json or csv'
                    })

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return get_custom_queryset(File, self.request.user, self.kwargs)


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows feedback messages to be viewed or edited.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermissionSafe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)


class DashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    filterset_fields = ['user_id__id']

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return get_custom_queryset(Dashboard, self.request.user, self.kwargs)


class ChartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows charts to be viewed or edited.
    """
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    filterset_fields = ['user_id__id']

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return get_custom_queryset(Chart, self.request.user, self.kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all().order_by('-date_send')
    serializer_class = CommentSerializer
    filterset_fields = ['user_id__id']

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, DataAccessPermission]
        else:
            permission_classes = [IsAuthenticated, CommentAccessPermission]
        return [permission() for permission in permission_classes]


class ReadCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comment reading to be viewed or edited.
    """
    queryset = ReadComment.objects.all().order_by('-date_reading')
    serializer_class = ReadCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)


class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """
    queryset = Chat.objects.filter(is_remove=False).order_by('-date_send')
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user_id_owner__id', 'user_id_sender__id', 'date_send']

    def destroy(self, request, *args, **kwargs):
        chat = self.get_object()
        # if self.action == 'destroy':
        chat.is_remove = True
        serializer = ChatSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_context = {'request': request}
            return Response(ChatSerializer(chat, context=serializer_context).data, status=status.HTTP_200_OK)
        else:
            return Response({
                'state': '0',
                'message': serializer.errors
            })
        # else:
        #     return Response({
        #         'state': '0',
        #         'message': f"отклонено. причина: {chat.get_status_display()}"
        #     })

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id_sender"""
        datas = serializer.validated_data
        print('self.request.user', self.request.user)  ### WTF
        return serializer.save(**datas)


class ChartDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = ChartDashboard.objects.all()
    serializer_class = ChartDashboardSerializer
    permission_classes = [IsAuthenticated]
