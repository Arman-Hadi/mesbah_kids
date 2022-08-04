from django.contrib import admin

from .models import Kid


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    ordering = ['status', 'gender', 'gate_in', 'gate_out',
        'first_name', 'last_name', '-number',]
    list_display = ['first_name', 'last_name', 'gender',
        'caretaker', 'status', 'number']
    list_filter = ['gender', 'gate_in', 'gate_out', 'status',]
    search_fields = ['first_name', 'last_name', 'caretaker_name', 'number']
