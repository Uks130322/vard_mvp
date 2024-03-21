from django.db import models
#from vardapp.models import Users

#import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import re
import json

class DataBaseQuery(models.Model):
    def __init__(self,driver, user_name, password, url,host,port, data_base_name, data_base_type, description, str_query):
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

    def create_host(self):
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

    def get_engine(self):
        password_new = self.password.replace('@', '%40')
        password_new = re.escape(password_new)
        host_new = self.create_host()
        engine = create_engine(f"{self.driver}://{self.user_name}:{password_new}@{host_new}/{self.data_base_name}", echo=False)
        return engine

    @property
    def get_query(self):
        subjects = []
        engine = self.get_engine()
        Session = sessionmaker(autoflush=False, bind=engine)
        with Session(autoflush=False, bind=engine) as db:
            rows = db.execute(text(self.str_query)).fetchall()
            data = [r._asdict() for r in rows]
            #json_data = json.dumps(data)
        return data  #json_data





#     driver1 = 1
#     DRIVERS = [
#         (driver1, 'SQLAlchemy'),
#     ]
#     #ENGINES = {'SQLAlchemy';''}
#
#     user_id = models.ForeignKey(Users , on_delete=models.CASCADE, null=False) # like '[0-9a-zA-Z_][0-9a-zA-Z_-]%'
#     user_name = models.CharField(min_length=1, max_length=16, null=False) #
#     password = models.CharField(min_length=8, max_length=128, null=False) #
#     driver = models.CharField(max_length='255', null=False, choices=DRIVER, default=engine) #
#     url = models.CharField(null=True) #host может быть как именем хоста, так и IP-адресом
#     host = models.CharFieldField(null=False, default='localhost') #host может быть как именем хоста, так и IP-адресом
#     port = models.IntegerFieldField(null=False, default=3306) #
#     data_base_type = models.CharField(max_length=255, null=False) #что это??? OPTIONS???
#     data_base_name = models.CharField(max_length=63, null=False) # like '%[0-9a-zA-Z_-]%' # Имена mysql, sys, information_schema и performance_schema запрещены
#     description = models.CharField(max_length=255, null=False) #
#     OPTIONS = models.CharField(max_length=255, null=False, default="""'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}""")
#
#
# # https://sky.pro/media/podklyuchenie-k-baze-dannyh-mysql-s-pomoshhyu-python/
# # install mysql-connector-python
# import mysql.connector
# cnx = mysql.connector.connect(user='username', password='password',
#                               host='hostname',
#                               database='database_name')
# cnx.close()


# https://metanit.com/python/database/3.1.php
# pip install SQLAlchemy




