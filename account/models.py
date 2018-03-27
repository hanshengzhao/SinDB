from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from db_manage.models import DataBases
from libs.base_model import Common_Info
from libs.utils.common_data.cmdb_data import get_projects


# Create your models here.

# 查询权限
class Select_Permission(Common_Info):
    permission_name = models.CharField('权限名称', max_length=128)
    database = models.ManyToManyField(DataBases, verbose_name='数据库权限',blank=True)
    project = models.CharField('项目组权限', max_length=128, choices=get_projects(), null=True, blank=True)
    common = models.TextField('备注')

    def __str__(self):
        return self.permission_name

    class Meta:
        verbose_name = '查询权限'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        permissions = (
            ("can_manage", 'can manage permission'),
        )


class My_UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    select_permissions = models.ManyToManyField(Select_Permission, verbose_name=u'查询权限', blank=True)
    # 取消first_name 和 last_name
    first_name = models.Empty
    last_name = models.Empty

    objects = My_UserManager()

    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']
