# -*- coding:utf-8 -*-
from wtforms import StringField
from wtforms.validators import DataRequired
from app.validators import BaseForm
import re
from app.httpCode.code import NotAllowed


class SendEmailForm(BaseForm):
    receivers = StringField(validators=[DataRequired()])
    send_name = StringField(validators=[DataRequired()])
    to_name = StringField(validators=[DataRequired()])
    title = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
    file_name = StringField()
    file_path = StringField()
    file_type = StringField()

    def validate_receivers(self, field):
        for i in field.data:
            if not re.match(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", i):
                err = "[{}]邮箱格式错误".format(i)
                raise NotAllowed(err)

    def validate_file_name(self, field):

        if field.data:
            if not self.file_path.data:
                raise NotAllowed("请传入[file_path]参数")

            if not self.file_type.data:
                raise NotAllowed("请传入[file_type]参数")
            elif self.file_type.data not in ['xlsx', 'zip']:
                    raise NotAllowed("[file_type]参数无效!")

