# -*- coding:utf-8 -*-

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from application import app


class EmailServer:
    def __init__(self, receivers, send_name, to_name, title, content):
        """

        :param receivers: 收件人 list
        :param send_name: 发件人落款
        :param to_name: 收件人落款
        :param title: 邮件标题
        :param content: 邮件内容
        """
        self.mail_host = app.config['EMAIL_KEY']['MAIL_HOST']
        self.mail_port = app.config['EMAIL_KEY']['MAIL_PORT']
        self.mail_user = app.config['EMAIL_KEY']['MAIL_USER']
        self.mail_pass = app.config['EMAIL_KEY']['MAIL_PASS']
        self.sender = app.config['EMAIL_KEY']['SENDER']

        self.receivers = receivers  # 收件人
        self.send_name = send_name  # 发件人落款
        self.to_name = to_name  # 收件人落款
        self.title = title  # 邮件标题
        self.content = content  # 正文内容
        self.message = MIMEMultipart()
        self.build_email()

    def build_email(self):
        self.message['From'] = Header(self.send_name, 'utf-8')  # 邮件发件人落款
        self.message['To'] = Header(self.to_name, 'utf-8')  # 邮件收件人落款
        self.message['Subject'] = Header(self.title, 'utf-8')  # 标题
        self.message.attach(MIMEText(self.content, 'html', 'utf-8'))  # 添加正文内容

    def insert_attachment_rendition(self, file, file_name, file_type=None):
        """

        :param file_type: 文件类型,默认为xlsx
        :param file: 文件路径
        :param file_name: 文件名
        :return:
        """
        file_type = file_type if file_type else 'xlsx'
        type_minebase = {
            'xlsx': MIMEBase('Application', 'xlsx', filename=file_name),
            'zip': MIMEBase('zip', 'zip', filename=file_name)
        }
        with open(file, 'rb') as f:
            # mime = MIMEBase('Application', 'xlsx', filename=file_name)
            mime = type_minebase[file_type]
            mime.add_header('Content-Disposition', 'attachment', filename=file_name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            self.message.attach(mime)

    def insert_picture(self, picture):
        """

        :param picture: 图片路径
        :return:
        """
        with open(picture, 'rb') as f:
            mime = MIMEImage(f.read())
            mime.add_header('Content-ID', 'Imgid')
            self.message.attach(mime)

    def send(self):
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            smtp_obj.login(self.mail_user, self.mail_pass)
            smtp_obj.sendmail(self.sender, self.receivers, self.message.as_string())
            smtp_obj.quit()
            return {'status': True, 'msg': '发送成功'}
        except Exception as e:
            app.logger.error(e)
            return {'status': False, 'msg': e}
