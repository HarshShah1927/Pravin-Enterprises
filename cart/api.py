from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from products.models import Product
from .models import Cart, CartItem


# helper serializer

def serialize_cart(cart):
    items = []
    total = 0
    for item in cart.items.all():
        price = item.product.discount_price if item.product.discount_price else item.product.price
        subtotal = price * item.quantity
        total += subtotal
        items.append({
            "id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "price": float(price),
            "quantity": item.quantity,
            "subtotal": float(subtotal),
        })
    return {"id": cart.id, "user": cart.user.id, "items": items, "total": float(total)}


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart = get_or_create_cart(request.user)
    return Response(serialize_cart(cart))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not product_id:
        return Response({"error": "product_id is required"}, status=400)
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        return Response({"error": "quantity must be positive integer"}, status=400)

    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock < quantity:
        return Response({"error": "insufficient stock"}, status=400)

    cart = get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity = item.quantity + quantity if not created else quantity
    item.save()

    return Response(serialize_cart(cart))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({"error": "quantity is required"}, status=400)
    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError()
    except (ValueError, TypeError):
        return Response({"error": "quantity must be non-negative integer"}, status=400)

    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if quantity == 0:
        item.delete()
    else:
        if item.product.stock < quantity:
            return Response({"error": "insufficient stock"}, status=400)
        item.quantity = quantity
        item.save()

    return Response(serialize_cart(cart))


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return Response(serialize_cart(cart))


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    return Response({"status": "cleared"})
