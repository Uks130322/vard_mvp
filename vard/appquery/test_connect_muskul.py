# pip install SQLAlchemy

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import re


# def get_engine():
#     parol = 'P%40r0l'  #%40
#     engine = create_engine(f"mysql://root:{parol}@localhost/baza_test1",echo=False)
#     return engine



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
with Session(autoflush=False, bind=engine) as db:
    df = db.execute(text('SELECT * FROM vardapp_users'))
    for i in df:
        print(i)

