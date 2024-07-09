from django.contrib import admin
from django.utils import timezone

from .models import Kid, StatusChange



@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    ordering = ['status', 'gender', 'gate_in', 'gate_out',
        'first_name', 'last_name', '-number',]
    list_display = ['first_name', 'last_name', 'gender',
        'caretaker', 'status', 'number']
    list_filter = ['gender', 'gate_in', 'gate_out', 'status',]
    search_fields = ['first_name', 'last_name', 'caretaker_name', 'number']
    actions = ['calculate_age',]

    @admin.action(description="Calculate Age")
    def calculate_age(modeladmin, request, queryset):
        for q in queryset:
            q.calculate_age()


@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = ['kid', 'user', 'previous_status', 'status', 'created_at']
    list_filter = ['user', 'previous_status', 'status']
    search_fields = ['kid', 'user']
