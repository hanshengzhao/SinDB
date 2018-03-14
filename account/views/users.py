#!/bin/env python
# -*- coding:utf-8 -*-
# created by
from django.db.models import Q
from django.shortcuts import render
from django.urls.base import reverse
from account.models import User
from libs.base_datatable.base_datatable_view import BaseDatatableView
from account.forms import AddUserForm, ChangePasswordForm
from libs.base_view import Add_View, Delete_View, Update_View, get_buttons_html


def user_manage(request):
    paths = [
        {"name": "基本管理", },
        {"name": "用户管理", },
    ]
    page_title = "用户列表"
    actions = {
        "add": {
            "url": reverse("add_user"),
            "title": "添加新用户",
        },
        "delete": {
            "url": '/account/user/delete/',
            "title": "删除用户",
        },
        "update": {
            "url": '/account/user/update/',
            "title": "更新用户",
        },
        "change_password": {
            "url": '/account/user/change_password/',
            "title": "更新用户密码",
        },
    }
    return render(request, 'account/users.html', locals())


class UserList(BaseDatatableView):
    """
        用户列表
    """
    model = User

    columns = ['', "id", "username", "email", "select_permissions", "is_staff", "date_joined", "operate"]
    order_columns = columns
    max_display_length = 100

    def render_column(self, row, column):
        if column == "select_permissions":
            if row.select_permissions:
                permission_name = ""
                for i in row.select_permissions.all():
                    permission_name = i.permission_name + " " + permission_name
                return permission_name
            else:
                return ""
        elif column == "operate":
            # 操作界面
            buttons_info = {
                'primary':{
                    'text':'修改',
                    'onclick':'update_item({id})'.format(id=row.id),
                },
                'dropdown_buttons':[
                    {
                        'text':'修改密码',
                        'onclick':'change_password({id})'.format(id=row.id),
                    },
                    {
                        'text': '删除',
                        'onclick': 'delete_item({id})'.format(id=row.id),
                    },

                ],
            }
            operate_html = get_buttons_html(buttons_info)
            return operate_html
        else:
            return super(UserList, self).render_column(row, column)

    def get_initial_queryset(self):
        return User.objects.all()

    def filter_queryset(self, qs):
        qs_params = None
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(username__contains=search)
            qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs


class User_Add(Add_View):
    AddForm = AddUserForm
    form_title = "添加用户"
    form_desc = None

    # template_name = 'base/add_or_update_form.html'

    def _handler_item(self, request, item):
        item.set_password("123")


class User_Delte(Delete_View):
    model = User

    def _permission(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return True
        else:
            return False


class User_Update(Update_View):
    model = User
    form = AddUserForm
    form_title = "修改用户"


class User_Passwd_Update(Update_View):
    model = User
    form = ChangePasswordForm
    form_title = "修改用户密码"
