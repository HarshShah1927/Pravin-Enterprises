from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from orders.models import Order


def is_shop_owner(user):
    return user.is_active and user.is_superuser


@user_passes_test(is_shop_owner)
@require_http_methods(["GET"])
def send_notification_view(request, order_id):
    """Admin view to send WhatsApp notification for an order"""
    from .whatsapp import send_order_notification
    from django.contrib import messages
    from django.shortcuts import redirect
    
    order = Order.objects.get(id=order_id)
    
    if send_order_notification(order):
        messages.success(request, 'WhatsApp notification sent successfully!')
    else:
        messages.error(request, 'Failed to send WhatsApp notification.')
    
    return redirect('admin:orders_order_change', order.id)
