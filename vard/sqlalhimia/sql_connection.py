#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.sql import text
#
#
# MYSQL = {"user":,"":,"pwd":,"hostname":,"dbname":,}
# MSSQL = {"user":,"":,"pwd":,"hostname":,"dbname":,}
# POSTGRES = {"user":,"":,"pwd":,"hostname":,"dbname":,}
# MARIASDB = {"user":,"":,"pwd":,"hostname":,"dbname":,}
#
#
# README_db_connection_description.md
#
#
# def get_engine(hostname, dbname, user, pwd):
#     engine = create_engine(
#         f"mssql+pyodbc://{user}:{pwd}@{hostname}/{dbname}"
#         "?driver=ODBC+Driver+17+for+SQL+Server",
#         fast_executemany=True, echo=False)
#     return engine
#
# engine = get_engine('***', '***', '***', '***')
# Session = sessionmaker(autoflush=False, bind=engine)
# with Session(autoflush=False, bind=engine) as db:
#     L = []
#     df = db.query(Data).filter(Data.hash_sha3_512.is_(None)).all()
#     for p in df:
#         row = f"{p.f1}{p.f2}{p.f3}{p.f4}"
#         value = hashlib.sha3_512(row.encode('utf-8')).hexdigest()
#         L.append(dict(id=p.id, hash_sha3_512=value))
#
#     db.bulk_update_mappings(Data, L)
#     db.commit()
#
#


