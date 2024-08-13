
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import exc
import pandas as pd
import pyodbc
from appchart_DB.sqlcredits import LISTSUBD, SQLCREDITS, EXTENSIONS, DATABASETYPE_DIC, EXTENSION_DIC
import json
import base64
import os
import uuid
import io
from io import StringIO, BytesIO
import os
from pathlib import Path


class Work:
    def __init__(self, data_base_type, url, user_name, password, host, port, data_base_name, str_query, extension):
        self.data_base_type = data_base_type
        self.data_base_type_cleaned = self.set_data_base_type
        self.url = url
        #self.url_cleaned = self.set_url
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.port_cleaned = self.set_port
        self.data_base_name = data_base_name
        self.str_query = str_query
        self.str_query_cleaned = self.set_str_query
        self.extension = extension
        self.extension_cleaned = self.set_extension
        self.extension_cleaned_name = self.set_extension_name
        self.driver_cleaned = self.set_driver
        self.driver2_cleaned = self.set_driver2
        self.echo = False  # True #False
        self.filename = self.set_filename
        self.path = self.set_path
        self.status = self.set_status
        self.engine = self.set_engine

    @property
    def set_data_base_type(self):
        for item in DATABASETYPE_DIC:
            if self.data_base_type == item['id'] and item['is_available']:
                result = self.data_base_type
                break
            else:
                result = 'ERROR'
        return result

    @property
    def set_extension(self):
        for item in EXTENSION_DIC:
            if self.extension == item['id'] and item['is_available']:
                result = self.extension
                break
            else:
                result = f'filetype {self.extension} not supported yet'
        return result

    @property
    def set_extension_name(self):
        for item in EXTENSION_DIC:
            if self.extension_cleaned == item['id']:
                result = item['name']
                break
            else:
                result = f'filetype {self.extension} not supported yet'
        return result

    @property
    def set_port(self):
        for item in DATABASETYPE_DIC:
            if self.data_base_type == item['id'] and item['is_available'] and not self.port:
                result = item['port']
                break
            else:
                result = self.port
        return result

    @property
    def set_status(self):
        if self.str_query:
            self.status = 'ok'
        else:
            self.status = 'test connection'
        return self.status

    @property
    def set_filename(self):
        self.filename = uuid.uuid4()
        return self.filename

    @property
    def set_path(self):
        MEDIA_DIR = os.path.join(Path(__file__).resolve().parent.parent, 'media')
        TEMP_FILES_DIR = os.path.join(MEDIA_DIR, 'temp_files')
        self.path = f'{TEMP_FILES_DIR}/{self.filename}.{self.extension}'
        return self.path

    @property
    def set_str_query(self):
        if self.str_query:
            result = self.str_query
        else:
            result = "select 1"
        return result

    @property
    def set_driver(self):
        for item in DATABASETYPE_DIC:
            if self.data_base_type == item['id'] and item['is_available']:
                result = item['driver']
                break
            else:
                result = 'ERROR'
        return result

    @property
    def set_driver2(self):
        for item in DATABASETYPE_DIC:
            if self.data_base_type == item['id'] and item['is_available']:
                result = item['driver2']
                break
            else:
                result = 'ERROR'
        return result

    #@property
    def set_url(self):
        if self.url:
            result = self.url
        else:
            result = f"{self.driver_cleaned}://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.data_base_name}{self.driver2_cleaned}"
        #print('result--------',result)
        return result

    @property
    def set_engine(self):
        try:
            if self.data_base_type_cleaned == 1:
                """'id': 1, 'name': 'MSSQL SQLAlchemy mssql+pyodbc'"""
                self.engine = create_engine(self.set_url(), fast_executemany=True, echo=self.echo).execution_options(isolation_level="AUTOCOMMIT")
            elif self.data_base_type_cleaned  in [2,3,4]:
                self.engine = create_engine(self.set_url(), echo=self.echo)
            else:
                self.engine = f'{self.url_cleaned} not aviable yet'
        except Exception as e:
            #print(format(e))
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

    def data_to_file(self, rows):
        if self.extension_cleaned_name == 'xlsx':
            pd.DataFrame(rows).to_excel(self.path)
            result = self.file_b64encode(self.path)
            os.remove(self.path)
            return result
        elif self.extension_cleaned_name == 'json':
            data = [row._asdict() for row in rows]
            json_data = json.dumps(data)
            result = base64.b64encode(json_data.encode('utf-8'))
            return result
        elif self.extension_cleaned_name == 'csv':
            pd.DataFrame(rows).to_csv(self.path, sep='\t', encoding='utf-8', index=False, header=True, float_format='%.2f')
            result = self.file_b64encode(self.path)
            os.remove(self.path)
            return result
        else:
            return False

    def get_result(self):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            sql = text(self.str_query)
            try:
                rows = db.execute(sql).all()
                if self.extension_cleaned == 1:
                    encoded = [row._asdict() for row in rows]
                else:
                    encoded = self.data_to_file(rows)
                self.rezult = {'http_code': 200,'status': self.status, 'name': f'{self.filename}', 'result': encoded, 'extension': self.extension_cleaned_name, 'query': self.str_query, 'countrows': len(rows)}
            except Exception as e:
                if format(e).find('This result object does not return rows') >= 0:
                    self.rezult = {'http_code': 204,'status': self.status, 'name': '', 'result': format(e), 'extension': '', 'query': self.str_query, 'countrows': 0}
                else:
                    self.rezult = {'http_code': 400,'status': 'error', 'name': '', 'result': format(e), 'extension': '', 'query': self.str_query, 'countrows': None}
            return self.rezult


L = ["MSSQL-DOCKER","MSSQL-HOSTING","MYSQLROOT-DOCKER","MYSQLROOT-HOSTING","MYSQL-DOCKER","MYSQL-HOSTING",
     "MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING","POSTGRES-DOCKER","POSTGRES-HOSTING",]

SUBD = "MYSQLROOT-DOCKER"
user = SQLCREDITS[SUBD]["user"]
pwd = SQLCREDITS[SUBD]["pwd"]
hostname = SQLCREDITS[SUBD]["hostname"]
port = SQLCREDITS[SUBD]["port"]
bdname = SQLCREDITS[SUBD]["dbname"]
query = "select 'fff' as j"
extension = ""


# x = Work(data_base_type=2, url="", user_name=user, password=pwd, host=hostname, port=port, data_base_name=bdname, str_query=query, extension=extension);
# print(x.get_result())
# print(x.set_engine)



