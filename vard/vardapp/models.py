from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError('User must have an email adress')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(email=email,**kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self,email,password=None,**kwargs):
        user = self.create_user(email,password=password,**kwargs)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_password_change = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'



