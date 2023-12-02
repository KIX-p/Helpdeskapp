from django.contrib import admin

# Register your models here.
from .models import ITuser, Ticket

@admin.register(ITuser)
class ITuserAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    list_filter = ['user']
    search_fields = ['user__username']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'request_type', 'created_at', 'assigned_to', 'updated_at', 'created_by']
    list_filter = ['status', 'priority', 'request_type', 'created_at', 'assigned_to', 'updated_at', 'created_by']
    search_fields = ['title', 'description']

