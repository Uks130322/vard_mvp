from django.core.validators import FileExtensionValidator
from django.db import models

from appfile.utils import user_directory_path
from appuser.models import User


class File(models.Model):

    class Publish(models.IntegerChoices):
        NO = 0
        YES = 1

    class Place(models.IntegerChoices):
        Community = 1
        MyFiles = 2
        BestPractices = 3

    class FilesType(models.IntegerChoices):
        """By URL can be uploaded CSV and JSON files, by local can be uploaded CSV, JSON and PDF files"""
        CSV = 1
        JSON = 2
        PDF = 3
        # EXCEL = 4
        # ... = 5

        def __str__(self):
            return self.value

    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='file id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name='user id')
    place_id = models.IntegerField(choices=Place.choices, default=2, null=False, verbose_name='id of place file')
    type_id = models.IntegerField(choices=FilesType.choices, null=False, verbose_name='id type of file', )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    date_delete = models.DateTimeField(blank=True, null=True, verbose_name='date of delete')
    name = models.CharField(max_length=255, blank=True, verbose_name='name of file')
    link = models.FileField(upload_to=user_directory_path, blank=True, verbose_name='link of file',
                            validators=[FileExtensionValidator(allowed_extensions=['pdf', 'csv', 'json'])])
    publish = models.IntegerField(choices=Publish.choices, default=0)

    def __str__(self):
        return f'{self.name}, id={self.user_id}'
