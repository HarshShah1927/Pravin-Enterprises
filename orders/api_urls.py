from django.urls import path
from . import api

urlpatterns = [
    path('checkout/', api.checkout, name='api-checkout'),
    path('<int:order_id>/', api.get_order, name='api-get-order'),
    path('list/', api.list_orders, name='api-list-orders'),
]
