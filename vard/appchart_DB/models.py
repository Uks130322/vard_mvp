from django.db import models
from sqlalchemy import exc
from sqlcredits import LISTSUBD, SQLCREDITS, EXTENSIONS
from appuser.models import User


class Dashboard(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='dashboard id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    chart = models.ManyToManyField('Chart', blank=True, through='ChartDashboard')

    def __str__(self):
        return f'{self.id} {self.user_id}'


class ClientDB(models.Model):
    driver1 = 1
    driver2 = 2
    driver3 = 3
    driver4 = 4

    DRIVERS = [
        (driver1, 'MSSQL', SQLCREDITS['MSSQL-HOSTING']),  ##### "driver": "mssql+pyodbc", "driver2": "ODBC+Driver+17+for+SQL+Server",
        (driver2, 'MYSQL', SQLCREDITS['MYSQLROOT-HOSTING']),
        (driver3, 'MARIADB', SQLCREDITS['MARIADB-HOSTING']),
        (driver4, 'POSTGRES', SQLCREDITS['POSTGRES-HOSTING']),
    ]

    dbtype1 = 1
    dbtype2 = 2
    dbtype3 = 3
    dbtype4 = 4

    DBTYPE = [
        (driver1, 'MSSQL'),
        (driver2, 'MYSQL'),
        (driver3, 'MARIADB'),
        (driver4, 'POSTGRES'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    connection_name = models.CharField(max_length=255, null=False)
    url = models.CharField(max_length=255, blank=True, null=True)
    data_base_type = models.CharField(choices=DBTYPE, blank=True, null=True)
    driver = models.IntegerField(choices=DRIVERS, blank=True, null=True) ##### пока не надо, понадобится если на 1 субд пользователь будет выбирать из несколькких драйверов
    user_name = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    host = models.CharField(max_length=60, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    data_base_name = models.CharField(max_length=63, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    #str_datas_for_connection = models.CharField(max_length=255, blank=True, null=True) ##### не надо. вместо неё url

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

    def get_status_db(self):
        pass

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
