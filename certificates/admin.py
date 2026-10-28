from django.contrib import admin
from .models import CertificateApplication

@admin.register(CertificateApplication)
class CertificateApplicationAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'full_name', 'certificate_type', 'status', 'created_at')
    list_filter = ('status', 'certificate_type')
    search_fields = ('tracking_id', 'full_name', 'phone')
    readonly_fields = ('tracking_id', 'certificate_uuid', 'issued_at', 'qr_code')