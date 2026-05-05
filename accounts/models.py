"""
Models for accounts app - User management
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be between 9 and 15 digits.')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone_number}"


class Address(models.Model):
    """Shipping and billing addresses for users"""
    ADDRESS_TYPES = [
        ('shipping', 'Shipping Address'),
        ('billing', 'Billing Address'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES)
    street_address = models.CharField(max_length=255)
    apartment_or_house = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    phone_number = models.CharField(max_length=17)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f"{self.get_address_type_display()} - {self.user.username}"


class EmailVerificationToken(models.Model):
    """Store email verification tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'email_verification_tokens'
    
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
    
    def __str__(self):
        return f"Token for {self.user.email}"


class ShopProfile(models.Model):
    """Business/Shop profile for store details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_profile')
    shop_name = models.CharField(max_length=255, help_text='Name of your hardware shop')
    gst_number = models.CharField(max_length=15, unique=True, help_text='GST Registration Number (15 digits)')
    email = models.EmailField(help_text='Office/Shop email address')
    phone_number = models.CharField(max_length=17, help_text='Shop contact number')
    whatsapp_number = models.CharField(max_length=17, blank=True, help_text='WhatsApp business number (optional)')
    
    # Address details
    shop_address = models.TextField(help_text='Complete shop/office address')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    # Bank details (optional but useful for invoicing)
    bank_name = models.CharField(max_length=100, blank=True, help_text='Bank name for invoices')
    bank_account = models.CharField(max_length=20, blank=True, help_text='Bank account number')
    ifsc_code = models.CharField(max_length=11, blank=True, help_text='IFSC code')
    
    # Business info
    registration_number = models.CharField(max_length=50, blank=True, help_text='Business registration number')
    pan_number = models.CharField(max_length=10, blank=True, help_text='PAN number (10 digits)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shop_profiles'
        verbose_name = 'Shop Profile'
        verbose_name_plural = 'Shop Profiles'
    
    def __str__(self):
        return f"{self.shop_name} - {self.gst_number}"
