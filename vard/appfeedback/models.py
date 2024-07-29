from django.db import models

from appuser.models import User


class Feedback(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='feedback id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    theme = models.CharField(max_length=255, verbose_name='theme of feedback')
    description = models.TextField(verbose_name='feedback')
