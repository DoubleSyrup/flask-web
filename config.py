#baseConfig
HOST = "0.0.0.0"
DEBUG = True

#dialect+driver://username:password@host:port/database
DIALECT = "mysql"
DRIVER = "mysqldb"
USERNAME = "***"
PASSWORD = "***"
LOCALHOST = '***'
PORT = "3306"
DATABASE = "flask"
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT,DRIVER,USERNAME,PASSWORD,LOCALHOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

