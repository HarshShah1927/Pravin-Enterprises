from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart_view, name='add-to-cart'),
    path('update/<int:item_id>/', views.update_cart_item_view, name='update-cart-item'),
    path('remove/<int:item_id>/', views.remove_from_cart_view, name='remove-from-cart'),
    path('clear/', views.clear_cart_view, name='clear-cart'),
    path('summary/', views.get_cart_summary, name='cart-summary'),
]
