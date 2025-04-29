import os

# Configuración de la URI de la base de datos para desarrollo
DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.getenv('DBUSER', 'dev_user'),
    dbpass=os.getenv('DBPASS', 'dev_password'),
    dbhost=os.getenv('DBHOST', 'localhost'),
    dbname=os.getenv('DBNAME', 'dev_db')
)
#HOLA
# Configuración adicional para desarrollo
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False