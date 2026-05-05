from django.urls import path
from . import api

urlpatterns = [
    path('', api.get_cart, name='api-get-cart'),
    path('add/', api.add_to_cart, name='api-add-to-cart'),
    path('update/<int:item_id>/', api.update_cart_item, name='api-update-item'),
    path('remove/<int:item_id>/', api.remove_from_cart, name='api-remove-item'),
    path('clear/', api.clear_cart, name='api-clear-cart'),
]
