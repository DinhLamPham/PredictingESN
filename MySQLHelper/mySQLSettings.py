import pymysql

my_host = 'localhost'
my_user = 'root'
my_password = '123456'
my_db = 'ProcessMining'


def OpenConnection():
    connection = pymysql.connect(host=my_host, user=my_user, password=my_password, db=my_db)
    return connection


def CloseConnection(connection):
    connection.close()
