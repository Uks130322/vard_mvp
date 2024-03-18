from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


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


class Users(AbstractBaseUser, PermissionsMixin):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='user id')
    name = models.CharField(max_length=255, verbose_name='name of user')
    email = models.EmailField(unique=True, max_length=255, verbose_name='email of user')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of dign up')
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
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='access id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, null=False, verbose_name='user id')
    access_type_id = models.ForeignKey('AccessType', on_delete=models.CASCADE, null=False, verbose_name='access type id')
    file_id = models.ForeignKey('Files', on_delete=models.CASCADE, verbose_name='')
    date_access_open = models.DateTimeField(auto_now = True, verbose_name='date access open')
    date_access_close = models.DateTimeField(auto_now = True, verbose_name='date access close')

class AccessType(models.Model):
    p1 = 1
    p2 = 2
    p3 = 3
    p4 = 4
    POSITIONS = [
        (p1, 'READER'),
        (p2, 'OWNER'),
        (p3, 'COMMENTATOR'),
        (p4, 'EDITOR'),
    ]
    access_type = models.IntegerField(choices = POSITIONS) #, default=p1

class Files(models.Model):
    p0 = 0
    p1 = 1
    POSITIONS = [
        (p0, 'NO'),
        (p1, 'YES'),
    ]
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='file id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, null=False, verbose_name='user id')
    place_id = models.ForeignKey('Place', on_delete=models.CASCADE, null=False, verbose_name='id of place file')
    type_id = models.ForeignKey('FilesType', on_delete=models.CASCADE, null=False, verbose_name='id type of file')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now = True, verbose_name='date of change')
    date_delete = models.DateTimeField(auto_now = True, verbose_name='date of delete')
    name = models.CharField(max_length = 255, verbose_name='name of file')
    link = models.CharField(max_length = 255, verbose_name='link of file')
    publish = models.IntegerField(choices = POSITIONS, default=p0)

class Place(models.Model):
    p1 = 1
    p2 = 2
    p3 = 3
    POSITIONS = [
        (p1, 'Community'),
        (p2, 'My Files'),
        (p3, 'Best Practices'),
    ]
    type = models.IntegerField(choices = POSITIONS) #, default=p1

class FilesType(models.Model):
    p1 = 1
    p2 = 2
    p3 = 3
    p4 = 4
    p5 = 5
    POSITIONS = [
        (p1, 'CSV'),
        (p2, 'JSON'),
        (p3, 'EXCEL'),
        (p4, 'PDF'),
        (p5, '...'),
    ]
    files_type = models.IntegerField(choices = POSITIONS) #, default=p1

class Feedback(models.Model):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='feedback id')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    theme = models.CharField(max_length=255, verbose_name='theme of feedback')
    description = models.TextField(verbose_name='feedback')


class Dushboards(models.Model):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='dushboard id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')

class Charts(models.Model):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='charts id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')

class Comments(models.Model):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name = 'publish id')
    file_id = models.ForeignKey('Files', on_delete=models.CASCADE, null=False, verbose_name='cells id')
    chart_id = models.ForeignKey('Charts', on_delete=models.CASCADE, null=False, verbose_name='chart id')
    dushboard_id = models.ForeignKey('Dushboards', on_delete=models.CASCADE, null=False, verbose_name='dushboard id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='user id')
    date_send = models.DateTimeField(auto_now_add=True, verbose_name='date of send')
    date_remove = models.DateTimeField(auto_now_add=True, verbose_name='date of remove')
    date_delivery = models.DateTimeField(auto_now_add=True, verbose_name='date of delivery')
    comment = models.TextField(verbose_name='comment')

class ReadComments(models.Model):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='id')
    comment_id = models.ForeignKey('Comments', on_delete=models.CASCADE, verbose_name='id of comment')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='id of user')
    date_reading = models.DateTimeField(auto_now_add=True, verbose_name='date of read')



