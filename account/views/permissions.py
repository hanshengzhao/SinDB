#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.db.models import Q
from django.shortcuts import render
from django.urls.base import reverse
from account.models import Select_Permission
from libs.base_datatable.base_datatable_view import BaseDatatableView
from account.forms import AddPermissionForm
from libs.base_view import Add_View, Delete_View, Update_View, get_buttons_html


def permission_manage(request):
    paths = [
        {"name": "基本管理", },
        {"name": "权限管理", },
    ]
    page_title = "权限列表"
    actions = {
        "add": {
            "url": reverse("add_permission"),
            "title": "添加新权限",
        },
        "delete": {
            "url": '/account/permission/delete/',
            "title": "删除权限",
        },
        "update": {
            "url": '/account/permission/update/',
            "title": "更新权限",
        },
    }
    return render(request, 'account/permissions.html', locals())


class PermissionList(BaseDatatableView):
    """
        权限列表
    """
    model = Select_Permission

    columns = ['', "id", "permission_name", "project", "database", "common", "created_user", "created_time", "operate"]
    order_columns = columns
    max_display_length = 100
    from libs.utils.common_data.cmdb_data import get_projects
    all_projects = get_projects()

    def render_column(self, row, column):
        if column == "database":
            databases_name = ""
            for i in row.database.all():
                databases_name = i.db_name + "(" + i.db_database + ")   " + databases_name
            return databases_name
        elif column == "project":

            for project_name, project_ch_name in self.all_projects:
                if row.project == project_name:
                    return project_ch_name
            else:
                return "--"
        elif column == "operate":
            # 操作界面
            buttons_info = {
                'primary': {
                    'text': '修改',
                    'onclick': 'update_item({id})'.format(id=row.id),
                },
                'dropdown_buttons': [
                    {
                        'text': '删除',
                        'onclick': 'delete_item({id})'.format(id=row.id),
                    },
                ],
            }
            operate_html = get_buttons_html(buttons_info)
            return operate_html
        else:
            return super(PermissionList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Select_Permission.objects.all()

    def filter_queryset(self, qs):
        qs_params = None
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(username__contains=search)
            qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs


class Permission_Add(Add_View):
    AddForm = AddPermissionForm
    form_title = ""
    form_desc = ''

    def _handler_item(self, request, item):
        item.created_user = request.user


class Permission_Delete(Delete_View):
    model = Select_Permission

    def _permission(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return True
        else:
            return False


class Permission_Update(Update_View):
    model = Select_Permission
    form = AddPermissionForm
    form_title = "修改权限"
