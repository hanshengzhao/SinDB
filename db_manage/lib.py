#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from db_manage.models import DataBases
from logging import getLogger

logger = getLogger("SinDB")


# 数据库管理相关通用函数

def get_db_info(db_id):
    """
    根据数据库id获取数据库连接信息
    :param db_id: 数据库ID
    :return: 返回数据库连接信息
    """
    try:
        db_obj = DataBases.objects.get(id=db_id)
        return {
            "host": db_obj.db_host,
            "port": db_obj.db_port,
            "user": db_obj.db_user,
            "passwd": db_obj.db_passwd,
            "db": db_obj.db_database,
            "charset": db_obj.db_charset,
            "db_type": db_obj.db_type,
            "db_driver": db_obj.db_driver,
            "db_query_timeout": db_obj.db_query_timeout,
            "db_query_limit": db_obj.db_query_limit,
        }

    except Exception as e:
        logger.exception(e)
        return False



# 用户是否有权限查询该库
def is_allow_query(user, db_id):
    all_permission = user.select_permissions.all()
    for permission in all_permission:
        if DataBases.objects.values_list("id").filter(project=permission.project, id=db_id).count() > 0:
            return True
        if permission.database.filter(id=db_id).count() > 0:
            return True
    else:
        return False
