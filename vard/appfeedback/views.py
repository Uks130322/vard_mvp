from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from appchart_DB.permissions import DataAccessPermissionSafe
from appfeedback.models import Feedback
from appfeedback.serializers import FeedbackSerializer


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
