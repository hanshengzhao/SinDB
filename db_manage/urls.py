#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

from django.urls import path
from db_manage.views import *

urlpatterns = [
    path('', mysql_view),
    path('list/', DatabaseList.as_view()),
    path('add/', Database_Add.as_view(),name="add_database"),
    path('delete/<int:id>', Database_Delete.as_view()),
    path('update/<int:id>', Database_Update.as_view()),

]
