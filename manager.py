# -*- coding:utf-8 -*-
from application import app, create_models
from common.libs.LogService import LogService
from app.api import api

app.register_blueprint(api, url_prefix='/')


@app.route('/')
def hello():
    LogService.record_running(module_name="测试连接", message="Success")
    return 'hello'


if __name__ == '__main__':
    create_models(app)
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
