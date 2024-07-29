from django.db import models

from appuser.models import User


class Chat(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_id_owner')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_id_sender')
    date_send = models.DateTimeField(auto_now_add=True)
    date_remove = models.DateTimeField(auto_now=True)
    is_remove = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.id} {self.user_id}'


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_send = models.DateTimeField(auto_now_add=True)
    date_remove = models.DateTimeField(auto_now=True)
    is_remove = models.BooleanField(null=False, default=False)
    message = models.TextField()
    doc = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.user_id}'
