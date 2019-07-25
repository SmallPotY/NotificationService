# -*- coding:utf-8 -*-

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from application import app
from web.httpCode.code import NotAllowed
from common.libs.LogService import LogService as Log

class ShortMessageService:

    def __init__(self, sms_type=None, phone_number=None, template_id=None, sms_sign=None, proxy=None):
        """

        :type proxy: 短信代理商, 默认为腾讯云
        :param sms_type:    Enum{0: 普通短信, 1: 营销短信}, 默认为普通短信
        :param phone_number:   接收短信的手机号码
        :param template_id:     模板ID
        :param sms_sign:        签名内容
        """
        self.sms_type = sms_type if sms_type else 0
        self.template_id = template_id if template_id else None
        self.sms_sign = sms_sign if sms_sign else None
        self.phone_number = phone_number if phone_number else ""
        self.proxy = proxy if proxy else "腾讯云"

        proxy_key = app.config['SHORT_MESSAGE_KEY'].get(proxy)

        if not proxy_key:
            raise NotAllowed("短信代理商不存在!")

        if not app.config['SHORT_MESSAGE_TEMPLATE'].get(template_id):
            raise NotAllowed("短信模板不存在!")

        if sms_sign not in app.config['SHORT_MESSAGE_SIGNATURE']:
            raise NotAllowed("短信签名不存在!")

        self.sender = SmsSingleSender(proxy_key['APP_ID'], proxy_key['APP_KEY'])

    def send(self, params):
        """
        发送短信
        :param params:
        """
        result = None
        template = app.config['SHORT_MESSAGE_TEMPLATE'].get(self.template_id)
        try:
            template.format(*params)
        except Exception as e:
            msg = "模板参数不符!  template : " + template
            Log.record_abnormality(
                module_name="短信模块", level="3", message=msg, details=str(e)
            )
            raise NotAllowed(msg)

        try:
            result = self.sender.send_with_param(86, self.phone_number, self.template_id, params,
                                                 sign=self.sms_sign, extend="", ext="")
        except HTTPError as e:
            Log.record_abnormality(
                module_name="短信模块", level="3", message="短信接口异常", details=str(e)
            )
        except Exception as e:
            Log.record_abnormality(
                module_name="短信模块", level="2", message="短信发送异常", details=str(e)
            )
        return result
