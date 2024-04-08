from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from vardapp.utils import user_directory_path


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            password=password,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email=email,
            password=password,
            **kwargs
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='user id')
    name = models.CharField(max_length=255, verbose_name='name of user')
    email = models.EmailField(unique=True, max_length=255, verbose_name='email of user')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of sign up')
    date_password_change = models.DateTimeField(auto_now=True, verbose_name='date of password change')
    password = models.CharField(_("password"), max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.email}'


class Access(models.Model):

    class AccessType(models.IntegerChoices):
        READER = 1
        OWNER = 2
        COMMENTATOR = 3
        EDITOR = 4

    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='access id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='user id')
    file_id = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='file id')
    access_type_id = models.IntegerField(choices=AccessType.choices, null=False, verbose_name='access type id')
    date_access_open = models.DateTimeField(auto_now=True, verbose_name='date access open')
    date_access_close = models.DateTimeField(auto_now=True, verbose_name='date access close')


class File(models.Model):

    class Publish(models.IntegerChoices):
        NO = 0
        YES = 1

    class Place(models.IntegerChoices):
        Community = 1
        MyFiles = 2
        BestPractices = 3

    class FilesType(models.IntegerChoices):
        CSV = 1
        JSON = 2
        PDF = 3
        # EXCEL = 4
        # ... = 5

        def __str__(self):
            return self.value

    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='file id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='user id')
    place_id = models.IntegerField(choices=Place.choices, default=2, null=False, verbose_name='id of place file')
    type_id = models.IntegerField(choices=FilesType.choices, null=False, verbose_name='id type of file', )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    date_delete = models.DateTimeField(blank=True, null=True, verbose_name='date of delete')
    name = models.CharField(max_length=255, blank=True, verbose_name='name of file')
    link = models.FileField(upload_to=user_directory_path, blank=True, verbose_name='link of file')
    publish = models.IntegerField(choices=Publish.choices, default=0)


class Feedback(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='feedback id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    theme = models.CharField(max_length=255, verbose_name='theme of feedback')
    description = models.TextField(verbose_name='feedback')


class Dashboard(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='dashboard id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')


class Chart(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='chart id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')


class Comment(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name = 'publish id')
    file_id = models.ForeignKey('File', on_delete=models.CASCADE, null=True, verbose_name='cells id')
    chart_id = models.ForeignKey('Chart', on_delete=models.CASCADE, null=True, verbose_name='chart id')
    dashboard_id = models.ForeignKey('Dashboard', on_delete=models.CASCADE, null=True, verbose_name='dashboard id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user id')
    date_send = models.DateTimeField(auto_now_add=True, verbose_name='date of send')
    date_remove = models.DateTimeField(auto_now_add=True, verbose_name='date of remove')
    date_delivery = models.DateTimeField(auto_now_add=True, verbose_name='date of delivery')
    comment = models.TextField(verbose_name='comment')


class ReadComment(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='id')
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='id of comment')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='id of user')
    date_reading = models.DateTimeField(auto_now_add=True, verbose_name='date of read')
