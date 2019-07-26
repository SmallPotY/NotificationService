# -*- coding:utf-8 -*-
from flask import Blueprint

from app.httpCode.code import Success, NotAllowed
from app.validators.SendEmail import SendEmailForm
from common.libs.EmailService import EmailServer
from common.libs.ShortMessageService import ShortMessageService
from flask import jsonify
from app.validators.SendMessages import SendMessagesForm
from common.libs.LogService import LogService

api = Blueprint('api', __name__)


@api.route('/send_messages', methods=['POST'])
def send_messages():
    """
    发送短信接口, 请求体示例:
        {
            "phone_number":"18575750621",
            "sms_sign":"员工盒子",
            "template_id":"378130",
            "proxy":"腾讯云",
            "params":["老杨","短信模块","发送成功了"]
        }
    """
    data = SendMessagesForm().validate_for_forms().to_dict()
    s = ShortMessageService(phone_number=data['phone_number'], template_id=data['template_id'],
                            sms_sign=data['sms_sign'], proxy=data['proxy'])

    res = s.send(data['params'])
    LogService.record_running(
        module_name="短信通知", details=str(res), message="短信发送"
    )
    return jsonify(res)


@api.route('/send_email', methods=['POST'])
def send_email():
    """
    发送邮件接口, 请求示例:
        {
            "content":"请查收报表,谢谢!",
            "title":"每日报表",
            "receivers":["1041132457@qq.com"],
            "to_name":"Dear",
            "send_name":"员工盒子",
            "file_name":"每日报表.xlsx",
            "file_path": "C:\\Users\\dell\\Desktop\\报表.xlsx",
            "file_type":"xlsx"
        }
    """
    data = SendEmailForm().validate_for_forms().to_dict()
    email = EmailServer(receivers=data['receivers'], send_name=data['send_name'], to_name=data['to_name'],
                        title=data['title'],
                        content=data['content'])

    if data.get('file_name'):
        email.insert_attachment_rendition(file=data['file_path'], file_name=data['file_name'],
                                          file_type=data['file_type'])
    result = email.send()

    if result['status']:
        LogService.record_running(module_name="邮件模块", message=result['msg'], details=str(data))
        return Success("发送成功!")
    else:
        LogService.record_running(module_name="邮件模块", message=result['msg'], details=str(data))
        return Success(result['msg'])
