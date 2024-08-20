from django.db import models
from appuser.models import User
import uuid
import hashlib


class Invite(models.Model):
    """надо сделать 1 справочник на invite и на access"""
    class AccessType(models.IntegerChoices):
        READER = 1
        # OWNER = 2    # not used
        COMMENTATOR = 3
        EDITOR = 4

    id = models.CharField(primary_key=True, max_length=128, unique=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    access_type_id = models.IntegerField(choices=AccessType.choices, null=False)
    date_invite = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner_id', 'email')

    def __str__(self):
        return self.id







