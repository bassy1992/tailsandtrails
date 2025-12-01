from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import Payment, PaymentProvider, PaymentCallback
from .services import PaymentService
from .utils import generate_payment_reference, format_phone_number

User = get_user_model()

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.provider = PaymentProvider.objects.create(
            name='Test Provider',
            code='test_provider',
            configuration={'test': 'config'},
            is_active=True
        )
    
    def test_payment_creation(self):
        payment = Payment.objects.create(
            user=self.user,
            reference='TEST-001',
            amount=100.00,
            currency='KES',
            payment_method='mobile_money',
            provider=self.provider,
            phone_number='+254700000000'
        )
        
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, 100.00)
        self.assertEqual(payment.status, 'pending')
        self.assertTrue(payment.payment_id)
    
    def test_payment_str_representation(self):
        payment = Payment.objects.create(
            user=self.user,
            reference='TEST-001',
            amount=100.00,
            currency='KES',
            payment_method='mobile_money',
            provider=self.provider
        )
        
        expected = f"Payment TEST-001 - KES 100.0 (pending)"
        self.assertEqual(str(payment), expected)
    
    def test_payment_log(self):
        payment = Payment.objects.create(
            user=self.user,
            reference='TEST-001',
            amount=100.00,
            currency='KES',
            payment_method='mobile_money',
            provider=self.provider
        )
        
        payment.log('info', 'Test log message', {'test': 'data'})
        
        log = payment.logs.first()
        self.assertEqual(log.level, 'info')
        self.assertEqual(log.message, 'Test log message')
        self.assertEqual(log.data, {'test': 'data'})

class PaymentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.provider = PaymentProvider.objects.create(
            name='Test Provider',
            code='test_provider',
            configuration={'test': 'config'},
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_payment(self):
        url = reverse('payments:payment-create')
        data = {
            'amount': 100.00,
            'currency': 'KES',
            'payment_method': 'mobile_money',
            'provider': self.provider.id,
            'phone_number': '+254700000000',
            'description': 'Test payment'
        }
        
        with patch('payments.services.PaymentService.initiate_payment') as mock_initiate:
            mock_initiate.return_value = {
                'success': True,
                'external_reference': 'EXT-123'
            }
            
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
            payment = Payment.objects.get(user=self.user)
            self.assertEqual(payment.amount, 100.00)
            self.assertEqual(payment.status, 'processing')
    
    def test_list_payments(self):
        # Create test payment
        Payment.objects.create(
            user=self.user,
            reference='TEST-001',
            amount=100.00,
            currency='KES',
            payment_method='mobile_money',
            provider=self.provider
        )
        
        url = reverse('payments:payment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_payment_detail(self):
        payment = Payment.objects.create(
            user=self.user,
            reference='TEST-001',
            amount=100.00,
            currency='KES',
            payment_method='mobile_money',
            provider=self.provider
        )
        
        url = reverse('payments:payment-detail', kwargs={'reference': payment.reference})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reference'], payment.reference)

class PaymentServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.provider = PaymentProvider.objects.create(
            name='M-Pesa',
            code='mpesa',
            configuration={
                'consumer_key': 'test_key',
                'consumer_secret': 'test_secret',
                'business_short_code': '174379',
                'passkey': 'test_passkey',
                'token_url': 'https://test.com/token',
                'stk_push_url': 'https://test.com/stkpush'
            },
            is_active=True
        )
        self.payment = Payment.objects.create(
            user=self.user,
            reference='TEST-001',
            amount=100.00,
            currency='KES',
            payment_method='mobile_money',
            provider=self.provider,
            phone_number='+254700000000'
        )
        self.service = PaymentService()
    
    @patch('payments.services.requests.get')
    @patch('payments.services.requests.post')
    def test_initiate_mpesa_payment(self, mock_post, mock_get):
        # Mock token request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'access_token': 'test_token'}
        
        # Mock STK push request
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'ResponseCode': '0',
            'CheckoutRequestID': 'ws_CO_123456789'
        }
        
        result = self.service.initiate_payment(self.payment)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['external_reference'], 'ws_CO_123456789')
    
    def test_process_mpesa_callback_success(self):
        callback_data = {
            'Body': {
                'stkCallback': {
                    'ResultCode': 0,
                    'ResultDesc': 'The service request is processed successfully.',
                    'CallbackMetadata': {
                        'Item': [
                            {'Name': 'Amount', 'Value': 100},
                            {'Name': 'MpesaReceiptNumber', 'Value': 'NLJ7RT61SV'},
                            {'Name': 'PhoneNumber', 'Value': 254700000000}
                        ]
                    }
                }
            }
        }
        
        callback = PaymentCallback.objects.create(
            payment=self.payment,
            provider_reference='ws_CO_123456789',
            status='success',
            callback_data=callback_data
        )
        
        result = self.service.process_callback(self.payment, callback)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], 'successful')
        self.assertEqual(result['transaction_id'], 'NLJ7RT61SV')

class PaymentUtilsTest(TestCase):
    def test_generate_payment_reference(self):
        reference = generate_payment_reference()
        
        self.assertTrue(reference.startswith('PAY-'))
        self.assertEqual(len(reference), 25)  # PAY- + 14 digits + - + 6 chars
    
    def test_format_phone_number(self):
        # Test with leading zero
        result = format_phone_number('0700000000', '+254')
        self.assertEqual(result, '+254700000000')
        
        # Test with country code
        result = format_phone_number('+254700000000')
        self.assertEqual(result, '+254700000000')
        
        # Test without country code
        result = format_phone_number('254700000000')
        self.assertEqual(result, '+254700000000')