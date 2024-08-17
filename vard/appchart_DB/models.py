from django.db import models
from appuser.models import User
from appchart_DB.sqlcredits import EXTENSION_DIC, DATABASETYPE_DIC

class ClientDB(models.Model):

    DBTYPE = []
    for dic in DATABASETYPE_DIC:
        if dic['is_available']:
            tuple = (dic['id'], dic['name'])
            DBTYPE.append(tuple)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    connection_name = models.CharField(max_length=255, null=False)
    data_base_type = models.CharField(choices=DBTYPE, null=False)
    url = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    host = models.CharField(max_length=60, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    data_base_name = models.CharField(max_length=63, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.connection_name}'


class ClientData(models.Model):
    # charts_id = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='charts id', null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.data}'


class Chart(models.Model):
    EXTENSIONS = []
    for dic in EXTENSION_DIC:
        if dic['is_available']:
            tuple = (dic['id'], dic['name'])
            EXTENSIONS.append(tuple)

    class PlotType(models.IntegerChoices):
        PLOT = 1
        SCATTER = 2
        BAR = 3
        PIE = 4
        STACKPLOT = 5

    class Color(models.TextChoices):
        RED = '#F15C3C'
        GREEN = '#8FC73C'
        BLUE = '#26ADE1'
        PURPLE = '#DE4AF0'
        YELLOW = '#FCD205'
        GREY = '#6C6C6C'

    class ImageFormat(models.IntegerChoices):
        PNG = 1
        PS = 2
        PDF = 3
        SVG = 4

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    clientdb_id = models.ForeignKey(ClientDB, on_delete=models.PROTECT, verbose_name='clientdb id')
    str_query = models.TextField(blank=True, verbose_name='query')
    clientdata = models.OneToOneField(ClientData, on_delete=models.CASCADE, verbose_name='clientdata')

    x_data = models.CharField(blank=True, null=True, max_length=100, verbose_name='x data')
    y_data = models.CharField(blank=True, null=True, max_length=100, verbose_name='y data')
    x_label = models.CharField(blank=True, null=True, max_length=100, default='X', verbose_name='x label')
    y_label = models.CharField(blank=True, null=True, max_length=100, default='y', verbose_name='y label')
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name='title')

    plot_type = models.IntegerField(choices=PlotType.choices, default=0, verbose_name='plot type')
    color = models.CharField(max_length=15, choices=Color.choices, default=Color.BLUE, verbose_name='color')
    image_format = models.IntegerField(choices=ImageFormat.choices, default=0, verbose_name='image format')
    plot = models.TextField(blank=True, null=True, verbose_name='plot_in_base64')

    extension = models.IntegerField(choices=EXTENSIONS, default=1)

    def __str__(self):
        return f'{self.id} {self.user_id}'


class Dashboard(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='dashboard id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    #extension = models.IntegerField(choices=EXTENSIONS, default=1)
    data = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    chart = models.ManyToManyField(Chart, blank=True, through='ChartDashboard')

    def __str__(self):
        return f'{self.id} {self.user_id}'


class ChartDashboard(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
