# -*- coding:utf-8 -*-
from wtforms import StringField
from wtforms.validators import DataRequired
from app.validators import BaseForm
import re
from app.httpCode.code import NotAllowed


class SendMessagesForm(BaseForm):

    phone_number = StringField(validators=[DataRequired()])
    template_id = StringField(validators=[DataRequired()])
    sms_sign = StringField(validators=[DataRequired()])
    proxy = StringField()
    params = StringField()

    def validate_phone_number(self, field):
        ret = re.match(r"^1[35678]\d{9}$", field.data)
        if not ret:
            raise NotAllowed("手机号码验证不通过!")
