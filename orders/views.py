from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
import uuid
from cart.models import Cart
from .models import Order, OrderItem, OrderTracking
from .forms import CheckoutForm
from payments.services import generate_invoice
from notifications.whatsapp import send_order_notification


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def checkout_view(request):
    """Checkout view"""
    cart = request.user.cart
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            with transaction.atomic():
                order = Order.objects.create(
                    order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                    user=request.user,
                    order_status='confirmed',
                    subtotal=cart.get_total(),
                    shipping_cost=Decimal('0.00'),  # Calculate based on location
                    tax=Decimal('0.00'),  # Calculate based on location
                    discount=Decimal('0.00'),
                    total_amount=cart.get_total(),
                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_state=form.cleaned_data['shipping_state'],
                    shipping_postal_code=form.cleaned_data['shipping_postal_code'],
                    shipping_phone=form.cleaned_data['shipping_phone'],
                    billing_address=form.cleaned_data['billing_address'] or form.cleaned_data['shipping_address'],
                    billing_city=form.cleaned_data['billing_city'] or form.cleaned_data['shipping_city'],
                    billing_state=form.cleaned_data['billing_state'] or form.cleaned_data['shipping_state'],
                    billing_postal_code=form.cleaned_data['billing_postal_code'] or form.cleaned_data['shipping_postal_code'],
                    customer_notes=form.cleaned_data['customer_notes'],
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.price_at_add,
                    )
                    
                    # Decrease product stock
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.total_sold += cart_item.quantity
                    cart_item.product.save()
                
                # Create initial tracking entry
                OrderTracking.objects.create(
                    order=order,
                    status='confirmed',
                    description='Order confirmed and ready for processing'
                )

                generate_invoice(order)
                cart.items.all().delete()

            send_order_notification(order)
            
            messages.success(request, 'Order placed successfully! Your invoice is ready.')
            return redirect('order-detail', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.get_total(),
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def order_detail_view(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    tracking_history = order.tracking_history.all().order_by('timestamp')
    
    context = {
        'order': order,
        'order_items': order_items,
        'tracking_history': tracking_history,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def order_list_view(request):
    """View all user orders"""
    orders = request.user.orders.all().order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@require_http_methods(["POST"])
def update_order_status_view(request, order_id):
    """Update order status (Admin only)"""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.ORDER_STATUS_CHOICES):
        order.order_status = new_status
        order.save()
        
        # Create tracking entry
        OrderTracking.objects.create(
            order=order,
            status=new_status,
            description=f'Order status updated to {new_status}'
        )
        
        messages.success(request, f'Order status updated to {new_status}.')
    
    return redirect('admin:orders_order_change', order.id)
