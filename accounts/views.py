from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from datetime import timedelta
import secrets
from .forms import UserRegistrationForm, UserProfileForm, AddressForm, UserLoginForm, ShopProfileForm
from .models import UserProfile, Address, EmailVerificationToken, ShopProfile


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        if settings.DEBUG:
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=email, is_active=True).order_by('id').first()
            if user and user.has_usable_password():
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                self.request.session['debug_password_reset_link'] = self.request.build_absolute_uri(reset_url)
        return response


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if settings.DEBUG:
            context['debug_password_reset_link'] = self.request.session.get('debug_password_reset_link')
        return context


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view with shop profile creation"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number']
            )
            
            # Create shop profile with business details
            ShopProfile.objects.create(
                user=user,
                shop_name=form.cleaned_data['shop_name'],
                gst_number=form.cleaned_data['gst_number'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                shop_address=form.cleaned_data['shop_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                country='India'
            )
            
            # Create cart for user
            from cart.models import Cart
            Cart.objects.create(user=user)
            
            messages.success(request, f'Account created successfully! Login with your email.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                messages.success(request, f'Welcome {user.first_name or user.username}!')
                return redirect(request.GET.get('next', 'home'))
            messages.error(request, 'Invalid email or password.')
                
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """User profile view"""
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'phone_number': ''}
    )
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def addresses_view(request):
    """View all user addresses"""
    addresses = request.user.addresses.all()
    context = {'addresses': addresses}
    return render(request, 'accounts/addresses.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def add_address_view(request):
    """Add a new address"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('addresses')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/add_address.html', {'form': form})


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_address_view(request, pk):
    """Edit an address"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('addresses')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/edit_address.html', {'form': form, 'address': address})


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_address_view(request, pk):
    """Delete an address"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('addresses')


@login_required(login_url='login')
@require_http_methods(["GET"])
def dashboard_view(request):
    """User dashboard"""
    recent_orders = request.user.orders.all()[:5]
    total_orders = request.user.orders.count()
    total_spent = sum(order.total_amount for order in request.user.orders.all())
    
    context = {
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'accounts/dashboard.html', context)
