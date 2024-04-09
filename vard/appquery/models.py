from django.db import models
from vardapp.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy import exc
import re


class ClientDB(models.Model):
    driver1 = 1
    DRIVERS = [
        (driver1, 'SQLAlchemy for MySQL'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
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
                result = self.get_query(user_id, url, host, port, password, driver, user_name, data_base_name, str_query)
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
    clientdb_id = models.ForeignKey(ClientDB, on_delete=models.CASCADE, verbose_name='clientdb id')
    str_query = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user_id}'


class ClientData(models.Model):
    chart = models.OneToOneField(Chart, on_delete=models.CASCADE)
    data = models.TextField(blank=True, null=True)

