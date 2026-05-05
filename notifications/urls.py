from django.urls import path
from . import views

urlpatterns = [
    path('send/<int:order_id>/', views.send_notification_view, name='send-notification'),
]
