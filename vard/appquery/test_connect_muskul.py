# pip install SQLAlchemy

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


def get_engine():
    parol = 'P%40r0l'  #%40
    engine = create_engine(f"mysql://root:{parol}@localhost/baza_test1",echo=False)
    return engine

engine = get_engine()
Session = sessionmaker(autoflush=False, bind=engine)
with Session(autoflush=False, bind=engine) as db:
    df = db.execute(text('SELECT * FROM vardapp_users'))
    for i in df:
        print(i)

