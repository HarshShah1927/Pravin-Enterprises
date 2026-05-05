"""
Models for cart app - Shopping cart management
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal

class Cart(models.Model):
    """Shopping cart for each user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    total_items = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total(self):
        """Calculate total cart value"""
        return sum(item.get_total() for item in self.items.all())
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()
        self.total_items = 0
        self.total_price = 0
        self.save()


class CartItem(models.Model):
    """Individual items in the shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_add = models.DecimalField(max_digits=10, decimal_places=2)  # Price when added to cart
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity})"
    
    def get_total(self):
        """Get total price for this item"""
        return self.price_at_add * self.quantity
    
    def get_current_product_price(self):
        """Get current product price"""
        return self.product.get_discounted_price()
    
    def price_changed(self):
        """Check if product price has changed since adding to cart"""
        return self.price_at_add != self.get_current_product_price()
