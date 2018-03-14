#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
# 通用的 models
from django.db import models


class Common_Info(models.Model):
    created_user = models.CharField('创建用户', max_length=128,null=True,blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        abstract = True
