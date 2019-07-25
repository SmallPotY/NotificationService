# -*- coding:utf-8 -*-
from common.models.mExceptionLog import ExceptionLogModel
from common.models.mRunningLog import RunningLogModel
from flask import request


class LogService:

    @staticmethod
    def record_abnormality(module_name=None, level=None, message=None, details=None, source=None, url=None):
        """
        记录异常
        :param module_name: 模块名
        :param level: 异常等级
        :param message: 消息
        :param details: 详情
        :param source: 异常来源
        :param url: 请求
        """
        log = dict(
            url=url if url else str(request.full_path),
            module_name=module_name if module_name else "",
            level=level if level else "1",
            message=message if message else "",
            details=details if details else "",
            source=source if source else "",
        )
        ExceptionLogModel.c_(**log)

    @staticmethod
    def record_running(module_name=None, details=None, message=None, url=None, source=None):
        log = dict(
            module_name=module_name if module_name else "",
            details=details if details else "",
            message=message if message else "",
            url=url if url else str(request.full_path),
            source=source if source else "",
        )
        RunningLogModel.c_(**log)
