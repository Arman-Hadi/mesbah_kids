from django.contrib import admin

from .models import Kid


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    ordering = ['id', 'number',]
    list_display = ['number', 'name', 'parent', 'status', 'gender']
    list_filter = ['parent', 'gender',]
    search_fields = ['number', 'name',]
