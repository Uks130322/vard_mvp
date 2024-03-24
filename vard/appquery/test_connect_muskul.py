# pip install SQLAlchemy
#from vardapp.models import Users
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import re


# def get_engine():
#     parol = 'P%40r0l'  #%40
#     engine = create_engine(f"mysql://root:{parol}@localhost/baza_test1",echo=False)
#     return engine

#user_id = Users.get().first()
user_id = 'ddd'

def create_host(url,host,port):
    if host == 'localhost' or host == '127.0.0.1':
        result = host
    elif port == '' or port is None or not port:
        result = f'{url}:3306'
    else:
        result = f'{url}:{port}'
    return result

def get_engine(driver, user_name, password, url,host,port, data_base_name):
    password_new = password.replace('@', '%40')
    password_new = re.escape(password_new)
    host_new = create_host(url,host,port)
    engine = create_engine(f"{driver}://{user_name}:{password_new}@{host_new}/{data_base_name}", echo=False)
    return engine

engine = get_engine('mysql','root','P@r0l','','localhost','','baza_test1')
Session = sessionmaker(autoflush=False, bind=engine)
# with Session(autoflush=False, bind=engine) as db:
#     df = db.execute(text('SELECT * FROM vardapp_users'))
#     for i in df:
#         print(i)

with Session(autoflush=False, bind=engine) as db:
    rows = db.execute(text('SELECT * FROM vardapp_users')).fetchall()
    data = [{'user_id': user_id}]
    data.append([r._asdict() for r in rows])
print(data)






# r[1]
# keys_list = list(r.keys())

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

# "method": "info","select","create db","drop db"
# {
# "method": "select",
# "user_id": 1,
# "driver": "mysql",
# "user_name": "root",
# "password": "P@r0l",
# "url": null,
# "host": "localhost",
# "port": null,
# "data_base_name": "baza_test1",
# "data_base_type": null,
# "description": null,
# "str_query": "SELECT * FROM vardapp_users where id=1"
# }
#
# {
# "method": "create db",
# "user_id": 1,
# "driver": "mysql",
# "user_name": "root",
# "password": "P@r0l",
# "url": null,
# "host": "localhost",
# "port": null,
# "data_base_name": "baza_test2"
# }