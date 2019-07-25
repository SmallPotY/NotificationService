# -*- coding:utf-8 -*-
from configparser import ConfigParser

config = ConfigParser()
config.read("secret.ini")

SERVER_PORT = 8877
SERVER_HOST = '127.0.0.1'
DEBUG = True
RELEASE_VERSION = '1.0'

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = config.get('localhostDB', 'USERNAME')
PASSWORD = config.get('localhostDB', 'PASSWORD')
HOST = config.get('localhostDB', 'HOST')
PORT = config.get('localhostDB', 'PORT')
DATABASE = 'letter_pigeon_service'
SQLALCHEMY_ENCODING = 'utf-8'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                          PORT, DATABASE)
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

SHORT_MESSAGE_KEY = {
    "腾讯云": {
        "APP_ID": config.get('ShortMessageKey', 'TENCENT_APP_ID'),
        "APP_KEY": config.get('ShortMessageKey', 'TENCENT_APP_KEY'),
    }
}

SHORT_MESSAGE_TEMPLATE = {
    "378130": "Dear {0}： 你好，应用： {1} ，运行的结果为：{2}。请知悉！",

}

SHORT_MESSAGE_SIGNATURE = ["员工盒子"]
