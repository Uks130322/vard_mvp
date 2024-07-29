from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            password=make_password(password),
            **kwargs
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **kwargs):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
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
    password = models.CharField(max_length=255, verbose_name='password')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    random_field = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.email}'


class Access(models.Model):

    class AccessType(models.IntegerChoices):
        READER = 1
        # OWNER = 2    # not used
        COMMENTATOR = 3
        EDITOR = 4

    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='access id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='user id',
                                related_name='invited_user')
    owner_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='owner id',
                                 related_name='owner')
    access_type_id = models.IntegerField(choices=AccessType.choices, null=False, verbose_name='access type id')
    date_access_open = models.DateTimeField(auto_now=True, verbose_name='date access open')
    date_access_close = models.DateTimeField(auto_now=True, verbose_name='date access close')

    class Meta:
        unique_together = ('owner_id', 'user_id')
