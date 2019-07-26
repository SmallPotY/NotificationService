# -*- coding:utf-8 -*-
import os
import platform

from flask import Flask, json
from werkzeug.exceptions import HTTPException
from decimal import Decimal
import datetime
from common.models import db
from app.httpCode import APIException
from common.libs.LogService import LogService


class JSONEncoder(json.JSONEncoder):
    """JSON序列化"""

    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


class Application(Flask):
    json_encoder = JSONEncoder

    def __init__(self, import_name, template_folder=None, root_path=None, static_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=static_folder, )
        self.config.from_object('config.baseSetting')
        env = platform.system()
        if env == "Linux":
            self.config.from_object('config.production')
        else:
            self.config.from_object('config.development')
        db.init_app(self)


def create_models(application):
    from common.models.mExceptionLog import ExceptionLogModel
    from common.models.mRunningLog import RunningLogModel
    with application.app_context():
        db.create_all()


current_path = os.path.dirname(__file__)
app = Application(__name__, template_folder=current_path + '/web/templates/',
                  static_folder=current_path + '/web/static',
                  root_path=current_path)


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, HTTPException):
        """可预知的错误"""
        code = e.code
        msg = e.description
        error_code = 999
        LogService.record_abnormality(module_name="框架异常(已捕获)", level="2", message=str(msg), details=str(e))
        return APIException(msg, code, error_code)
    else:
        """不可预知的错误"""
        LogService.record_abnormality(module_name="框架异常(无法捕获)", level="3", message="未知的异常", details=str(e))
        raise e
