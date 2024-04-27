from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from vardapp.models import *
from .permissions import DataAccessPermission, CommentAccessPermission
from appchat.models import Chat
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = User.objects.filter(email = self.request.user)
        return query


class AccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Access to be viewed or edited. Only Owner can change access level.
    """
    queryset = Access.objects.all()
    serializer_class = AccessSerializer

    def perform_create(self, serializer):
        """The creator is automatically assigned as owner_id"""
        datas = serializer.validated_data
        return serializer.save(owner_id=self.request.user, **datas)

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_ = User.objects.get(email = self.request.user)
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
        user_ = User.objects.get(email = self.request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        if access_owners.exists():
            users = User.objects.filter(id=access_owners[0]['owner_id'])
            print('users',users)
            for access_owner in access_owners:
                users = users.union(User.objects.filter(id=access_owner['owner_id']))
            query = File.objects.filter(user_id=users[0].id)
            for user in users:
                query = query.union(File.objects.filter(Q(user_id=user.id) | Q(user_id=user_)))
        else:
            query = File.objects.filter(user_id=user_)
        return query


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows feedback messages to be viewed or edited.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

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
        user_ = User.objects.get(email = self.request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        if access_owners.exists():
            users = User.objects.filter(id=access_owners[0]['owner_id'])
            for access_owner in access_owners:
                users = users.union(User.objects.filter(id=access_owner['owner_id']))
            query = Dashboard.objects.filter(user_id=users[0].id)
            for user in users:
                query = query.union(Dashboard.objects.filter(Q(user_id=user.id) | Q(user_id=user_)))
        else:
            query = Dashboard.objects.filter(user_id=user_)
        return query


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
        user_ = User.objects.get(email = self.request.user)
        access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
        if access_owners.exists():
            users = User.objects.filter(id=access_owners[0]['owner_id'])
            for access_owner in access_owners:
                users = users.union(User.objects.filter(id=access_owner['owner_id']))
            query = Chart.objects.filter(user_id=users[0].id)
            for user in users:
                query = query.union(Chart.objects.filter(Q(user_id=user.id) | Q(user_id=user_)))
        else:
            query = Chart.objects.filter(user_id=user_)
        return query


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
        ???
    """
    queryset = Chat.objects.filter(is_remove=False).order_by('-date_send')
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user_id_owner__id', 'user_id_sender__id', 'date_send', 'message']

    def destroy(self, request, *args, **kwargs):
        chat = self.get_object()
        if self.action == 'destroy':
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
        else:
            return Response({
                'state': '0',
                'message': f"отклонено. причина: {chat.get_status_display()}"
            })

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id_sender"""
        datas = serializer.validated_data
        print('self.request.user',self.request.user)
        return serializer.save(**datas)


class ChartDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = ChartDashboard.objects.all()
    serializer_class = ChartDashboardSerializer
