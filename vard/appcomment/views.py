from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appchart_DB.models import Chart, Dashboard
from appchart_DB.permissions import get_custom_queryset
from appcomment.models import Comment, ReadComment
from appcomment.permissions import CommentAccessPermission, can_comment
from appcomment.serializers import ReadCommentSerializer, CommentSerializer
from appfile.models import File


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all().order_by('-date_send')
    serializer_class = CommentSerializer
    filterset_fields = ['user_id__id', 'file_id', 'chart_id', 'dashboard_id']
    permission_classes = [IsAuthenticated, CommentAccessPermission]

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # checking comment has relation with exactly one table, else 409 error
        valid_file_id = 1 if request.data['file_id'] else 0
        valid_chart_id = 1 if request.data['chart_id'] else 0
        valid_dashboard_id = 1 if request.data['dashboard_id'] else 0
        valid_foreign_keys = valid_file_id + valid_chart_id + valid_dashboard_id

        if can_comment(request, serializer.validated_data) and valid_foreign_keys == 1:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif can_comment(request, serializer.validated_data) and valid_foreign_keys != 1:
            return Response({
                'status': status.HTTP_409_CONFLICT,
                'message': "Comment should have relation with exactly one table: file, chart or dashboard",
            })
        else:
            return Response({
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'message': "You have no access to comment",
            })

    def perform_create(self, serializer):
        """The creator is automatically assigned as user_id"""
        datas = serializer.validated_data
        return serializer.save(user_id=self.request.user, **datas)

    @transaction.atomic
    def get_queryset(self):
        """Superuser can see all comments, others can see theirs own and all with access"""
        if self.request.user.is_superuser:
            queryset = Comment.objects.all()
            return queryset

        if 'pk' in self.kwargs:
            pk = {'pk': self.kwargs['pk']}
            pk.pop('pk', None)
        else:
            pk = self.kwargs
        file = get_custom_queryset(File, self.request.user, pk)
        file_items = Comment.objects.filter(file_id__in=file)
        chart = get_custom_queryset(Chart, self.request.user, pk)
        chart_items = Comment.objects.filter(chart_id__in=chart)
        dashboard = get_custom_queryset(Dashboard, self.request.user, pk)
        dashboard_items = Comment.objects.filter(dashboard_id__in=dashboard)
        queryset = Comment.objects.filter(Q(id__in=file_items) |
                                          Q(id__in=chart_items) |
                                          Q(id__in=dashboard_items)).order_by('-date_send')
        if 'pk' in self.kwargs:
            queryset = Comment.objects.filter(Q(id__in=file_items) |
                                              Q(id__in=chart_items) |
                                              Q(id__in=dashboard_items)).filter(id=self.kwargs['pk'])
        for query in queryset:
            ReadComment.objects.get_or_create(comment_id_id=query.id, user_id_id=query.user_id.id)
        return queryset


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
