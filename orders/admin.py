from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, OrderTracking, Refund

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Simplified order management for shop owners"""
    list_display = ['order_id', 'customer_name', 'total_amount', 'get_order_status_badge', 'created_at']
    list_filter = ['order_status', 'created_at']
    search_fields = ['order_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['order_id', 'created_at', 'updated_at', 'shipped_at', 'delivered_at']
    
    fieldsets = (
        ('📋 Order Details', {
            'fields': ('order_id', 'user'),
            'description': 'Customer and order identification'
        }),
        ('💰 Pricing Breakdown', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount'),
        }),
        ('📍 Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_phone'),
            'description': 'Where to deliver the order'
        }),
        ('💳 Billing Address', {
            'fields': ('billing_address', 'billing_city', 'billing_state', 'billing_postal_code'),
            'classes': ('collapse',),
            'description': 'For invoicing'
        }),
        ('📊 Status', {
            'fields': ('order_status',),
            'description': 'Order status'
        }),
        ('🚚 Tracking Info', {
            'fields': ('tracking_number', 'estimated_delivery'),
            'classes': ('collapse',),
            'description': 'Shipping and delivery details'
        }),
        ('📝 Notes', {
            'fields': ('customer_notes', 'admin_notes'),
            'classes': ('collapse',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def customer_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    customer_name.short_description = 'Customer'
    
    def get_order_status_badge(self, obj):
        colors = {
            'pending': '#FFC107',
            'confirmed': '#17A2B8',
            'processing': '#007BFF',
            'shipped': '#28A745',
            'delivered': '#20C997',
            'cancelled': '#DC3545',
            'returned': '#6C757D'
        }
        color = colors.get(obj.order_status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_order_status_display()
        )
    get_order_status_badge.short_description = 'Order Status'
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order items inline view"""
    list_display = ['order_link', 'product', 'quantity', 'price', 'get_subtotal']
    list_filter = ['order__created_at']
    search_fields = ['order__order_id', 'product__name']
    readonly_fields = ['order', 'product', 'quantity', 'price', 'subtotal']
    
    fieldsets = (
        ('📦 Item Details', {
            'fields': ('order', 'product', 'quantity', 'price', 'subtotal'),
        }),
    )
    
    def order_link(self, obj):
        return obj.order.order_id
    order_link.short_description = 'Order'
    
    def get_subtotal(self, obj):
        return f"₹{obj.subtotal}"
    get_subtotal.short_description = 'Subtotal'


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    """Order tracking history"""
    list_display = ['order', 'status', 'get_status_icon', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['order__order_id']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('📍 Tracking Info', {
            'fields': ('order', 'status', 'description'),
        }),
        ('📅 Timestamp', {
            'fields': ('timestamp',),
        }),
    )
    
    def get_status_icon(self, obj):
        icons = {
            'pending': '⏳',
            'confirmed': '✅',
            'processing': '⚙️',
            'shipped': '📦',
            'out_for_delivery': '🚚',
            'delivered': '✨'
        }
        return icons.get(obj.status, '📍')
    get_status_icon.short_description = ''


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """Refund management"""
    list_display = ['order', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('💸 Refund Details', {
            'fields': ('order', 'amount', 'reason'),
        }),
        ('📊 Status', {
            'fields': ('status',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
