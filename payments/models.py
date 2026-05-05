"""
Models for payments app - Payment processing
"""

from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class Payment(models.Model):
    """Payment transactions"""
    PAYMENT_METHOD_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('cod', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Payment Information
    payment_id = models.CharField(max_length=100, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Payment Details
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='initiated')
    
    # Gateway Information
    gateway_reference_id = models.CharField(max_length=200, blank=True, null=True)
    gateway_response = models.JSONField(null=True, blank=True)
    
    # Additional Details
    email = models.EmailField()
    phone = models.CharField(max_length=17)
    description = models.TextField(blank=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment {self.payment_id}"


class Invoice(models.Model):
    """Invoice generation and storage"""
    invoice_number = models.CharField(max_length=50, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True)
    
    # Customer Information
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=17)
    
    # Invoice Details
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # File
    pdf_file = models.FileField(upload_to='invoices/')
    
    # Dates
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoices'
        ordering = ['-invoice_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number}"
    
    def get_formatted_date(self):
        return self.invoice_date.strftime("%d-%m-%Y")


class InvoiceTemplate(models.Model):
    """Admin-editable invoice PDF content."""
    name = models.CharField(max_length=100, default='Default Invoice Template')
    company_name = models.CharField(max_length=255, default='Pravin Enterprises')
    company_address = models.TextField(blank=True)
    company_phone = models.CharField(max_length=30, blank=True)
    company_email = models.EmailField(blank=True, default='pravin@enterprises.com')
    title = models.CharField(max_length=100, default='Tax Invoice')
    footer_message = models.TextField(default='Thank you for your purchase!')
    terms_and_conditions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoice_templates'
        ordering = ['-is_active', 'name']

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    """Saved payment methods for users"""
    CARD_TYPE_CHOICES = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('upi', 'UPI'),
        ('wallet', 'Digital Wallet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    card_token = models.CharField(max_length=200, unique=True)  # Token from payment gateway
    last_four = models.CharField(max_length=4)  # Last 4 digits of card
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_methods'
    
    def __str__(self):
        return f"{self.get_card_type_display()} ending in {self.last_four}"
