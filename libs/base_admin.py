#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.contrib import admin

admin.site.site_header = 'SinDB 数据库查询系统'
admin.site.site_title = 'SinDB 数据库查询系统'


def get_all_field(model_name, id=True):
    list_1 = [x.name for x in model_name._meta.fields]
    if id:
        return list_1
    else:
        list_1.remove('id')
        return list_1
