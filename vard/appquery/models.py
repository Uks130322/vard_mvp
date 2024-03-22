from django.db import models
from vardapp.models import Users
#import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import re


class DataBaseQuery(models.Model):
    def __init__(self, user_id, driver, user_name, password, url,host,port, data_base_name, data_base_type, description, str_query):
        self.user_id = user_id  #Users.objects.get(id = 1).id
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

    def get_query(self):
        subjects = []
        engine = self.get_engine()
        Session = sessionmaker(autoflush=False, bind=engine)
        with Session(autoflush=False, bind=engine) as db:
            rows = db.execute(text(self.str_query)).fetchall()
            user = [{'user_id':self.user_id}]
            result = user + [r._asdict() for r in rows]
        return result

    @property
    def get_responces(self):
        if not self.str_query or self.str_query is None or self.str_query == '':
            result  = [{'user_id':self.user_id}]
        else:
            result  = self.get_query()
        return result









