#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

from django import dispatch

# 定义查询数据库的信号
# 查询的 查询状态 查询时长 查询备注
query_db_signal = dispatch.Signal(providing_args=["status","query_time","message"])