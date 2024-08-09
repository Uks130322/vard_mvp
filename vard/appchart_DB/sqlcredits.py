


SQLCREDITS = {
"MSSQL-DOCKER"        : {"driver": "mssql+pyodbc",
                         "driver2": "?driver=ODBC+Driver+17+for+SQL+Server",
                         "user": "sa",
                         "pwd": "QeTuo123",
                         "hostname": "localhost",
                         "dbname": "master",
                         "port": "6003",
                         "volumes": {"DATA_DIR": "/var/opt/sqlserver/data", "LOG_DIR": "/var/opt/sqlserver/log", "BACKUP_DIR": "/var/opt/sqlserver/backup"}
                         },
"MSSQL-HOSTING"       : {"driver": "mssql+pyodbc",
                         "driver2": "?driver=ODBC+Driver+17+for+SQL+Server",
                         "user": "sa",
                         "pwd": "QeTuo123",
                         "hostname": "testmssql",
                         "dbname": "master",
                         "port": "1433",
                         "volumes": {"DATA_DIR": "/var/opt/sqlserver/data", "LOG_DIR": "/var/opt/sqlserver/log", "BACKUP_DIR": "/var/opt/sqlserver/backup"}
                         },

"MYSQLROOT-DOCKER"     : {"driver": "mysql+pymysql",
                         "driver2": "?charset=utf8mb4",
                         "user": "root",
                         "pwd": "rootmysql",
                         "hostname": "localhost",
                         "dbname": "bdmysql",
                         "port": "6001",
                         "volumes": {"DATA_DIR": "/var/lib/mysql/", "LOG_DIR": "", "BACKUP_DIR": ""}
                         },
"MYSQLROOT-HOSTING"   : {"driver": "mysql+pymysql",
                         "driver2": "?charset=utf8mb4",
                         "user": "root",
                         "pwd": "rootmysql",
                         "hostname": "testmysql",
                         "dbname": "bdmysql",
                         "port": "3306",
                         "volumes": {"DATA_DIR": "/var/lib/mysql/", "LOG_DIR": "", "BACKUP_DIR": ""}
                         },
"MYSQL-DOCKER"         : {"driver": "mysql+pymysql",
                         "driver2": "?charset=utf8mb4",
                         "user": "mysqluser",
                         "pwd": "mysqlpass",
                         "hostname": "localhost",
                          "dbname": "bdmysql",
                          "port": "6000",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"MYSQL-HOSTING"        : {"driver": "mysql+pymysql",
                         "driver2": "?charset=utf8mb4",
                         "user": "mysqluser",
                         "pwd": "mysqlpass",
                         "hostname": "testmysql",
                         "dbname": "bdmysql",
                         "port": "3306",
                         "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"POSTGRES-DOCKER"      : {"driver": "postgresql+psycopg2",
                          "driver2": "",
                          "user": "postgresuser",
                          "pwd": "postgrespass",
                          "hostname": "localhost",
                          "dbname": "bdpostgres",
                          "port": "6002",
                          "volumes": {"DATA_DIR": "/var/lib/postgresql/data/testpgdata", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"POSTGRES-HOSTING"     : {"driver": "postgresql+psycopg2",
                          "driver2": "",
                          "user": "postgresuser",
                          "pwd": "postgrespass",
                          "hostname": "testpostgres",
                          "dbname": "bdpostgres",
                          "port": "5432",
                          "volumes": {"DATA_DIR": "/var/lib/postgresql/data/testpgdata", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"MARIADB-DOCKER"       : {"driver": "mysql+pymysql",
                          "driver2": "",
                          "user": "mariauser",
                          "pwd": "mariapass",
                          "hostname": "localhost",
                          "dbname": "bdmaria",
                          "port": "6000",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"MARIADB-HOSTING"      : {"driver": "mysql+pymysql",
                          "driver2": "",
                          "user": "mariauser",
                          "pwd": "mariapass",
                          "hostname": "testmariadb",
                          "dbname": "bdmaria",
                          "port": "3306",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"MARIADBROOT-DOCKER"   : {"driver": "mysql+pymysql",
                          "driver2": "",
                          "user": "root",
                          "pwd": "rootmaria",
                          "hostname": "localhost",
                          "dbname": "bdmaria",
                          "port": "6000",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"MARIADBROOT-HOSTING"  : {"driver": "mysql+pymysql",
                          "driver2": "",
                          "user": "root",
                          "pwd": "rootmaria",
                          "hostname":  "testmariadb",
                          "dbname": "bdmaria",
                          "port": "3306",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"ERROR"                : {"driver": "",
                          "driver2": "",
                          "user": "",
                          "pwd": "",
                          "hostname":  "",
                          "dbname": "",
                          "port": "",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          }

}
LISTSUBD = ["MSSQL-DOCKER","MSSQL-HOSTING","MYSQLROOT-DOCKER","MYSQLROOT-HOSTING","MYSQL-DOCKER","MYSQL-HOSTING",
     "MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING",
     "POSTGRES-DOCKER","POSTGRES-HOSTING","ERROR"]

SUBD = "ERROR"
driver = SQLCREDITS[SUBD]["driver"]
driver2 = SQLCREDITS[SUBD]["driver2"]
user = SQLCREDITS[SUBD]["user"]
pwd = SQLCREDITS[SUBD]["pwd"]
hostname = SQLCREDITS[SUBD]["hostname"]
port = SQLCREDITS[SUBD]["port"]
dbname =  SQLCREDITS[SUBD]["dbname"]
datadir = SQLCREDITS[SUBD]["volumes"]["DATA_DIR"]
logdir = SQLCREDITS[SUBD]["volumes"]["LOG_DIR"]


# 1 "MSSQL-DOCKER","MSSQL-HOSTING"
# 2 "MYSQLROOT-DOCKER","MYSQLROOT-HOSTING","MYSQL-DOCKER","MYSQL-HOSTING"
# 3 "MARIADB-DOCKER","MARIADB-HOSTING","MARIADBROOT-DOCKER","MARIADBROOT-HOSTING"
# 4 "POSTGRES-DOCKER","POSTGRES-HOSTING"

###################################################

EXTENSION_DIC = {
    'xls': False,
    'xlsx': True,
    'xlsb': False,
    'csv': True,
    'json': True,
    'pandas': False,
}

EXTENSIONS = []

for key, value in EXTENSION_DIC.items():
    if value == True:
        EXTENSIONS.append(key)

###################################################

# CHOISES_TYPE_DB = [
#     {'MSSQL': [
#                 {'lib':'SQL Alchemy', "is_available": True,  "driver": "mssql+pyodbc", "driver2": "ODBC+Driver+17+for+SQL+Server"},
#                 {'lib':'pyodbc', "is_available": False, "driver": "Driver={SQL Server Native Client 11.0};", "driver2": ""},
#                 {'lib':'pymssql', "is_available": False, "driver": "Driver={SQL Server Native Client 11.0};", "driver2": ""},
#              ]},
#
# ]
#
# "{self.driver}://{self.user}:{self.pwd}@{self.hostname}:{self.port}/{self.dbname}{self.driver2}"
# connectionString = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=localhost:1433;Database=cars;UID=sa;PWD=QeTuo123;")
# connectionString = pymssql.connect(server='host:port', user='user', password='pass', database ='database')

# DBTYPE = [
#         (1, 'MSSQL'),
#         (2, 'MYSQL'),
#         (3, CHOISES_TYPE_DB[3]),
#         (4, 'POSTGRES'),
#     ]

###################################################

