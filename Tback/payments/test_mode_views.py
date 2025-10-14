from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Payment

@api_view(['POST'])
@permission_classes([AllowAny])
def simulate_test_payment_success(request, reference):
    """Simulate payment success in test mode - for development only"""
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        # Only allow this in test mode (when using test keys)
        from django.conf import settings
        public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
        
        if not public_key.startswith('pk_test_'):
            return Response({
                'success': False,
                'error': 'This endpoint only works with test API keys'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Update payment to successful
        if payment.status in ['processing', 'failed', 'cancelled']:
            old_status = payment.status
            payment.status = 'successful'
            payment.processed_at = timezone.now()
            payment.save()
            payment.log('info', f'Payment manually completed via API: {old_status} -> successful')
            
            # If this is a mobile money payment, sync it to Paystack dashboard
            if payment.payment_method == 'mobile_money':
                from .paystack_service import PaystackService
                
                try:
                    paystack_service = PaystackService()
                    sync_data = {
                        'reference': payment.reference,
                        'amount': float(payment.amount),
                        'email': request.data.get('email', 'test@example.com'),
                        'provider': 'mtn',  # Default provider
                        'phone_number': payment.phone_number or '233244123456',
                        'description': payment.description or 'Mobile Money Payment'
                    }
                    
                    sync_result = paystack_service.sync_successful_payment_to_paystack(sync_data)
                    
                    if sync_result['success']:
                        payment.log('info', 'Payment synced to Paystack dashboard for visibility')
                    else:
                        payment.log('warning', f'Failed to sync to Paystack dashboard: {sync_result.get("error")}')
                        
                except Exception as sync_error:
                    payment.log('warning', f'Paystack sync error: {str(sync_error)}')
            
            return Response({
                'success': True,
                'message': 'Payment marked as successful (test mode)',
                'payment': {
                    'reference': payment.reference,
                    'status': payment.status,
                    'amount': payment.amount,
                    'processed_at': payment.processed_at
                },
                'synced_to_paystack': payment.payment_method == 'mobile_money'
            })
        else:
            return Response({
                'success': False,
                'error': f'Payment is already {payment.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)