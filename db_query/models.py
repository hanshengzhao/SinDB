from __future__ import unicode_literals

from django.db import models

from db_manage.models import DataBases

from libs.base_model import Common_Info


# Create your models here.

# 查询记录

class Select_Record(Common_Info):
    sql = models.TextField('执行SQL')
    status = models.BooleanField('执行状态', max_length=128)
    database = models.ForeignKey(DataBases, verbose_name='查询数据库',on_delete=models.CASCADE)
    execute_time = models.DecimalField('执行耗时',max_digits=5,decimal_places=2)
    message = models.CharField("执行结果",max_length=512,default=True,blank=True)

    def __unicode__(self):
        return self.sql

    class Meta:
        verbose_name = '查询记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        default_permissions = ()