from django.contrib import admin

# Register your models here.
from db_manage.forms import DatabaseForm
from db_manage.models import *
from libs.base_admin import get_all_field


@admin.register(DataBases)
class DataBases_admin(admin.ModelAdmin):
    list_display = get_all_field(DataBases,exclude=["db_passwd",])

    search_fields = list_display
    form = DatabaseForm
