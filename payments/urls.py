from django.urls import path
from . import views

urlpatterns = [
    path('invoice/<int:order_id>/download/', views.download_invoice_view, name='download-invoice'),
]
