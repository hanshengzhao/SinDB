from django.db.models import Q
from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import reverse

from db_manage.models import DataBases
from libs.base_datatable.base_datatable_view import BaseDatatableView
from db_manage.forms import AddDatabaseForm
from libs.base_view import Add_View, Delete_View, Update_View, get_buttons_html


# Create your views here.


def mysql_view(request):
    paths = [
        {"name": "数据库管理", },
        {"name": " 数据库", },
    ]
    page_title = "数据库列表"
    actions = {
        "add": {
            "url": reverse("add_database"),
            "title": "添加新数据库",
            "size_y": "600px",
        },
        "delete": {
            "url": '/databases/delete/',
            "title": "删除数据库",
        },
        "update": {
            "url": '/databases/update/',
            "title": "更新数据库",
        },
    }
    return render(request, 'db_manage/db.html', locals())


class DatabaseList(BaseDatatableView):
    """
         数据库列表
    """
    model = DataBases

    columns = ['', "db_name", "project", "db_host", "db_user", "db_database", "db_charset", "operate"]
    order_columns = columns
    max_display_length = 100

    def render_column(self, row, column):
        if column == "db_host":
            if row.db_host:
                return "%s:%d" % (row.db_host, row.db_port)
            else:
                return ""
        elif column == "operate":
            # 操作界面
            buttons_info = {
                'primary': {
                    'text': '修改',
                    'onclick': 'update_item({id})'.format(id=row.id),
                },
                'dropdown_buttons': [
                    {
                        'text': '连接测试',
                        'onclick': 'connect_item({id},\'{db_name}\')'.format(id=row.id, db_name=row.db_name),
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
            return super(DatabaseList, self).render_column(row, column)

    def get_initial_queryset(self):
        return DataBases.normal_objects.all()

    def filter_queryset(self, qs):
        qs_params = None
        search = self.request.POST.get('search[value]', None)
        if search:
            q = Q(db_name__contains=search)
            qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs


class Database_Add(Add_View):
    AddForm = AddDatabaseForm
    form_title = "添加数据库"
    form_desc = ''

    def _handler_item(self, request, item):
        item.created_user = request.user
        if item.db_type == "mysql":
            item.db_driver = "pymysql"
        elif item.db_type == "oracle":
            item.db_driver = "cx_oracle"


class Database_Delete(Delete_View):
    model = DataBases


class Database_Update(Update_View):
    model = DataBases
    form = AddDatabaseForm
    form_title = "修改数据库"

    def _handler_item(self, request, item):
        print(item.db_type)
        if item.db_type == "mysql":
            item.db_driver = "pymysql"
        elif item.db_type == "oracle":
            item.db_driver = "cx_oracle"
