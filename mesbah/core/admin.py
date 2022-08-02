from django.contrib import admin

from .models import Kid


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    ordering = ['number',]
    list_display = ['number', 'name', 'parent', 'status',]
    list_filter = ['parent', 'gender',]
    search_fields = ['number', 'name',]
