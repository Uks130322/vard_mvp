from django.db import models
from sqlalchemy import exc
#from appchart_DB.sqlcredits import LISTSUBD, SQLCREDITS, EXTENSIONS
from appuser.models import User
from appchart_DB.sqlcredits import EXTENSION_DIC, DATABASETYPE_DIC

class Dashboard(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='dashboard id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    chart = models.ManyToManyField('Chart', blank=True, through='ChartDashboard')

    def __str__(self):
        return f'{self.id} {self.user_id}'


class ClientDB(models.Model):

    DBTYPE = []
    for dic in DATABASETYPE_DIC:
        if dic['is_available']:
            tuple = (dic['id'], dic['name'])
            DBTYPE.append(tuple)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    connection_name = models.CharField(max_length=255, null=False)
    data_base_type = models.CharField(choices=DBTYPE, null=False)
    #driver = models.IntegerField(choices=DRIVERS, default=1)
    url = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    host = models.CharField(max_length=60, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    data_base_name = models.CharField(max_length=63, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.connection_name}'


class Chart(models.Model):
    EXTENSIONS = []
    for dic in EXTENSION_DIC:
        if dic['is_available']:
            tuple = (dic['id'], dic['name'])
            EXTENSIONS.append(tuple)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    clientdb_id = models.ForeignKey(ClientDB, on_delete=models.PROTECT, verbose_name='clientdb id')
    str_query = models.TextField(blank=True)
    clientdata = models.OneToOneField('ClientData', on_delete=models.CASCADE)
    extension = models.IntegerField(choices=EXTENSIONS, default=1)

    def __str__(self):
        return f'{self.id} {self.user_id}'


class ClientData(models.Model):

    # EXTENSIONS = []
    # for dic in EXTENSION_DIC:
    #     if dic['is_available']:
    #         tuple = (dic['id'], dic['name'])
    #         EXTENSIONS.append(tuple)

    #charts_id = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='charts id', null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    #extension = models.IntegerField(choices=EXTENSIONS, default=1)
    data = models.TextField(blank=True, null=True)


class ChartDashboard(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
