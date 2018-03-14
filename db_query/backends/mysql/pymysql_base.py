#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

# mysql 默认版本 通过pymysql 连接

import pymysql
import time
from libs.base_wrap import Result_Thread
from libs.base_wrap import set_timeout


class DatabaseOperations:
    def __init__(self, host, port, user, passwd, db, charset="utf8",connect_timeout=10):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=db, charset=charset,
                                    connect_timeout=connect_timeout)
        self.conn_for_kill = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=db,
                                             charset=charset, connect_timeout=connect_timeout)
        self.server_id = self.conn.server_thread_id[0]
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):
        try:
            effect_row = self.cursor.execute(sql)
            execute_ret = {
                "execute_status": True,
                "effect_row": effect_row
            }
        except Exception as e:
            execute_ret = {
                "execute_status": False,
                "effect_row": 0,
                "error_message": str(e)
            }

        return execute_ret

    def select_sql(self, sql, limit, timeout):
        """
        查询sql
        :param sql: 查询的sql
        :param limit: 限制返回结果
        :return:
        """
        # execute_ret = set_timeout(timeout,self.kill_conn)(self.execute_sql(sql))()
        # execute_ret = self.execute_sql(sql)
        t1 = Result_Thread(target=self.execute_sql, args=(sql,))
        t1.start()
        t1.join(timeout)
        if t1.is_alive():
            self.kill_conn()
            execute_ret = None
        else:
            execute_ret = t1.get_result()
        if not execute_ret:
            ret = {
                "message": "查询超时",
                "status": False,
            }
        else:
            if execute_ret["execute_status"]:
                result = self.cursor.fetchall()[:limit]
                field = self.cursor.description
                ret = {
                    "field": field,
                    "result": result,
                    "effect_row": len(result),
                    "status": True,
                    "message": "查询成功",

                }
            else:
                ret = {
                    "message": execute_ret["error_message"],
                    "status": False,
                }
            self.close_conn()
        return ret

    def kill_conn(self):
        """ kill 数据库连接"""
        print("超时 kill %s" % self.server_id)
        self.cursor.close()
        self.conn.close()
        self.conn_for_kill.kill(self.server_id)
        self.conn_for_kill.close()
        return False

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
        self.conn_for_kill.close()

# my_database_operate = DatabaseOperations(host='172.17.32.218', port=3306, user='root', passwd='root', db='SinAPI')
# sql = "SELECT `API_MONITOR_api_log`.`id`, `API_MONITOR_api_monitor`.`name`, `API_MONITOR_api_log`.`status`, `API_MONITOR_api_log`.`result`, `API_MONITOR_api_log`.`date` FROM `API_MONITOR_api_log` INNER JOIN `API_MONITOR_api_monitor` ON (`API_MONITOR_api_log`.`api_id` = `API_MONITOR_api_monitor`.`id`) WHERE (`API_MONITOR_api_log`.`date` BETWEEN '2018-01-31 17:00:00' AND '2018-02-02 02:00:00' AND `API_MONITOR_api_log`.`api_id` IN (SELECT `API_MONITOR_api_monitor`.`id` FROM `API_MONITOR_api_monitor`)) ORDER BY `API_MONITOR_api_log`.`id` DESC LIMIT 30;"
# simple_sql = "select * from auth_user"
# result = my_database_operate.select_sql(sql, 20)
# print(result)
