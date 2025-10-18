"""
Management command to test booking confirmation emails
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from payments.email_service import EmailService

class Command(BaseCommand):
    help = 'Test booking confirmation email system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test to',
            default='commey120jo@outlook.com'
        )

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write(self.style.SUCCESS('📧 Testing Booking Email System'))
        self.stdout.write('=' * 60)
        
        # Check email configuration
        self.stdout.write('🔧 Email Configuration:')
        self.stdout.write(f"   HOST: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        self.stdout.write(f"   USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"   FROM: {settings.DEFAULT_FROM_EMAIL}")
        
        # Check password
        if hasattr(settings, 'EMAIL_HOST_PASSWORD') and settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(f"   PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD)} (SET)")
        else:
            self.stdout.write(self.style.ERROR("   PASSWORD: NOT SET!"))
            self.stdout.write("   Add BREVO_SMTP_PASSWORD environment variable")
            return
        
        # Test 1: Basic SMTP
        self.stdout.write('\n🧪 Test 1: Basic SMTP Connection')
        try:
            success = send_mail(
                subject='🧪 SMTP Test - Tails & Trails',
                message='Basic SMTP test from Railway.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS("✅ Basic SMTP test passed"))
            else:
                self.stdout.write(self.style.ERROR("❌ Basic SMTP test failed"))
                return
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ SMTP error: {str(e)}"))
            return
        
        # Test 2: Booking confirmation email
        self.stdout.write('\n🏞️ Test 2: Booking Confirmation Email')
        try:
            # Create mock payment
            class MockPayment:
                reference = 'TEST-BOOKING-12345'
                amount = 150
                payment_method = 'mtn_momo'
                user = None
            
            mock_payment = MockPayment()
            
            # Mock booking details
            booking_details = {
                'customer_name': 'Test Customer',
                'customer_email': test_email,
                'customer_phone': '+233241234567',
                'tour_name': 'Kakum National Park Adventure',
                'duration': '2 Days / 1 Night',
                'travelers': {'adults': 2, 'children': 0, 'total': 2},
                'selected_date': '2024-10-25',
                'selected_addons': [
                    {'name': 'Professional Photography', 'price': 25},
                    {'name': 'Traditional Lunch', 'price': 15}
                ]
            }
            
            # Send booking email
            success = EmailService.send_booking_confirmation(mock_payment, booking_details)
            
            if success:
                self.stdout.write(self.style.SUCCESS(f"✅ Booking email sent to {test_email}"))
            else:
                self.stdout.write(self.style.ERROR("❌ Booking email failed"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Booking email error: {str(e)}"))
        
        # Test 3: Check recent payments
        self.stdout.write('\n💳 Test 3: Recent Payment Status')
        try:
            from payments.models import Payment
            
            recent_payments = Payment.objects.filter(
                description__icontains='tour'
            ).order_by('-created_at')[:3]
            
            self.stdout.write(f"Found {recent_payments.count()} recent tour payments:")
            
            for payment in recent_payments:
                self.stdout.write(f"  • {payment.reference}: {payment.status}")
                if payment.status == 'successful':
                    self.stdout.write("    ✅ Should have triggered email")
                else:
                    self.stdout.write(f"    ❌ Status '{payment.status}' - no email sent")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Payment check error: {str(e)}"))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 Test Complete!')
        self.stdout.write(f"📧 Check {test_email} for test emails")
        
        self.stdout.write('\n📋 Key Points:')
        self.stdout.write('• Emails only sent when payment status = "successful"')
        self.stdout.write('• Check Railway logs for email sending messages')
        self.stdout.write('• Verify BREVO_SMTP_PASSWORD is set correctly')
        self.stdout.write('• Check spam folder for delivered emails')