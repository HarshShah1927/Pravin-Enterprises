from django.contrib import admin
from .models import UserProfile, Address, EmailVerificationToken, ShopProfile

@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    """Simplified admin for shop owner's business details"""
    list_display = ['shop_name', 'get_owner_name', 'gst_number', 'city', 'phone_number']
    list_filter = ['city', 'state', 'created_at']
    search_fields = ['shop_name', 'gst_number', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('🏪 Shop Information', {
            'fields': ('user', 'shop_name', 'gst_number', 'registration_number', 'pan_number'),
            'description': 'Your shop/business details'
        }),
        ('📞 Contact Details', {
            'fields': ('email', 'phone_number', 'whatsapp_number'),
            'description': 'How customers can reach you'
        }),
        ('📍 Address', {
            'fields': ('shop_address', 'city', 'state', 'postal_code', 'country'),
            'description': 'Shop location details'
        }),
        ('🏦 Bank Details (Optional)', {
            'fields': ('bank_name', 'bank_account', 'ifsc_code'),
            'classes': ('collapse',),
            'description': 'For invoicing and payments'
        }),
        ('📅 System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_owner_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_owner_name.short_description = 'Owner'
    
    def has_add_permission(self, request):
        """Prevent adding duplicate shop profiles"""
        return not ShopProfile.objects.exists() or request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superadmin can delete"""
        return request.user.is_superuser


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Simplified admin for customer profiles"""
    list_display = ['get_user_name', 'phone_number', 'city', 'is_email_verified', 'created_at']
    list_filter = ['is_email_verified', 'city', 'state', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('👤 User Info', {
            'fields': ('user',),
            'description': 'Customer account'
        }),
        ('📞 Contact Info', {
            'fields': ('phone_number',),
        }),
        ('👨 Personal Details', {
            'fields': ('gender', 'date_of_birth'),
            'classes': ('collapse',)
        }),
        ('📍 Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country'),
        }),
        ('✅ Verification Status', {
            'fields': ('is_email_verified', 'is_phone_verified'),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'Customer'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Simplified admin for customer addresses"""
    list_display = ['user', 'address_type', 'city', 'state', 'is_default']
    list_filter = ['address_type', 'country', 'is_default', 'created_at']
    search_fields = ['user__username', 'user__email', 'city', 'state']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('📋 Address Info', {
            'fields': ('user', 'address_type', 'is_default'),
            'description': 'Select user and address type'
        }),
        ('📍 Location', {
            'fields': ('street_address', 'apartment_or_house', 'city', 'state', 'postal_code', 'country'),
        }),
        ('📞 Contact', {
            'fields': ('phone_number',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """Simplified admin for email tokens"""
    list_display = ['user', 'is_used', 'is_valid', 'created_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at']
    
    fieldsets = (
        ('🔐 Token Info', {
            'fields': ('user', 'token'),
        }),
        ('✅ Status', {
            'fields': ('is_used', 'expires_at'),
        }),
        ('📅 Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual token creation"""
        return False

