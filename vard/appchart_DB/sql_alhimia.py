
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import exc
import pandas as pd
import pyodbc
from sqlcredits import LISTSUBD, SQLCREDITS, EXTENSIONS
import json
import base64



class Work:
    def __init__(self, SUBDja, query, ext):
        self.SUBDja = SUBDja
        self.SUBD = self.set_subd
        self.driver = SQLCREDITS[self.SUBD]["driver"]
        self.driver2 = SQLCREDITS[self.SUBD]["driver2"]
        self.user = SQLCREDITS[self.SUBD]["user"]
        self.pwd = SQLCREDITS[self.SUBD]["pwd"]
        self.hostname = SQLCREDITS[self.SUBD]["hostname"]
        self.port = SQLCREDITS[self.SUBD]["port"]
        self.dbname = SQLCREDITS[self.SUBD]["dbname"]
        self.datadir = SQLCREDITS[self.SUBD]["volumes"]["DATA_DIR"]
        self.logdir = SQLCREDITS[self.SUBD]["volumes"]["LOG_DIR"]
        self.backupdir = SQLCREDITS[self.SUBD]["volumes"]["BACKUP_DIR"]
        self.echo = False #True #False
        self.connection = self.get_string_connection
        self.engine = self.get_engine
        self.query = query
        self.ext = ext
        self.extension = self.set_extension

    @property
    def set_subd(self):
        if self.SUBDja in LISTSUBD:
            return self.SUBDja
        else:
            return f'supported bases are {LISTSUBD}'

    @property
    def set_extension(self):
        if self.ext in EXTENSIONS:
            return self.ext
        else:
            return f'filetype {self.ext} not supported yet'

    @property
    def get_string_connection(self):
        if self.SUBD == "MSSQL-DOCKER" or self.SUBD == "MSSQL-HOSTING" :
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}?driver={self.driver2};"
        elif self.SUBD in ("MYSQLROOT-DOCKER", "MYSQLROOT-HOSTING", "MYSQL-DOCKER", "MYSQL-HOSTING"):
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}?charset=utf8mb4;"
        elif self.SUBD in ("POSTGRES-DOCKER", "POSTGRES-HOSTING"):
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}"
        elif self.SUBD in ("MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING"):
            self.connection = f"{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}"
        else:
            None
        return self.connection

    @property
    def get_engine(self):
        if self.SUBD == "MSSQL-DOCKER" or self.SUBD == "MSSQL-HOSTING" :
            self.engine = create_engine(self.connection, fast_executemany=True, echo=self.echo).execution_options(isolation_level="AUTOCOMMIT")
        elif self.SUBD in ("MYSQLROOT-DOCKER", "MYSQLROOT-HOSTING", "MYSQL-DOCKER", "MYSQL-HOSTING"):
            self.engine = create_engine(self.connection, echo=self.echo)
        elif self.SUBD in ("POSTGRES-DOCKER","POSTGRES-HOSTING"):
            self.engine = create_engine(self.connection, echo=self.echo)
        elif self.SUBD in ("MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING"):
            self.engine = create_engine(self.connection, echo=self.echo)
        else:
            None
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
        if self.extension == 'xlsx':
            pd.DataFrame(rows).to_excel('C:\файлы\sales.xlsx')
            result = self.file_b64encode('C:\файлы\sales.xlsx')
            return result
        elif self.extension == 'json':
            data = [row._asdict() for row in rows]
            json_data = json.dumps(data)
            result = self.file_b64encode(json_data)
            return result
        elif self.extension == 'csv':
            pd.DataFrame(rows).to_csv('C:\\файлы\\sales.csv', sep='\t', encoding='utf-8', index=False, header=True, float_format='%.2f')
            result = self.file_b64encode('C:\\файлы\\sales.csv')
            return result
        else:
            return False

    #@property
    def get_result(self):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            sql = text(self.query)
            try:
                rows = db.execute(sql).all()
                print('ggggg',[row._asdict() for row in rows])
                encoded = self.data_to_file(rows)
                self.rezult = {'status': 'ok', 'rezult' : encoded, 'count': len(rows)}
            except Exception as e:
                if format(e).find('This result object does not return rows') >= 0:
                    self.rezult = {'status': 'ok', 'result' : format(e), 'query': self.query, 'count': 0}
                else:
                    self.rezult = {'status': 'error', 'result' : format(e), 'query': self.query, 'count': None}
            return self.rezult


L = ["MSSQL-DOCKER","MSSQL-HOSTING","MYSQLROOT-DOCKER","MYSQLROOT-HOSTING","MYSQL-DOCKER","MYSQL-HOSTING",
     "MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING",
     "POSTGRES-DOCKER","POSTGRES-HOSTING",]
x = Work("MARIADB-DOCKER", "select 'tttttrr' as ff", 'xlsx'); #.get_result;
print(x.get_result())
#решить вопрос с неправильным именем субд
#print(x.get_result)
#print(x) CREATE DATABASE Sales21
#"select N'ddは一生に一度の選手vvсмвамамиvv' COLLATE Latin1_General_BIN"




