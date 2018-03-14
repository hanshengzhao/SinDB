#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

# 数据查询核心功能
import importlib
from libs.config import Config

from logging import getLogger

logger = getLogger('SinDB')


def sql_filter(sql, db_type):
    """
    过滤SQL 是否符合
    :param sql: SQL语句
    :param db_type: 数据库类型
    :return: 返回一个字典
    """
    ret = {
        "status": True,
        "message": "",
    }
    conf = Config()
    filter_classes = conf.get("%s_filter" % db_type, "filter_class")
    # 获取配置文件中配置的所有的filter_class
    if filter_classes:
        filter_classes = filter_classes.split(",")
        imp_module = importlib.import_module('db_query.backends.%s.sql_filter' % db_type)
        for filter_class in filter_classes:
            # 循环所有的过滤器,如果发现有一个过滤失败,那么就返回
            try:
                db_filter_class = getattr(imp_module, filter_class)
                db_filter = db_filter_class()
                if not db_filter.sql_passes(sql):
                    ret["message"] = db_filter.filter_description()
                    ret["status"] = False
                    break
            except Exception as e:
                ret["message"] = str(e)
                ret["status"] = False
                break
    return ret


def sql_query(sql, db_backend, db_connect_info, timeout, limit):
    """
    :param sql: 要查询的sql
    :param db_backend: 查询后端
    :param db_connect_info: 数据库连接信息
    :param timeout: 查询超时时间
    :param limit: 查询限制
    :return: 返回查询结果列表
    """
    imp_module = importlib.import_module('db_query.backends.%s' % db_backend)
    db_operate_class = getattr(imp_module, 'DatabaseOperations')
    db_operate = db_operate_class(**db_connect_info)
    select_ret = db_operate.select_sql(sql, limit, timeout)
    if select_ret["status"]:
        if select_ret["result"] and select_ret["field"]:
            list_result = list(map(lambda x: list(x), select_ret["result"]))
            list_field = list(map(lambda x: x[0], select_ret["field"]))  # 只返回第一个名称
            return_ret = {"field": list_field, "result": list_result, "status": True,
                          "effect_row": select_ret["effect_row"], "message": select_ret['message']
                          }
        else:
            return_ret = {"field": [], "result": [], "status": True,
                          "effect_row": select_ret["effect_row"], "message": select_ret['message']
                          }

    else:
        return_ret = {"status": False, "message": select_ret['message']}
    return return_ret


# 数据库连接状态判断
def database_status(db_backend, db_connect_info):
    imp_module = importlib.import_module('db_query.backends.%s' % db_backend)
    db_operate_class = getattr(imp_module, 'DatabaseOperations')
    try:
        db_connect_info["connect_timeout"] = 5
        db_operate = db_operate_class(**db_connect_info)
        db_operate.close_conn()
        return {"status":True}
    except Exception as e:
        return {"status":False,"message":str(e)}
