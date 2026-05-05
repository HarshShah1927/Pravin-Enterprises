from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('list/', views.order_list_view, name='order-list'),
    path('<int:order_id>/', views.order_detail_view, name='order-detail'),
    path('<int:order_id>/status/', views.update_order_status_view, name='update-order-status'),
]
