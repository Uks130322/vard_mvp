from django.db import models
from vardapp.models import User


class Chat(models.Model):
    user_id_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_id_owner')
    user_id_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_id_sender')
    date_send = models.DateTimeField(auto_now_add=True)
    date_remove = models.DateTimeField(auto_now=True)
    is_remove = models.BooleanField(null=False,default=False)
    message = models.TextField()


