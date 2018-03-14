#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.forms import models
from db_manage.models import DataBases
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from libs.utils.common_data.cmdb_data import get_projects


class AddDatabaseForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

        self.base_fields['db_type'].initial = "mysql"
        super(AddDatabaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataBases
        exclude = ("id", "created_user", "is_notify", "notify_url", "notify_email", "db_status", "db_query_limit",
                   "db_query_timeout", "db_charset", "db_version", "db_driver")
        widgets = {
            # render_value 用来回显 密码 ,否则设置为passwordinput的话 修改的时候就为空了
            "db_passwd": Fwidgets.PasswordInput(render_value=True),
        }
