import os
from sqlalchemy import create_engine
import urllib


class Config(object):
    SECRET_KEY = 'Clave_nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:1234@127.0.0.1/empleadosPruebas'
    #SQLALCHEMY_DATABASE_URL='mysql+pymysql://localhost:3306/?user=root'
    SQLALCHEMY_TRACK_MODIFICATION=False
