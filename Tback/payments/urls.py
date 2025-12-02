from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment providers
    path('providers/', views.PaymentProviderListView.as_view(), name='provider-list'),
    
    # Payment operations
    path('create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('list/', views.PaymentListView.as_view(), name='payment-list'),
    path('<str:reference>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('<str:reference>/status/', views.payment_status, name='payment-status'),
    path('<str:reference>/complete/', views.complete_payment, name='payment-complete'),
    path('<str:reference>/cancel/', views.cancel_payment, name='payment-cancel'),
    
    # Callbacks
    path('callback/<str:provider_code>/', views.payment_callback, name='payment-callback'),
    
    # Checkout
    path('checkout/methods/', views.get_payment_methods, name='payment-methods'),
    path('checkout/create/', views.checkout_payment, name='checkout-payment'),
    
    # MTN MoMo webhook
    path('mtn-momo/webhook/', views.mtn_momo_webhook, name='mtn-momo-webhook'),
    
    # Paystack endpoints
    path('paystack/initialize/', views.paystack_initialize_payment, name='paystack-initialize'),
    path('paystack/verify/<str:reference>/', views.paystack_verify_payment, name='paystack-verify'),
    path('paystack/webhook/', views.paystack_webhook, name='paystack-webhook'),
    path('paystack/refund/<str:reference>/', views.paystack_refund_payment, name='paystack-refund'),
    
    # Demo endpoints
    path('<str:reference>/simulate-auth/', views.simulate_payment_authorization, name='simulate-payment-auth'),
    path('<str:reference>/start-auto-completion/', views.start_demo_auto_completion, name='start-auto-completion'),
    path('<str:reference>/force-complete/', views.force_complete_payment, name='force-complete-payment'),
    path('setup/create-paystack-provider/', views.create_paystack_provider_endpoint, name='create-paystack-provider'),
    
    # Booking details endpoints
    path('<str:reference>/add-booking-details/', views.add_booking_details_to_payment, name='add-booking-details'),
    path('ensure-booking-details/', views.ensure_all_booking_details, name='ensure-all-booking-details'),
    
    # Debug endpoint
    path('debug/', views.debug_payments, name='debug-payments'),
]