from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from vardapp.models import *
from appchat.models import Chat
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class AccessViewSet(viewsets.ModelViewSet):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
    permission_classes = [AllowAny]


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('name')
    serializer_class = FileSerializer
    permission_classes = [AllowAny]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [AllowAny]


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-date_send')
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class ReadCommentViewSet(viewsets.ModelViewSet):
    queryset = ReadComment.objects.all().order_by('-date_reading')
    serializer_class = ReadCommentSerializer
    permission_classes = [AllowAny]


class FileUserViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer

    def get_queryset(self):
        u1 = self.request.user
        if u1.id is not None:
            queryset = File.objects.filter(user_id=u1).order_by('id')
        else:
            queryset = []
        return queryset


class CommentUserViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        u1 = self.request.user
        if u1.id is not None:
            queryset = Comment.objects.filter(user_id=u1).order_by('id')
        else:
            queryset = []
        return queryset


class DashboardUserViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer

    def get_queryset(self):
        u1 = self.request.user
        if u1.id is not None:
            queryset = Dashboard.objects.filter(user_id=u1).order_by('id')
        else:
            queryset = []
        return queryset


class ChartUserViewSet(viewsets.ModelViewSet):
    serializer_class = ChartSerializer

    def get_queryset(self):
        u1 = self.request.user
        if u1.id is not None:
            queryset = Chart.objects.filter(user_id=u1).order_by('id')
        else:
            queryset = []
        return queryset


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all().order_by('-date_send')
    serializer_class = ChatSerializer
    permission_classes = [AllowAny]

