from django.db import models
from vardapp.models import Users
#import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy import exc
import re
import json
#import datetime



class ClientDB(models.Model):
    driver1 = 1
    DRIVERS = [
        (driver1, 'SQLAlchemy for MySQL'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    connection_name = models.CharField(max_length=255, null=False, default='')
    user_name = models.CharField(max_length=16, null=False)
    password = models.CharField(max_length=128, null=False)
    driver = models.IntegerField(choices=DRIVERS, default=driver1)
    url = models.CharField(max_length=255, null=True)
    host = models.CharField(max_length=60, null=True, default='localhost')
    port = models.IntegerField(null=True, default=3306)
    data_base_type = models.CharField(null=True, max_length=255)
    data_base_name = models.CharField(max_length=63,null=False)
    description = models.CharField(null=True, max_length=255)
    str_connection = models.CharField(blank=True, null=True, max_length=255)

    # def get_host(self):
    #     if self.host == 'localhost' or self.host == '127.0.0.1':
    #         result = self.host
    #     elif self.port == '' or self.port is None or not self.port:
    #         result = f'{self.url}:3306'
    #     else:
    #         result = f'{self.url}:{self.port}'
    #     return result
    #
    # @property
    # def get_str_connect_sqlalchemy(self):
    #     password_new = self.password.replace('@', '%40')
    #     password_new = re.escape(password_new)
    #     host_new = self.get_host()
    #     str_connect = f"mysql://{self.user_name}:{password_new}@{host_new}/{self.data_base_name}"
    #     return str_connect

    # def get_engine_sqlalchemy(self, url, host, port, password, driver, user_name, data_base_name):
    #     if driver == 1:
    #         str_connect_new = self.get_str_connect_sqlalchemy(url, host, port, password, user_name, data_base_name)
    #     else:
    #         str_connect_new = ''
    #     engine = create_engine(f"{str_connect_new}", echo=False)
    #     return engine
    #
    # def get_query(self, user_id, url, host, port, password, driver, user_name, data_base_name, str_query):
    #     engine = self.get_engine_sqlalchemy(url, host, port, password, driver, user_name, data_base_name)
    #     Session = sessionmaker(autoflush=False, bind=engine)
    #     with Session(autoflush=False, bind=engine) as db:
    #         rows = db.execute(text(str_query)).fetchall()
    #         data = [r._asdict() for r in rows]
    #         keys_list = [set(r._asdict().keys()) for r in rows][0]
    #         fieldname = []
    #         for i in keys_list:
    #             fieldname.append(i)
    #         result = {'user_id': user_id, 'fieldname': fieldname, 'data': data, 'error': None}
    #     return result

    def get_responces(self, id):
        try:
            user = Users.objects.get(id=self.user.id)
            connect = ClientDB.objects.get(id = id)
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

    def update_responce(self, id):
        # def datetime_handler(x):
        #     if isinstance(x, datetime.datetime):
        #         return x.isoformat()
        #     raise TypeError("Unknown type")
        user = Users.objects.get(id=self.user.id)
        result = self.get_responces(id)
        # json_string = json.dumps(result, default=datetime_handler)
        #ClientDB.objects.filter(id=id).update(result_query=result)
        return result

    def __str__(self):
        return f'{self.connection_name}'


class Chart(models.Model):
    # id = models.AutoField(primary_key=True, blank=False, null=False, unique=True, verbose_name='chart id')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='user id')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    date_change = models.DateTimeField(auto_now=True, verbose_name='date of change')
    clientdb_id = models.ForeignKey(ClientDB, on_delete=models.CASCADE, verbose_name='clientdb id')
    str_query = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user_id}'


class ClientData(models.Model):
    chart = models.OneToOneField(Chart, on_delete=models.CASCADE)
    data = models.TextField(blank=True, null=True)


#--------------------------------------
class DataBaseQuery(models.Model):  #DataBaseQuery  ClientData
    def __init__(self, user_id, driver, user_name, password, url,host,port, data_base_name, data_base_type, description, str_query):
        self.user_id = user_id
        self.driver = driver
        self.user_name = user_name
        self.password = password
        self.url = url
        self.host = host
        self.port = port
        self.data_base_name = data_base_name
        self.data_base_type = data_base_type
        self.description = description
        self.str_query = str_query

    def get_host(self):
        """
            сначала подключаемся к локальному хосту. поэтому сначала проверяем на валидность локальный хост, если он невалиден,
            проверяем порт и подключаемся к удалённому url.
            у mysql по умолчанию порт = 3306. если порт не указан, устанавливаем 3306.
            эта проверка нужна тк в result-е стоит двоеточие : f'{self.url}:{self.port}
            если url неправилен, то бд вернёт ошибку,т.е. дополнительно его проверять не нужно
            """
        if self.host == 'localhost' or self.host == '127.0.0.1':
            result = self.host
        elif self.port == '' or self.port is None or not self.port:
            result = f'{self.url}:3306'
        else:
            result = f'{self.url}:{self.port}'
        return result

    def get_str_connect(self):
        password_new = self.password.replace('@', '%40')
        password_new = re.escape(password_new)
        host_new = self.get_host()
        str_connect = f"{self.driver}://{self.user_name}:{password_new}@{host_new}/{self.data_base_name}"
        return str_connect

    def get_engine(self):
        str_connect_new = self.get_str_connect()
        engine = create_engine(f"{str_connect_new}", echo=False)
        return engine

    def create_data_base(self):
        str_connect_new = self.get_str_connect()
        if not database_exists(f"{str_connect_new}"):
            create_database(f"{str_connect_new}")
            return f'{self.data_base_name} создана'
        else:
            return f'{self.data_base_name} уже существует'

    def drop_data_base(self):
        str_connect_new = self.get_str_connect()
        if database_exists(f"{str_connect_new}"):
            drop_database(f"{str_connect_new}")
            return f'{self.data_base_name} удалена'
        else:
            return f'{self.data_base_name} не найдена'

    def get_query(self):
        engine = self.get_engine()
        Session = sessionmaker(autoflush=False, bind=engine)
        with Session(autoflush=False, bind=engine) as db:
            rows = db.execute(text(self.str_query)).fetchall()
            user = [{'user_id':self.user_id}]
            result = user + [r._asdict() for r in rows]
        return result

    @property
    def get_responces(self):
        try:
            if not self.str_query or self.str_query is None or self.str_query == '':
                result = [{'user_id': self.user_id}]
            else:
                result = self.get_query()
            return result
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return [{'user_id': self.user_id}, {'error': f'{error}'}]










