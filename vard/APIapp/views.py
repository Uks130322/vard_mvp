from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from vardapp.models import *
from .permissions import FileAccessPermission, GiveAccessPermission
from .serializers import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class AccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Access to be viewed or edited. Only Owner can change access level.
    """
    queryset = Access.objects.all()
    serializer_class = AccessSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, GiveAccessPermission]
        return [permission() for permission in permission_classes]


class FileViewSet(viewsets.ModelViewSet):
    """
    User should see the list of all his files. If he got permission, he can see others users'
    files by detail, not the list
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['user_id__id']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, FileAccessPermission]
        return [permission() for permission in permission_classes]


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows feedback messages to be viewed or edited.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]


class DashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    filterset_fields = ['user_id__id']
    permission_classes = [IsAuthenticated]


class ChartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows charts to be viewed or edited.
    """
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    filterset_fields = ['user_id__id']
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all().order_by('-date_send')
    serializer_class = CommentSerializer
    filterset_fields = ['user_id__id']
    permission_classes = [IsAuthenticated]


class ReadCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comment reading to be viewed or edited.
    """
    queryset = ReadComment.objects.all().order_by('-date_reading')
    serializer_class = ReadCommentSerializer
    permission_classes = [IsAuthenticated]
