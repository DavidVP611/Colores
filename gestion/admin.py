from django.contrib import admin
from .models import *
# Register your models here.

class ColorsAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "quantity")
    search_fields = ("code", "name")
    list_filter = ("name", )
    ordering = ("name", "code")
admin.site.register(Colors_Inventory ,ColorsAdmin)
