from django.contrib import admin

# Register your models here.
from .models import User, Ticket



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'request_type', 'created_at', 'assigned_to', 'updated_at', 'created_by']
    list_filter = ['status', 'priority', 'request_type', 'created_at', 'assigned_to', 'updated_at', 'created_by']
    search_fields = ['title', 'description']

