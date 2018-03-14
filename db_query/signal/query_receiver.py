#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

import json
from logging import getLogger
from django.dispatch import receiver
from db_query.signal.query_signal import query_db_signal
from db_query.models import Select_Record
from db_manage.models import DataBases
from libs.config import Config

logger = getLogger("SinDB")


@receiver(query_db_signal)
def save_query_record(sender, **kwargs):
    try:
        query_dict = json.loads(sender.body)
        query_db_id = query_dict['db_id']
        query_sql = query_dict['query_sql']
        query_db = DataBases.objects.get(id=query_db_id)
        record = Select_Record(created_user=sender.user, sql=query_sql, status=kwargs["status"],
                               database=query_db,
                               execute_time=kwargs["query_time"], message=kwargs["message"]
                               )
        record.save()
        if not  query_db.is_notify:
            return
        server_url = "%s://%s" % (sender.scheme, sender.get_host())
        conf = Config()
        if not kwargs["status"]:
            picurl = "%s%s" % (server_url, conf.get('notify', "error_img"))
        else:
            picurl = "%s%s" % (server_url, conf.get('notify', "success_img"))
        data = {
            "msgtype": "link",
            "link": {
                "text": "%s用户查询%s %s" % (sender.user, query_db.db_database, kwargs["message"]),
                "title": "查询%s" % query_db.db_name,
                "picUrl": picurl,
                "messageUrl": "%s%s%s" % (server_url,conf.get('notify', "query_detail_url"),record.id)
            }
        }
        from libs.utils.notify.dingding_notify import DingDing_Notify
        notify_obj = DingDing_Notify(query_db.notify_url)
        notify_obj.notify(data)
    except Exception as e:
        logger.exception(e)
        logger.error("数据库查询记录保存失败")


