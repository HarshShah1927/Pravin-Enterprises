from django.contrib import admin
from .models import Category, Product, ProductReview, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Simplified product category admin"""
    list_display = ['name', 'product_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('📦 Category Info', {
            'fields': ('name', 'slug', 'description', 'image'),
        }),
        ('✅ Status', {
            'fields': ('is_active',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Simplified product admin for easy management"""
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'get_stock_status', 'is_active']
    list_filter = ['category', 'is_active', 'is_featured', 'is_new']
    search_fields = ['name', 'sku', 'manufacturer']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['average_rating', 'review_count', 'total_sold', 'created_at', 'updated_at']
    
    fieldsets = (
        ('🏷️ Basic Info', {
            'fields': ('category', 'name', 'slug', 'sku'),
            'description': 'Product name and category'
        }),
        ('📝 Description', {
            'fields': ('short_description', 'description'),
        }),
        ('💰 Pricing', {
            'fields': ('price', 'discount_price', 'cost_price'),
            'description': 'Cost price is for internal tracking only'
        }),
        ('📊 Stock Management', {
            'fields': ('stock', 'low_stock_threshold'),
            'description': 'Set low_stock_threshold to be notified when stock runs low'
        }),
        ('🖼️ Images', {
            'fields': ('image', 'additional_images'),
        }),
        ('🔧 Product Specifications', {
            'fields': ('weight', 'dimensions', 'manufacturer', 'warranty_months'),
            'classes': ('collapse',),
            'description': 'Technical details and warranty info'
        }),
        ('✅ Display Settings', {
            'fields': ('is_active', 'is_featured', 'is_new'),
            'description': 'Control product visibility and special labels'
        }),
        ('⭐ Performance', {
            'fields': ('average_rating', 'review_count', 'total_sold'),
            'classes': ('collapse',)
        }),
        ('📅 System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_stock_status(self, obj):
        if obj.stock == 0:
            return '❌ Out of Stock'
        elif obj.stock < obj.low_stock_threshold:
            return '⚠️ Low Stock'
        return '✅ In Stock'
    get_stock_status.short_description = 'Stock Status'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Simplified product review admin"""
    list_display = ['product', 'get_user_name', 'rating', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['product__name', 'user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('📝 Review Info', {
            'fields': ('product', 'user', 'title'),
        }),
        ('⭐ Rating', {
            'fields': ('rating', 'is_verified_purchase'),
        }),
        ('💬 Comment', {
            'fields': ('comment',),
        }),
        ('👍 Helpful', {
            'fields': ('helpful_count',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'User'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Contact messages from customers"""
    list_display = ['name', 'email', 'subject', 'category', 'get_status_badge', 'created_at']
    list_filter = ['category', 'is_read', 'is_resolved', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('👤 Sender Info', {
            'fields': ('name', 'email', 'phone'),
        }),
        ('📝 Message', {
            'fields': ('subject', 'category', 'message'),
        }),
        ('📊 Status', {
            'fields': ('is_read', 'is_resolved'),
        }),
        ('💬 Response', {
            'fields': ('response', 'response_date'),
            'classes': ('collapse',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status_badge(self, obj):
        if obj.is_resolved:
            return '✅ Resolved'
        elif obj.is_read:
            return '👀 Read'
        return '🔔 New'
    get_status_badge.short_description = 'Status'
