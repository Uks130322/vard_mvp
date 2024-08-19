from django.db import models
from appuser.models import User
import uuid
import hashlib


class Invite(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(primary_key=True, max_length=128, unique=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    date_invite = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id







