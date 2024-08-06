


SQLCREDITS = {
"MSSQL-DOCKER"        : {"driver": "mssql+pyodbc",
                         "driver2": "ODBC+Driver+17+for+SQL+Server",
                         "user": "sa",
                         "pwd": "QeTuo123",
                         "hostname": "localhost",
                         "dbname": "master",
                         "port": "6003",
                         "volumes": {"DATA_DIR": "/var/opt/sqlserver/data", "LOG_DIR": "/var/opt/sqlserver/log", "BACKUP_DIR": "/var/opt/sqlserver/backup"}
                         },
"MSSQL-HOSTING"       : {"driver": "mssql+pyodbc",
                         "driver2": "ODBC+Driver+17+for+SQL+Server",
                         "user": "sa",
                         "pwd": "QeTuo123",
                         "hostname": "testmssql",
                         "dbname": "master",
                         "port": "1433",
                         "volumes": {"DATA_DIR": "/var/opt/sqlserver/data", "LOG_DIR": "/var/opt/sqlserver/log", "BACKUP_DIR": "/var/opt/sqlserver/backup"}
                         },

"MYSQLROOT-DOCKER"     : {"driver": "",
                         "driver2": "",
                         "user": "root",
                         "pwd": "rootmysql",
                         "hostname": "localhost",
                         "dbname": "bdmysql",
                         "port": "6000",
                         "volumes": {"DATA_DIR": "/var/lib/mysql/", "LOG_DIR": "", "BACKUP_DIR": ""}
                         },
"MYSQLROOT-HOSTING"   : {"driver": "",
                         "driver2": "",
                         "user": "root",
                         "pwd": "rootmysql",
                         "hostname": "testmysql",
                         "dbname": "bdmysql",
                         "port": "3306",
                         "volumes": {"DATA_DIR": "/var/lib/mysql/", "LOG_DIR": "", "BACKUP_DIR": ""}
                         },
"MYSQL-DOCKER"         : {"driver": "",
                         "driver2": "",
                         "user": "mysqluser",
                         "pwd": "mysqlpass",
                         "hostname": "localhost",
                          "dbname": "bdmysql",
                          "port": "6000",
                          "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          },
"MYSQL-HOSTING"        : {"driver": "",
                         "driver2": "",
                         "user": "mysqluser",
                         "pwd": "mysqlpass",
                         "hostname": "testmysql",
                         "dbname": "bdmysql",
                         "port": "3306",
                         "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""}
                          }
# "POSTGRES"    = {"driver": "", "driver2": "", "user": "postgresuser", "pwd": "postgrespass", "hostname": ["localhost", "testpostgres"], "dbname": "bdpostgres", "port": ["6002", "5432"], "volumes": {"DATA_DIR": "/var/lib/postgresql/data/testpgdata"} }
# "MARIADB"     = {"driver": "", "driver2": "", "user": "mariauser",    "pwd": "mariapass",    "hostname": ["localhost", "testmariadb"],  "dbname": "bdmaria",    "port": ["6000", "3306"], "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""} }
# "MARIADBROOT" = {"driver": "", "driver2": "", "user": "root",         "pwd": "rootmaria",    "hostname": ["localhost", "testmariadb"],  "dbname": "bdmaria",    "port": ["6000", "3306"], "volumes": {"DATA_DIR": "", "LOG_DIR": "", "BACKUP_DIR": ""} }

}
L = ["MSSQL-DOCKER","MSSQL-HOSTING","MYSQLROOT-DOCKER","MYSQLROOT-HOSTING","MYSQL-DOCKER","MYSQL-HOSTING",]
SUBD = "MSSQL-DOCKER"
driver = SQLCREDITS[SUBD]["driver"]
driver2 = SQLCREDITS[SUBD]["driver2"]
user = SQLCREDITS[SUBD]["user"]
pwd = SQLCREDITS[SUBD]["pwd"]
hostname = SQLCREDITS[SUBD]["hostname"]
port = SQLCREDITS[SUBD]["port"]
dbname =  SQLCREDITS[SUBD]["dbname"]
datadir = SQLCREDITS[SUBD]["volumes"]["DATA_DIR"]
logdir = SQLCREDITS[SUBD]["volumes"]["LOG_DIR"]

###################################################

EXTENSION_DIC = {
    'xls': False,
    'xlsx': True,
    'xlsb': False,
    'csv': True,
    'json': True
}

EXTENSIONS = []

for key, value in EXTENSION_DIC.items():
    if value == True:
        EXTENSIONS.append(key)

###################################################





