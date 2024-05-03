from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from vardapp.models import (User, Access, File, Dashboard, Chart, Comment, Feedback, ChartDashboard, ReadComment)
from appchat.models import Chat
from .permissions import (DataAccessPermission, CommentAccessPermission, get_custom_queryset,
                          DataAccessPermissionSafe, can_comment)
from .serializers import (UserSerializer, AccessSerializer, FileSerializer, DashboardSerializer,
                          ChartSerializer, CommentSerializer, FeedbackSerializer, ChartDashboardSerializer,
                          ReadCommentSerializer, ChatSerializer)


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

    def get_queryset(self):
        """Superuser can see all access, others can see only theirs own"""
        if self.request.user.is_superuser:
            queryset = Access.objects.all()
        else:
            queryset = Access.objects.filter(owner_id=self.request.user)
        return queryset


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    By URL can be uploaded CSV and JSON files,
    by local can be uploaded CSV, JSON and PDF files
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['user_id__id']

    def create(self, request, *args, **kwargs):
        try:
            serializer = FileSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # type error by URL upload do not work :(
        except ValidationError as error:
            return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': error.detail['link'],
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
        """Superuser can see all files, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = File.objects.all()
        else:
            queryset = get_custom_queryset(File, self.request.user, self.kwargs)
        return queryset


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows feedback messages to be viewed.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filterset_fields = ['user_id__id']

    def get_permissions(self):
        """Edit is forbidden"""
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermissionSafe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    def get_queryset(self):
        """Superuser can see all feedback, others can see theirs own"""
        if self.request.user.is_superuser:
            queryset = Feedback.objects.all()
        else:
            queryset = Feedback.objects.filter(user_id=self.request.user)
        return queryset


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
        """Superuser can see all dashboards, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Dashboard.objects.all()
        else:
            queryset = get_custom_queryset(Dashboard, self.request.user, self.kwargs)
        return queryset


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
        #print('**datas',**datas)
        return serializer.save(**datas)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DataAccessPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Superuser can see all charts, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Chart.objects.all()
        else:
            queryset = get_custom_queryset(Chart, self.request.user, self.kwargs)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all().order_by('-date_send')
    serializer_class = CommentSerializer
    filterset_fields = ['user_id__id']
    permission_classes = [IsAuthenticated, CommentAccessPermission]

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if can_comment(request, serializer.validated_data):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'message': "You have no access to comment",
            })

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        print(self.permission_classes)
        return serializer.save(user_id=self.request.user, **datas)


class ReadCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comment reading to be viewed or edited.
    Probably does not fully work for now.
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
    API endpoint that allows chat messages to be viewed or edited.
    """
    queryset = Chat.objects.filter(is_remove=False).order_by('-date_send')
    serializer_class = ChatSerializer

    # should be added some special permissions
    permission_classes = [IsAuthenticated]

    filterset_fields = ['user_id_owner__id', 'user_id_sender__id', 'date_send']

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
        return serializer.save(user_id_sender=self.request.user, **datas)


class ChartDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = ChartDashboard.objects.all()
    serializer_class = ChartDashboardSerializer
    permission_classes = [IsAuthenticated]
