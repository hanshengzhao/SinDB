#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

from logging import getLogger

logger = getLogger('SinDB')


class Base_MySQL_Filter:
    """
    基础 Filter
    """
    pass


class Empty_Filter(Base_MySQL_Filter):
    # 为空 过滤器
    def __init__(self):
        logger.debug("开始过滤为空%s的sql")

    def sql_passes(self, sql):
        if sql.strip():
            return True
        else:
            return False

    def filter_description(self):
        desc = "sql 为空"
        return desc


class NoContain_Filter(Base_MySQL_Filter):
    # 通用 不包含 过滤器
    def __init__(self, filter_str):
        self.filter_str = filter_str
        logger.debug("开始过滤不含有%s的sql" % filter_str)

    def sql_passes(self, sql):
        if self.filter_str not in sql.lower():
            return False
        else:
            return True

    def filter_description(self):
        desc = "不含有%s的SQL" % self.filter_str
        return desc


class No_Select_Filter(NoContain_Filter):
    def __init__(self):
        super(No_Select_Filter, self).__init__("select")


class Contain_Filter(Base_MySQL_Filter):
    # 通用 包含 过滤器
    def __init__(self, filter_str):
        self.filter_str = filter_str
        logger.debug("开始过滤含有%s的sql" % filter_str)

    def sql_passes(self, sql):
        if self.filter_str in sql.lower():
            return False
        else:
            return True

    def filter_description(self):
        desc = "含有%s的SQL" % self.filter_str
        return desc


class Star_Symbol_Filter(Contain_Filter):
    def __init__(self):
        super(Star_Symbol_Filter, self).__init__("*")


class Insert_Filter(Contain_Filter):
    def __init__(self):
        super(Insert_Filter, self).__init__("insert")

    def filter_description(self):
        desc = "含有%s的SQL,仅允许查询,不允许插入" % self.filter_str
        return desc


class Drop_Filter(Contain_Filter):
    def __init__(self):
        super(Drop_Filter, self).__init__("drop")


