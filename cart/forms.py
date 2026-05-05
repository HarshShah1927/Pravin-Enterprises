from django import forms
from .models import CartItem

class AddToCartForm(forms.Form):
    """Form for adding items to cart"""
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number'
        })
    )


class UpdateCartForm(forms.Form):
    """Form for updating cart item quantity"""
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number'
        })
    )
