from django.contrib import admin
from db_query.models import Select_Record
# Register your models here.
from libs.base_admin import get_all_field


@admin.register(Select_Record)
class Select_Record_admin(admin.ModelAdmin):
    list_display = get_all_field(Select_Record)
    search_fields = list_display
