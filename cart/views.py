from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem
from .forms import AddToCartForm, UpdateCartForm


def get_or_create_cart(user):
    """Get or create cart for user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_to_cart_view(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    form = AddToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        
        # Check stock
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('product-detail', slug=product.slug)
        
        cart = get_or_create_cart(request.user)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price_at_add': product.get_discounted_price(), 'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already in cart
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(request, f'Only {product.stock} items available in stock.')
                return redirect('product-detail', slug=product.slug)
            
            cart_item.quantity = new_quantity
            cart_item.save()
        
        # Update cart total
        cart.total_items = sum(item.quantity for item in cart.items.all())
        cart.total_price = cart.get_total()
        cart.save()
        
        messages.success(request, f'{product.name} added to cart successfully!')
        
        # Return JSON response if AJAX request
        if request.headers.get('accept') == 'application/json':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart',
                'cart_count': cart.get_item_count(),
                'cart_total': str(cart.get_total())
            })
        
        return redirect('cart')
    
    messages.error(request, 'Invalid quantity.')
    return redirect('product-detail', slug=product.slug)


@login_required(login_url='login')
@require_http_methods(["GET"])
def view_cart(request):
    """View shopping cart"""
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.get_total(),
        'item_count': cart.get_item_count(),
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_cart_item_view(request, item_id):
    """Update cart item quantity"""
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    form = UpdateCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        
        if quantity == 0:
            # Remove item if quantity is 0
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            # Check stock
            if quantity > cart_item.product.stock:
                messages.error(request, f'Only {cart_item.product.stock} items available in stock.')
                return redirect('cart')
            
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        
        # Update cart totals
        cart.total_items = sum(item.quantity for item in cart.items.all())
        cart.total_price = cart.get_total()
        cart.save()
        
        # Return JSON response if AJAX request
        if request.headers.get('accept') == 'application/json':
            return JsonResponse({
                'success': True,
                'cart_total': str(cart.get_total()),
                'item_total': str(cart_item.get_total()),
                'item_count': cart.get_item_count()
            })
    else:
        messages.error(request, 'Invalid quantity.')
    
    return redirect('cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_from_cart_view(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    product_name = cart_item.product.name
    cart_item.delete()
    
    # Update cart totals
    cart.total_items = sum(item.quantity for item in cart.items.all())
    cart.total_price = cart.get_total()
    cart.save()
    
    messages.success(request, f'{product_name} removed from cart.')
    
    # Return JSON response if AJAX request
    if request.headers.get('accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'cart_total': str(cart.get_total()),
            'item_count': cart.get_item_count()
        })
    
    return redirect('cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def clear_cart_view(request):
    """Clear entire cart"""
    cart = get_or_create_cart(request.user)
    cart.clear()
    messages.success(request, 'Cart cleared successfully.')
    return redirect('home')


@login_required(login_url='login')
@require_http_methods(["GET"])
def get_cart_summary(request):
    """Get cart summary (for AJAX)"""
    cart = get_or_create_cart(request.user)
    
    return JsonResponse({
        'item_count': cart.get_item_count(),
        'total': str(cart.get_total()),
        'items': [{
            'name': item.product.name,
            'quantity': item.quantity,
            'price': str(item.price_at_add),
            'total': str(item.get_total())
        } for item in cart.items.all()]
    })
