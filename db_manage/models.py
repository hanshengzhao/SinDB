from __future__ import unicode_literals

from django.db import models

from libs.config import get_conf_items
from libs.base_model import Common_Info
from libs.base_fields import AESCharField

# Create your models here.


# 数据库管理表
from libs.utils.common_data.cmdb_data import get_projects


class DataBaseManagerNormal(models.Manager):
    def get_queryset(self):
        # 删除的不返回
        return super().get_queryset().exclude(db_status="delete")


class DataBases(Common_Info):
    db_type_choice = (get_conf_items('db_type'))
    db_status_choice = (get_conf_items('db_status'))
    db_name = models.CharField('名称', max_length=128)
    project = models.CharField('项目组', max_length=128, choices=get_projects())
    db_host = models.CharField('数据库主机', max_length=128)
    db_port = models.IntegerField('数据库端口', default=3306)
    db_type = models.CharField('数据库类型', choices=db_type_choice, max_length=128)
    db_driver = models.CharField("数据库驱动", max_length=128, default="pymysql")
    db_version = models.CharField('数据库版本', max_length=128, default="v")
    db_user = models.CharField('数据库用户', max_length=128)
    db_passwd = AESCharField('数据库密码', max_length=128)
    db_database = models.CharField('操作数据库', max_length=128)
    db_charset = models.CharField("数据库字符集", max_length=128, default="utf8")
    db_query_timeout = models.IntegerField("数据库查询超时时间", default=20)
    db_query_limit = models.IntegerField("数据库查询限制", default=20)
    is_notify = models.BooleanField('开启通知', default=False)
    notify_url = models.URLField('通知地址', null=True, blank=True)
    notify_email = models.CharField('提醒邮件', max_length=128, blank=True, null=True)
    db_status = models.CharField('数据库状态', choices=db_status_choice, max_length=128, blank=True, null=True)
    normal_objects = DataBaseManagerNormal()

    def __str__(self):
        return "%s:%s" % (self.db_name, self.db_database)

    class Meta:
        verbose_name = '数据库'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        permissions = (
            ("can_manage", 'can manage database'),
        )
        default_permissions = ()

    def delete(self, using=None, keep_parents=False):
        self.db_status = "delete"
        self.save()
