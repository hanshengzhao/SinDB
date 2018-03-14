from django.contrib import admin

# Register your models here.
from db_manage.models import *
from libs.base_admin import get_all_field

@admin.register(DataBases)
class DataBases_admin(admin.ModelAdmin):
    list_display = get_all_field(DataBases)
    search_fields = list_display

    def delete_model(self, request, obj):
        # 删除时把状态置为delete,实际不删除
        obj.db_status = 'delete'
        obj.save()
