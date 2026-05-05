from django.contrib import admin

from .models import Invoice, InvoiceTemplate
from .services import generate_invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Invoice management and download."""
    list_display = ['invoice_number', 'order_link', 'customer_name', 'total_amount', 'invoice_date']
    list_filter = ['invoice_date']
    search_fields = ['invoice_number', 'customer_email', 'order__order_id']
    readonly_fields = ['invoice_date', 'created_at']
    actions = ['regenerate_selected_invoices']

    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'order', 'invoice_date'),
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_email', 'customer_phone'),
        }),
        ('Amount', {
            'fields': ('subtotal', 'tax', 'shipping_cost', 'discount', 'total_amount'),
        }),
        ('File', {
            'fields': ('pdf_file',),
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def order_link(self, obj):
        return obj.order.order_id
    order_link.short_description = 'Order'

    @admin.action(description='Regenerate selected invoice PDFs using the active template')
    def regenerate_selected_invoices(self, request, queryset):
        for invoice in queryset.select_related('order'):
            generate_invoice(invoice.order, payment=invoice.payment, replace=True)
        self.message_user(request, f'{queryset.count()} invoice PDF(s) regenerated.')


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    """Invoice PDF template content controlled by admin."""
    list_display = ['name', 'company_name', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'company_name', 'company_email']

    fieldsets = (
        ('Template', {
            'fields': ('name', 'is_active', 'title'),
        }),
        ('Company Details', {
            'fields': ('company_name', 'company_address', 'company_phone', 'company_email'),
        }),
        ('Invoice Text', {
            'fields': ('footer_message', 'terms_and_conditions'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            InvoiceTemplate.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)
