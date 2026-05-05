"""
Main URL configuration for pravin_enterprises project.
"""

from django.contrib import admin
from django.urls import path, include
from .api_root import api_root
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', api_root),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('', include('products.urls')),  # Home page

    # REST API endpoints
    path('api/cart/', include('cart.api_urls')),
    path('api/orders/', include('orders.api_urls')),
    path('api/shop/', include('products.api_urls')),
]


def shop_owner_admin_permission(request):
    """Allow only the shop owner/superuser into Django admin."""
    return request.user.is_active and request.user.is_superuser


admin.site.has_permission = shop_owner_admin_permission

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
