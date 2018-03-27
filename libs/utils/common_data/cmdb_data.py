#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

# 从cmdb 获取的数据

import requests
from libs.config import Config
from urllib.parse import quote


# 从cmdb获取所有项目组
def get_projects():
    # print("获取projects")
    # todo 修改为 缓存方式的

    try:
        conf = Config()
        url = conf.get('project_info', 'url')
        url = quote(url, safe='?|/|=|&|:')
        res = requests.get(url, timeout=5)
        ret = res.json()['data']
        ret_tuple = tuple(map(lambda x: (x['project']['en_name'], x['project']['ch_name']), ret))
    except Exception as e:
        print('连接失败')
        ret_tuple = []
    return ret_tuple
