#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.db.models import Q
from django.shortcuts import render
from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect, HttpResponse
from logging import getLogger
from datetime import timedelta, datetime

from django.urls import reverse
from django.conf import settings


from db_query.models import Select_Record

# Create your views here.

logger = getLogger('SinDB')


def index_view(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse(settings.NORMAL_USER_INDEX))
    # 获取最近24 小时 查询次数
    recent_24_hours_records = Select_Record.objects.filter(created_time__gte=datetime.now() - timedelta(days=1))
    recent_24_hours_records_top = recent_24_hours_records.values_list("database__db_name",
                                                                      "database__db_database").annotate(
        query_nums=Count('id')).order_by('database__db_name')[:8]

    # 获取最近七天查询成功失败情况
    date_end = datetime.now().date() + timedelta(days=1)
    date_start = date_end - timedelta(days=7)
    recent_7_time_range = (date_start, date_end)
    recent_7_days_count = Select_Record.objects.filter(created_time__range=recent_7_time_range)
    success_q = Q(status=True)
    error_q = Q(status=False)
    recent_7_days_success = recent_7_days_count.extra(select={'created_date': 'date(created_time )'})
    recent_7_days_success_compare = recent_7_days_success.values("created_date").annotate(
        success=Count("id", filter=success_q), error=Count("id", filter=error_q)).order_by("created_date")

    percent_7_days = recent_7_days_count.values("status").annotate(nums=Count("id")).order_by("status")
    # print(percent_7_days)
    # 获取最新的十条查询记录
    recent_record = Select_Record.objects.values("id", "created_time", "created_user", "database__db_name",
                                                 "message").all().order_by("-created_time")[:5]
    # 获取最近的用户操作记录
    # recent_log = LogEntry.objects.values("id","user","action_time")[:5]
    page_title = "首页"
    return render(request, 'index.html', locals())


def not_permission(request):
    return render(request, '403.html')



