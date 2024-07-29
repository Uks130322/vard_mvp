from django.db import models

from appchart_DB.models import Chart, Dashboard
from appfile.models import File
from appuser.models import User


class Comment(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name = 'publish id')
    file_id = models.ForeignKey(File, on_delete=models.CASCADE, null=True, verbose_name='file id')
    chart_id = models.ForeignKey(Chart, on_delete=models.CASCADE, null=True, verbose_name='chart id')
    dashboard_id = models.ForeignKey(Dashboard, on_delete=models.CASCADE, null=True, verbose_name='dashboard id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    date_send = models.DateTimeField(auto_now_add=True, verbose_name='date of send')
    date_remove = models.DateTimeField(auto_now_add=True, verbose_name='date of remove')
    date_delivery = models.DateTimeField(auto_now_add=True, verbose_name='date of delivery')
    comment = models.TextField(verbose_name='comment')


class ReadComment(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='id')
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='id of comment')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id of user')
    date_reading = models.DateTimeField(auto_now_add=True, verbose_name='date of read')

    class Meta:
        unique_together = ('comment_id', 'user_id')
