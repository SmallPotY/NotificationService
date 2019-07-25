# -*- coding:utf-8 -*-
from common.models import Base, db


class RunningLogModel(Base):
    __tablename__ = 'RUNNING_LOG'

    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="id")
    module_name = db.Column(db.String(128), nullable=False, default="", server_default="", comment="模块名")
    details = db.Column(db.String(1024), nullable=False, default="", server_default="", comment="详情内容")
    message = db.Column(db.String(512), nullable=False, default="", server_default="", comment="消息")
    url = db.Column(db.String(512), nullable=False, default="", server_default="", comment="URL")
    source = db.Column(db.String(128), nullable=False, default="", server_default="", comment="来源")