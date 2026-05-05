from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F, Avg
from django.core.paginator import Paginator
from .models import Product, Category, ProductReview, ContactMessage
from .forms import ProductReviewForm, ProductSearchForm, ContactForm


def home_view(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    new_products = Product.objects.filter(is_active=True, is_new=True)[:8]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
    }
    return render(request, 'products/home.html', context)


def products_list_view(request):
    """List all products with search and filter options"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(sku__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(discount_price__gte=min_price) | products.filter(price__gte=min_price)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass
    
    # Stock filter
    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(stock__gt=0)
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'newest')
    if sort_by == 'price_low':
        products = products.annotate(final_price=F('discount_price')).order_by('final_price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.order_by('-total_sold')
    elif sort_by == 'rating':
        products = products.order_by('-average_rating')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'in_stock': in_stock or '',
        'sort_by': sort_by,
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """Display product details"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': ProductReviewForm() if request.user.is_authenticated else None,
    }
    return render(request, 'products/product_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_review_view(request, product_id):
    """Add a product review"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Check if user already reviewed this product
    existing_review = product.reviews.filter(user=request.user).first()
    
    form = ProductReviewForm(request.POST, instance=existing_review)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        
        # Update product average rating
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        product.average_rating = round(avg_rating, 2) if avg_rating else 0
        product.review_count = product.reviews.count()
        product.save()
        
        messages.success(request, 'Review added successfully!')
    else:
        messages.error(request, 'Error adding review. Please try again.')
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': product.reviews.all().order_by('-created_at'),
        'review_form': ProductReviewForm(),
    })


def category_view(request, slug):
    """View products in a specific category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Apply same filters as product list view
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'products/category.html', context)


def about_view(request):
    """About us page"""
    context = {
        'page_title': 'About Us',
    }
    return render(request, 'products/about.html', context)


@require_http_methods(["GET", "POST"])
def contact_view(request):
    """Contact us page with contact form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us',
    }
    return render(request, 'products/contact.html', context)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'products/category.html', context)
