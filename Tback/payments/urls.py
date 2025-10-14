from django.urls import path
from . import views

urlpatterns = [
    path('payment/<str:reference>/', views.get_payment_details, name='payment-details'),
    path('checkout/methods/', views.get_payment_methods, name='payment-methods'),
]