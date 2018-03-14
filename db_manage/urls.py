#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

from django.urls import path
from db_manage.views import *

urlpatterns = [
    path('mysql/', mysql_view),
    path('mysql/list/', MysqlList.as_view()),
    path('mysql/add/', Database_Add.as_view(),name="add_mysql"),
    path('mysql/delete/<int:id>', Database_Delete.as_view()),
    path('mysql/update/<int:id>', Database_Update.as_view()),

]
