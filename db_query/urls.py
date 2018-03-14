#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.urls import path, include
from db_query import views as db_query_view

urlpatterns = [
    path('', db_query_view.query_sql, name="sql_query"),
    path('db_status/', db_query_view.db_status,name="db_status"),
    path('record/list/', db_query_view.Query_Record_List.as_view()),
    path('record/', db_query_view.query_record_index),
]
