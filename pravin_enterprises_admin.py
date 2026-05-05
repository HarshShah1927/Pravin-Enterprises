from django.contrib import admin

# Central admin site configuration for simplified labels
admin.site.site_header = 'Pravin Enterprises — Seller Dashboard'
admin.site.site_title = 'Pravin Admin'
admin.site.index_title = 'Quick Actions'


def shop_owner_admin_permission(request):
    """Allow only the shop owner/superuser into Django admin."""
    return request.user.is_active and request.user.is_superuser


admin.site.has_permission = shop_owner_admin_permission
