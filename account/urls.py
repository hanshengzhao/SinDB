#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

from django.urls import path

from account.views.users import *
from account.views.permissions import *

# path 不需要写r  不需要写 ^
# 如果要使用之前的url 使用re_path 就可以



urlpatterns = [
    path('user/', user_manage, name="account_users_index"),
    path('user/list/', UserList.as_view(), name='account_users_list'),
    path('user/add/', User_Add.as_view(), name="add_user"),
    path('user/delete/<int:id>', User_Delte.as_view(), name="delete_user"),
    path('user/update/<int:id>', User_Update.as_view(), name="update_user"),
    path('user/change_password/<int:id>', User_Passwd_Update.as_view(), name="change_password"),
    path('permission/', permission_manage, name='account_permissions_index'),
    path('permission/list/', PermissionList.as_view(), name='account_permissions_list'),
    path('permission/add/', Permission_Add.as_view(), name="add_permission"),
    path('permission/delete/<int:id>', Permission_Delete.as_view()),
    path('permission/update/<int:id>', Permission_Update.as_view()),
]
