#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from libs.utils.notify.base_notify import Notify
import requests
import json
from logging import getLogger

# url = "https://oapi.dingtalk.com/robot/send?access_token=3efc2f9acf9a19e2642aefdc5af371593aaeef65dfad8ece19265bb27086203d"

a = {
    "msgtype": "link",
    "link": {
        "text": "查询xx",
        "title": "xx用户查询xx",
        "picUrl": "",
        "messageUrl": "http://www.baidu.com"
    }
}


class DingDing_Notify(Notify):
    def __init__(self,url):
        self.url = url
        self.headers = {"Content-Type": "application/json"}

    def notify(self,data):
        try:
            res = requests.post(self.url,json.dumps(data),headers=self.headers)
            return res
        except Exception as e :
            return None


