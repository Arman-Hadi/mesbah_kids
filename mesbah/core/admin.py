from django.contrib import admin

from .models import Kid, StatusChange


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    ordering = ['status', 'gender', 'gate_in', 'gate_out',
        'first_name', 'last_name', '-number',]
    list_display = ['first_name', 'last_name', 'gender',
        'caretaker', 'status', 'number']
    list_filter = ['gender', 'gate_in', 'gate_out', 'status',]
    search_fields = ['first_name', 'last_name', 'caretaker_name', 'number']


@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = ['kid', 'user', 'previous_status', 'status', 'created_at']
    list_filter = ['user', 'previous_status', 'status']
    search_fields = ['kid', 'user']
