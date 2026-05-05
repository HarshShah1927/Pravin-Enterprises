from django.urls import path
from . import api

urlpatterns = [
    path('', api.list_products, name='api-list-products'),
]