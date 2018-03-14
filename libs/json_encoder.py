#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
import json
from  datetime import date, datetime


# 用于json dumps 无法dump datetime 类型的数据

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
