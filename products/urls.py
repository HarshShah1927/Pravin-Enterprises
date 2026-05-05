from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.products_list_view, name='products'),
    path('product/<slug:slug>/', views.product_detail_view, name='product-detail'),
    path('category/<slug:slug>/', views.category_view, name='category-detail'),
    path('product/<int:product_id>/review/', views.add_review_view, name='add-review'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
