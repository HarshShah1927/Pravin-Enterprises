from django import forms
from .models import Order
from accounts.models import Address

class CheckoutForm(forms.Form):
    """Form for checkout"""
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Street Address',
            'rows': 2
        })
    )
    shipping_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    shipping_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State'
    }))
    shipping_postal_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Postal Code'
    }))
    shipping_phone = forms.CharField(max_length=17, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+91 XXXXXXXXXX'
    }))
    
    billing_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Street Address',
            'rows': 2
        })
    )
    billing_city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    billing_state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State'
    }))
    billing_postal_code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Postal Code'
    }))
    
    same_as_shipping = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Billing address same as shipping'
    )
    
    customer_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Add any special instructions...',
            'rows': 3
        })
    )
