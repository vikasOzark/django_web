from django.contrib import admin
from .models import StocksModel, UserQueryModel
from import_export.admin import ExportActionMixin

# Register your models here.
@admin.register(StocksModel)
class Admin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('stock_name', 'symbol', 'price', 'timestamp')


@admin.register(UserQueryModel)
class StocksAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user', 'stocks', 'query', 'timestamp')
