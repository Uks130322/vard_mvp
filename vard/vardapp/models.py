from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
#from appquery.models import ClientDB

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
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_password_change = models.DateTimeField(auto_now=True)
    password = models.CharField(_("password"), max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.id}'




# class Chart(models.Model):
#     # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='chart id')
#     user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='user id')
#     date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
#     date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
#     clientdb_id = models.ForeignKey(ClientDB, on_delete=models.CASCADE, verbose_name='user id')
#     str_query = models.TextField(blank=True)