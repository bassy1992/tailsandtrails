from django.urls import path
from . import views
from . import paystack_views

urlpatterns = [
    path('payment/<str:reference>/', views.get_payment_details, name='payment-details'),
    path('checkout/methods/', views.get_payment_methods, name='payment-methods'),
    
    # Paystack endpoints
    path('paystack/create/', paystack_views.create_paystack_payment, name='paystack-create'),
    path('paystack/verify/<str:reference>/', paystack_views.verify_paystack_payment, name='paystack-verify'),
    path('paystack/webhook/', paystack_views.paystack_webhook, name='paystack-webhook'),
    path('paystack/callback/', paystack_views.paystack_callback, name='paystack-callback'),
    path('paystack/config/', paystack_views.get_paystack_config, name='paystack-config'),
]