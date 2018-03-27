from django.db.models import Q
from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
import json
import time
from db_query.core import sql_query, sql_filter, database_status
from db_manage.lib import get_db_info, is_allow_query
from db_query.models import Select_Record
from libs.json_encoder import CJsonEncoder
from db_query.signal.query_signal import query_db_signal
from libs.base_datatable.base_datatable_view import BaseDatatableView
from db_manage.models import DataBases


# 数据库查询测试

# 数据库连接状态判断
def db_status(request):
    query_dict = json.loads(request.body)
    query_db_id = query_dict['db_id']
    db_connect_info = get_db_info(query_db_id)
    db_type = db_connect_info.pop("db_type")
    db_driver = db_connect_info.pop("db_driver")
    db_connect_info.pop("db_query_timeout")
    db_connect_info.pop("db_query_limit")
    status_ret = database_status("%s.%s_base" % (db_type, db_driver), db_connect_info)
    if status_ret["status"]:
        return HttpResponse("success")
    else:
        return HttpResponse(status_ret["message"])


# 数据库查询
def query_sql(request):
    if request.method == "POST":
        query_dict = json.loads(request.body)
        query_db_id = query_dict['db_id']
        # 判断当前用户是否有权限查询该数据库
        is_allow = is_allow_query(request.user, db_id=query_db_id)
        if not is_allow:
            res = {
                "status": False,
                "message": "没有权限查询"
            }
            return HttpResponse(json.dumps(res, cls=CJsonEncoder))
        query_sql = query_dict['query_sql']
        db_connect_info = get_db_info(query_db_id)
        db_type = db_connect_info.pop("db_type")
        db_driver = db_connect_info.pop("db_driver")
        db_query_timeout = db_connect_info.pop("db_query_timeout")
        db_query_limit = db_connect_info.pop("db_query_limit")
        filter_result = sql_filter(query_sql, db_type)
        if not filter_result["status"]:
            res = {
                "status": filter_result["status"],
                "message": filter_result["message"]
            }
        else:
            if db_connect_info:
                start_time = time.time()
                res = sql_query(query_sql, "%s.%s_base" % (db_type, db_driver), db_connect_info,
                                timeout=db_query_timeout, limit=db_query_limit)
                query_time = time.time() - start_time
                query_db_signal.send(
                    request, status=res["status"], query_time=query_time, message=res["message"]
                )
            else:
                res = {}

        return HttpResponse(json.dumps(res, cls=CJsonEncoder))
    else:
        paths = [
            {"name": "数据库查询", },
            {"name": "普通查询", },
        ]
        page_title = "数据库查询"
        request_user = request.user
        all_permission = request_user.select_permissions.all()
        databases = []
        projects = []
        for permission in all_permission:
            if permission.project:
                #  如果权限中勾选了项目组，所有属于该项目的数据库 都需要可查询
                for db in DataBases.objects.exclude(db_status="delete").filter(project__contains=permission.project):
                    databases.append(db)
                    # projects.append(permission.project)
            for data in permission.database.exclude(db_status="delete").only("db_name", "id", "db_database"):
                databases.append(data)
        databases = set(databases)
        return render(request, 'db_query/index.html', locals())


def query_record_index(request):
    paths = [
        {"name": "数据库查询", },
        {"name": "查询记录", },
    ]
    page_title = "查询记录"
    return render(request, 'db_query/query_record.html', locals())


class Query_Record_List(BaseDatatableView):
    """
        查询记录列表
    """
    model = Select_Record

    columns = ["id", "created_user", "database", "status", "sql", "execute_time", "message", "created_time"]
    order_columns = columns
    max_display_length = 100

    def render_column(self, row, column):
        if column == "database":
            return row.database.db_name
        else:
            return super(Query_Record_List, self).render_column(row, column)

    def get_initial_queryset(self):
        if self.request.user.is_superuser:
            return Select_Record.objects.all()
        else:
            return Select_Record.objects.filter(created_user=self.request.user)

    def filter_queryset(self, qs):
        qs_params = None
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(sql__contains=search)
            qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

#   数据库连接状态判断
