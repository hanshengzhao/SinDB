#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.forms import models
from account.models import User, Select_Permission
from django.forms import widgets as Fwidgets

from libs.utils.common_data.cmdb_data import get_projects


class AddUserForm(models.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "select_permissions")
        # widgets = {
        #     'username': Fwidgets.Input(attrs={'class': 'form-control'}),
        #     'email': Fwidgets.EmailInput(attrs={'class': 'form-control'}),
        #     'select_permissions': Fwidgets.SelectMultiple(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

        super(AddUserForm, self).__init__(*args, **kwargs)


class AddPermissionForm(models.ModelForm):
    class Meta:
        model = Select_Permission
        fields = ("permission_name", "project", "database", "common")

    def __init__(self, *args, **kwargs):
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

        # self.base_fields['project'].choices = get_projects()
        super(AddPermissionForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(models.ModelForm):
    class Meta:
        model = User
        fields = ("password",)
        widgets = {
            'password': Fwidgets.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data['password'])
        if commit:
            self.instance.save()
        return self.instance
