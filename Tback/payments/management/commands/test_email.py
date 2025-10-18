"""
Management command to test email configuration
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from payments.email_service import EmailService

class Command(BaseCommand):
    help = 'Test email configuration with Brevo SMTP'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to',
            default='test@example.com'
        )

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write(self.style.SUCCESS('🧪 Testing Email Configuration'))
        self.stdout.write('=' * 50)
        
        # Display current email settings
        self.stdout.write(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"📧 SMTP Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"📧 SMTP Port: {settings.EMAIL_PORT}")
        self.stdout.write(f"📧 Use TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"📧 From Email: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"📧 Host User: {settings.EMAIL_HOST_USER}")
        
        # Check if password is set
        if hasattr(settings, 'EMAIL_HOST_PASSWORD') and settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(f"📧 Password: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")
        else:
            self.stdout.write(self.style.ERROR("❌ EMAIL_HOST_PASSWORD not set!"))
            self.stdout.write("   Add BREVO_SMTP_PASSWORD to your environment variables")
            return
        
        self.stdout.write(f"\n📤 Sending test email to: {test_email}")
        
        try:
            # Send simple test email
            success = send_mail(
                subject='🧪 Test Email - Tails & Trails SMTP Configuration',
                message='This is a test email to verify your Brevo SMTP configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                html_message='''
                <html>
                <body>
                    <h2>🎉 SMTP Configuration Test Successful!</h2>
                    <p>This is a test email to verify your Brevo SMTP configuration.</p>
                    <p><strong>Configuration Details:</strong></p>
                    <ul>
                        <li>SMTP Server: smtp-relay.brevo.com</li>
                        <li>Port: 587</li>
                        <li>TLS: Enabled</li>
                        <li>From: Tails & Trails</li>
                    </ul>
                    <p>Your email system is ready to send booking and ticket confirmations!</p>
                    <hr>
                    <p><small>Sent from Tails & Trails Email System</small></p>
                </body>
                </html>
                ''',
                fail_silently=False,
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS("✅ Test email sent successfully!"))
                self.stdout.write("   Check your inbox (and spam folder)")
                
                # Test the EmailService class
                self.stdout.write("\n🔧 Testing EmailService class...")
                service_test = EmailService.test_email_configuration()
                if service_test:
                    self.stdout.write(self.style.SUCCESS("✅ EmailService test passed!"))
                else:
                    self.stdout.write(self.style.ERROR("❌ EmailService test failed"))
                
            else:
                self.stdout.write(self.style.ERROR("❌ Failed to send test email"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Email test failed: {str(e)}"))
            
            # Common error solutions
            self.stdout.write("\n🔧 Troubleshooting:")
            self.stdout.write("1. Check your BREVO_SMTP_PASSWORD environment variable")
            self.stdout.write("2. Verify your Brevo account is active")
            self.stdout.write("3. Check if your server can connect to smtp-relay.brevo.com:587")
            self.stdout.write("4. Ensure TLS is supported on your server")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("📋 Next Steps:")
        self.stdout.write("1. If test passed, emails will be sent automatically on bookings/tickets")
        self.stdout.write("2. Monitor the logs for email sending status")
        self.stdout.write("3. Test with real bookings to verify end-to-end flow")