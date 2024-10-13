from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'request_type', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'request_type')
    search_fields = ('customer__username', 'description')
    readonly_fields = ('created_at', 'updated_at')