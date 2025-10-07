from django.urls import path
from . import views

app_name = 'stripe_payments'

urlpatterns = [
    # Payment Intent operations
    path('payment-intents/create/', views.CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('payment-intents/', views.PaymentIntentListView.as_view(), name='payment-intent-list'),
    path('payment-intents/<str:stripe_payment_intent_id>/', views.PaymentIntentDetailView.as_view(), name='payment-intent-detail'),
    path('payment-intents/<str:payment_intent_id>/confirm/', views.confirm_payment_intent, name='confirm-payment-intent'),
    path('payment-intents/<str:payment_intent_id>/cancel/', views.cancel_payment_intent, name='cancel-payment-intent'),
    path('payment-intents/<str:payment_intent_id>/client-secret/', views.get_client_secret, name='get-client-secret'),
    
    # Payment Methods
    path('payment-methods/', views.PaymentMethodListView.as_view(), name='payment-method-list'),
    
    # Refunds
    path('payment-intents/<str:payment_intent_id>/refunds/', views.create_refund, name='create-refund'),
    
    # Webhooks
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]