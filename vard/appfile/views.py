from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appchart_DB.permissions import get_custom_queryset, DataAccessPermission
from appfile.models import File
from appfile.serializers import FileSerializer


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
