from django.db import models
from vardapp.models import Users

class Query(models.Model):
    driver1 = 1
    DRIVERS = [
        (driver1, 'SQLAlchemy'),
    ]
    #ENGINES = {'SQLAlchemy';''}

    user_id = models.ForeignKey(Users , on_delete=models.CASCADE, null=False) # like '[0-9a-zA-Z_][0-9a-zA-Z_-]%'
    user_name = models.CharField(min_length=1, max_length=16, null=False) #
    password = models.CharField(min_length=8, max_length=128, null=False) #
    driver = models.CharField(max_length='255', null=False, choices=DRIVER1, default=engine1) #
    url = models.CharField(null=True) #host может быть как именем хоста, так и IP-адресом
    host = models.CharFieldField(null=False, default='localhost') #host может быть как именем хоста, так и IP-адресом
    port = models.IntegerFieldField(null=False, default=3306) #
    data_base_type = models.CharField(max_length=255, null=False) #что это??? OPTIONS???
    data_base_name = models.CharField(max_length=63, null=False) # like '%[0-9a-zA-Z_-]%' # Имена mysql, sys, information_schema и performance_schema запрещены
    description = models.CharField(max_length=255, null=False) #
    OPTIONS = models.CharField(max_length=255, null=False, default="""'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}""")


# https://sky.pro/media/podklyuchenie-k-baze-dannyh-mysql-s-pomoshhyu-python/
# install mysql-connector-python
# import mysql.connector
# cnx = mysql.connector.connect(user='username', password='password',
#                               host='hostname',
#                               database='database_name')
# cnx.close()


# https://metanit.com/python/database/3.1.php
# pip install SQLAlchemy




