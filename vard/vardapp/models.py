from sqlalchemy import exc

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator

from vardapp.utils import user_directory_path


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

    # in specification BD was this structure:
    # file_id = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='file id')

    # instead there should be this:
    owner_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='owner id',
                                 related_name='owner')
    access_type_id = models.IntegerField(choices=AccessType.choices, null=False, verbose_name='access type id')
    date_access_open = models.DateTimeField(auto_now=True, verbose_name='date access open')
    date_access_close = models.DateTimeField(auto_now=True, verbose_name='date access close')

    class Meta:
        unique_together = ('owner_id', 'user_id')


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
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='user id')
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
    chart = models.ManyToManyField('Chart', blank=True, through='ChartDashboard')

    def __str__(self):
        return f'{self.id} {self.user_id}'


class Comment(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name = 'publish id')
    file_id = models.ForeignKey('File', on_delete=models.CASCADE, null=True, verbose_name='file id')
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

    class Meta:
        unique_together = ('comment_id', 'user_id')


class ClientDB(models.Model):
    driver1 = 1
    DRIVERS = [
        (driver1, 'SQLAlchemy for MySQL'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    connection_name = models.CharField(max_length=255, null=False, default='')
    user_name = models.CharField(max_length=16, null=False)
    password = models.CharField(max_length=128, null=False)
    driver = models.IntegerField(choices=DRIVERS, default=driver1)
    url = models.CharField(max_length=255, null=True)
    host = models.CharField(max_length=60, null=True, default='localhost')
    port = models.IntegerField(null=True, default=3306)
    data_base_type = models.CharField(null=True, max_length=255)
    data_base_name = models.CharField(max_length=63, null=False)
    description = models.CharField(null=True, max_length=255)
    str_datas_for_connection = models.CharField(blank=True, null=True, max_length=255)

    def get_responses(self, id):
        try:
            user = User.objects.get(id=self.user.id)
            connect = ClientDB.objects.get(id=id)
            user_id = user.id
            url = connect.url
            host = connect.host
            port = connect.port
            password = connect.password
            driver = connect.driver
            user_name = connect.user_name
            data_base_name = connect.data_base_name
            str_query = connect.str_query
            if not str_query or str_query is None or str_query == '':
                result = {'user_id': user_id, 'fieldname': None, 'data': None, 'error': None}
            else:
                result = self.get_query(user_id, url, host, port, password, driver, user_name,
                                        data_base_name, str_query)
            return result
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            result = {'user_id': user_id, 'fieldname': None, 'data': None, 'error': f'{error}'}
            return result

    def update_response(self, id):
        result = self.get_responses(id)
        return result

    def __str__(self):
        return f'{self.connection_name}'


class Chart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    clientdb_id = models.ForeignKey(ClientDB, on_delete=models.PROTECT, verbose_name='clientdb id')
    str_query = models.TextField(blank=True)
    clientdata = models.OneToOneField('ClientData', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} {self.user_id}'


class ClientData(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    data = models.TextField(blank=True, null=True)


class ChartDashboard(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
