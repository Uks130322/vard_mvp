
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import exc
import pandas as pd
import pyodbc
from sqlcredits import LISTSUBD, SQLCREDITS, EXTENSIONS
import json
import base64
import os
import uuid
import io
from io import StringIO, BytesIO


MEDIA_DIR = 'C:\\pitonprojekt\\vard_mvp\\vard\media'
TEMP_FILES_DIR = MEDIA_DIR+'\\temp_files\\'

#url, user_name, password, host, port, data_base_name, str_query
class Work:
    def __init__(self, **kwargs):
        self.SUBDja = kwargs["SUBDja"]
        self.SUBD = self.set_subd
        self.driver = SQLCREDITS[self.SUBD]["driver"]
        self.driver2 = SQLCREDITS[self.SUBD]["driver2"]
        self.user = SQLCREDITS[self.SUBD]["user"]
        self.pwd = SQLCREDITS[self.SUBD]["pwd"]
        self.hostname = SQLCREDITS[self.SUBD]["hostname"]
        self.port = SQLCREDITS[self.SUBD]["port"]
        self.bdname = kwargs["bdname"]
        self.dbname = self.set_dbname
        self.datadir = SQLCREDITS[self.SUBD]["volumes"]["DATA_DIR"]
        self.logdir = SQLCREDITS[self.SUBD]["volumes"]["LOG_DIR"]
        self.backupdir = SQLCREDITS[self.SUBD]["volumes"]["BACKUP_DIR"]
        self.echo = False #True #False
        self.connection = self.get_string_connection
        self.engine = self.get_engine
        self.querykw = kwargs["query"]
        self.query = self.set_query
        self.ext = kwargs["ext"]
        self.extension = self.set_extension
        self.filename = self.set_filename
        self.path = self.set_path
        self.status = self.set_status

    @property
    def set_status(self):
        if self.querykw:
            self.status = 'ok'
        else:
            self.status = 'test connection'
        return self.status

    @property
    def set_query(self):
        if self.querykw:
            self.query = self.querykw
        else:
            self.query = "select 1"
        return self.query

    @property
    def set_subd(self):
        if self.SUBDja in LISTSUBD:
            return self.SUBDja
        else:
            self.SUBDja = 'ERROR'
            return self.SUBDja

    @property
    def set_extension(self):
        if self.ext in EXTENSIONS:
            return self.ext
        else:
            return f'filetype {self.ext} not supported yet'

    @property
    def set_dbname(self):
        if self.bdname:
            self.dbname = self.bdname
        else:
            self.dbname = SQLCREDITS[self.SUBD]["dbname"]
        return self.dbname

    @property
    def get_string_connection(self):
        if self.SUBD == "MSSQL-DOCKER" or self.SUBD == "MSSQL-HOSTING" :
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}{self.driver2}"
        elif self.SUBD in ("MYSQLROOT-DOCKER", "MYSQLROOT-HOSTING", "MYSQL-DOCKER", "MYSQL-HOSTING"):
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}"
        elif self.SUBD in ("POSTGRES-DOCKER", "POSTGRES-HOSTING"):
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}"
        elif self.SUBD in ("MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING"):
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}"
        else:
            self.connection = None
        return self.connection

    @property
    def get_engine(self):
        if self.SUBD == "MSSQL-DOCKER" or self.SUBD == "MSSQL-HOSTING" :
            try:
                self.engine = create_engine(self.connection, fast_executemany=True, echo=self.echo).execution_options(isolation_level="AUTOCOMMIT")
            except Exception as e:
                print(format(e))
                self.engine = None
        elif self.SUBD in ("MYSQLROOT-DOCKER", "MYSQLROOT-HOSTING", "MYSQL-DOCKER", "MYSQL-HOSTING","POSTGRES-DOCKER","POSTGRES-HOSTING",
                           "MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING"):
            try:
                self.engine = create_engine(self.connection, echo=self.echo)
            except Exception as e:
                print(format(e))
                self.engine = None
        else:
            self.engine = None
        return self.engine

    def file_b64encode(self, file):
        with open(file, mode='rb') as file:
            f = file.read()
        encoded = base64.b64encode(f)
        return encoded

    def file_b64decode(self, file):
        decoded = base64.b64decode(file)
        return decoded

    @property
    def set_filename(self):
        self.filename = uuid.uuid4()
        return self.filename

    @property
    def set_path(self):
        self.path = f'{TEMP_FILES_DIR}{self.filename}.{self.extension}'
        return self.path

    def data_to_file(self, rows):
        if self.extension == 'xlsx':
            pd.DataFrame(rows).to_excel(self.path)
            result = self.file_b64encode(self.path)
            os.remove(self.path)
            return result
        elif self.extension == 'json':
            data = [row._asdict() for row in rows]
            json_data = json.dumps(data)
            result = base64.b64encode(json_data.encode('utf-8'))

            return result
        elif self.extension == 'csv':
            pd.DataFrame(rows).to_csv(self.path, sep='\t', encoding='utf-8', index=False, header=True, float_format='%.2f')
            result = self.file_b64encode(self.path)
            os.remove(self.path)
            return result
        else:
            return False

    def get_result(self):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            sql = text(self.query)
            try:
                rows = db.execute(sql).all()
                encoded = self.data_to_file(rows)
                self.rezult = {'http_code': 200,'status': self.status, 'name': f'{self.filename}', 'rezult': encoded, 'extension': self.extension, 'countrows': len(rows)}
            except Exception as e:
                if format(e).find('This result object does not return rows') >= 0:
                    self.rezult = {'http_code': 204,'status': self.status, 'name': '', 'result': format(e), 'extension': '', 'query': self.query, 'countrows': 0}
                else:
                    self.rezult = {'http_code': 400,'status': 'error', 'name': '', 'result': format(e), 'extension': '', 'query': self.query, 'countrows': None}
            return self.rezult


L = ["MSSQL-DOCKER","MSSQL-HOSTING","MYSQLROOT-DOCKER","MYSQLROOT-HOSTING","MYSQL-DOCKER","MYSQL-HOSTING",
     "MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING","POSTGRES-DOCKER","POSTGRES-HOSTING",]


#url, user_name, password, host, port, data_base_name, str_query
#Work(SUBDja="MYSQLROOT-DOCKER", bdname="", query="select 'fff' as j", ext="csv")
x = Work(SUBDja="MYSQLROOT-DOCKER", bdname="", query="select 'fff' as j", ext="csv").get_result();
print(x)


# from django.db import models
#
# class ModelDeal(models.Model):
#     STATUS_CHOISES = (
#         ('ok', 'Выполнена'),
#         ('new', 'Новая заявка'),
#         ('cancel', 'Отменена'),
#         ('error', 'Ошибка'),
#         ('timesup', 'Время вышло'),
#     )
#     deal_status = models.CharField('Статус', max_length=50, choices=STATUS_CHOISES, default='new')
#
# var = ModelDeal.return_choises()
# print(var)

