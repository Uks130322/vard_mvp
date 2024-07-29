from django.contrib import admin

from .models import Comment, ReadComment

admin.site.register(Comment)
admin.site.register(ReadComment)
