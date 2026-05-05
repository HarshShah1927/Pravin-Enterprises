from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal
import uuid
from .models import Order, OrderItem, OrderTracking
from cart.models import Cart
from notifications.whatsapp import send_order_notification
from payments.services import generate_invoice


def serialize_order(order):
    items = []
    for item in order.items.all():
        items.append({
            "product_id": item.product.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": float(item.price),
        })
    return {
        "id": order.id,
        "user": order.user.id,
        "order_id": order.order_id,
        "total_amount": float(order.total_amount),
        "status": order.order_status,
        "invoice_ready": hasattr(order, 'invoice'),
        "items": items,
        "created_at": order.created_at,
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic()
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return Response({"error": "cart is empty"}, status=400)

    data = request.data
    required = ["shipping_address", "shipping_city", "shipping_state", "shipping_postal_code", "shipping_phone"]
    if any(field not in data or not data[field] for field in required):
        return Response({"error": "missing shipping info"}, status=400)

    order = Order.objects.create(
        order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        user=request.user,
        order_status='confirmed',
        subtotal=Decimal('0.00'),
        shipping_cost=Decimal('0.00'),
        tax=Decimal('0.00'),
        discount=Decimal('0.00'),
        shipping_address=data["shipping_address"],
        shipping_city=data["shipping_city"],
        shipping_state=data["shipping_state"],
        shipping_postal_code=data["shipping_postal_code"],
        shipping_phone=data["shipping_phone"],
        billing_address=data.get("billing_address") or data["shipping_address"],
        billing_city=data.get("billing_city") or data["shipping_city"],
        billing_state=data.get("billing_state") or data["shipping_state"],
        billing_postal_code=data.get("billing_postal_code") or data["shipping_postal_code"],
        customer_notes=data.get("customer_notes", ""),
        total_amount=Decimal('0.00'),
    )

    total = Decimal('0.00')
    for item in cart.items.select_related('product'):
        if item.product.stock < item.quantity:
            transaction.set_rollback(True)
            return Response({"error": f"product {item.product.name} out of stock"}, status=400)
        price = item.product.discount_price if item.product.discount_price else item.product.price
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=price)
        total += price * item.quantity
        item.product.stock -= item.quantity
        item.product.total_sold += item.quantity
        item.product.save()

    order.subtotal = total
    order.total_amount = total
    order.save()

    # clear cart
    cart.items.all().delete()

    # tracking
    OrderTracking.objects.create(
        order=order,
        status='confirmed',
        description='Order confirmed and ready for processing',
    )
    generate_invoice(order)
    send_order_notification(order)

    return Response(serialize_order(order))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return Response(serialize_order(order))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return Response([serialize_order(o) for o in orders])
