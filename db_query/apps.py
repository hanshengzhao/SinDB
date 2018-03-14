from __future__ import unicode_literals

from django.apps import AppConfig


class DbQueryConfig(AppConfig):
    name = 'db_query'
    verbose_name = '查询管理'

    def ready(self):
        import db_query.signal.query_receiver
