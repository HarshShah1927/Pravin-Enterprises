from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, Address, ShopProfile
import re

class UserRegistrationForm(UserCreationForm):
    """Form for user registration with shop details"""
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password (min 8 characters, 1 letter, 1 number)'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    
    # Shop/Business Details
    shop_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Shop/Business Name'
    }))
    gst_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'GST Number (15 digits)'
    }))
    phone_number = forms.CharField(max_length=17, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Shop Contact Number'
    }))
    shop_address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Complete Shop/Office Address',
        'rows': 2
    }))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State'
    }))
    postal_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Postal Code'
    }))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_gst_number(self):
        gst = self.cleaned_data.get('gst_number').upper().replace(' ', '')
        if len(gst) != 15:
            raise forms.ValidationError('GST number must be exactly 15 characters.')
        # GSTIN format: 2-digit state code + PAN + entity code + Z + checksum.
        if not re.fullmatch(r'\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]', gst):
            raise forms.ValidationError('Invalid GST number format. Example: 27AJQPB1306D1ZQ')
        return gst
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.replace(' ', '').replace('+', '').replace('-', '').isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'\d', password):
            raise forms.ValidationError('Password must contain at least one digit.')
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError('Password must contain at least one letter.')
        return password


class ShopProfileForm(forms.ModelForm):
    """Form for updating shop/business profile"""
    phone_number = forms.CharField(max_length=17, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Shop Contact Number'
    }))
    whatsapp_number = forms.CharField(max_length=17, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'WhatsApp Number (Optional)'
    }))
    
    class Meta:
        model = ShopProfile
        fields = ['shop_name', 'gst_number', 'email', 'phone_number', 'whatsapp_number', 
                 'shop_address', 'city', 'state', 'postal_code', 'country',
                 'bank_name', 'bank_account', 'ifsc_code', 'registration_number', 'pan_number']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop Name'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Office Email'}),
            'shop_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Complete Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Name (Optional)'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Number (Optional)'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IFSC Code (Optional)'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Registration (Optional)'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN Number (Optional)'}),
        }


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    phone_number = forms.CharField(max_length=17, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+91 XXXXXXXXXX'
    }))
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'gender', 'date_of_birth', 'bio', 'address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddressForm(forms.ModelForm):
    """Form for adding/editing addresses"""
    class Meta:
        model = Address
        fields = ['address_type', 'street_address', 'apartment_or_house', 'city', 'state', 'postal_code', 'country', 'phone_number', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'apartment_or_house': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment/House No.'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserLoginForm(forms.Form):
    """Form for user login"""
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))

