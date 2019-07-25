# -*- coding:utf-8 -*-
"""
    异常记录模块
"""
from common.models import Base, db


class ExceptionLogModel(Base):
    __tablename__ = 'EXCEPTION_LOG'

    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="id")
    module_name = db.Column(db.String(128), nullable=False, default="", server_default="", comment="模块名")
    level = db.Column(db.String(32), nullable=False, default="1", server_default="1", comment="等级")
    message = db.Column(db.String(512), nullable=False, default="", server_default="", comment="信息")
    details = db.Column(db.String(1024), nullable=False, default="", server_default="", comment="详细内容")
    url = db.Column(db.String(512), nullable=False, default="", server_default="", comment="资源符")
    source = db.Column(db.String(512), nullable=False, default="", server_default="", comment="来源")
