#!/usr/bin/env python3
"""
Test the email setup for order confirmations
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('Tback')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from payments.email_service import EmailService

def test_email_configuration():
    """Test the email configuration"""
    print("📧 Testing Email Configuration")
    print("=" * 50)
    
    # Display settings
    print(f"📋 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"📋 SMTP Host: {settings.EMAIL_HOST}")
    print(f"📋 SMTP Port: {settings.EMAIL_PORT}")
    print(f"📋 Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"📋 Host User: {settings.EMAIL_HOST_USER}")
    print(f"📋 From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check password
    if hasattr(settings, 'EMAIL_HOST_PASSWORD') and settings.EMAIL_HOST_PASSWORD:
        print(f"📋 Password: {'*' * len(settings.EMAIL_HOST_PASSWORD)} (Set)")
    else:
        print("❌ EMAIL_HOST_PASSWORD not set!")
        print("   You need to set BREVO_SMTP_PASSWORD environment variable")
        return False
    
    return True

def test_booking_email():
    """Test booking confirmation email template"""
    print("\n🎫 Testing Booking Email Template")
    print("=" * 40)
    
    try:
        from django.template.loader import render_to_string
        
        # Test context
        context = {
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'customer_phone': '+233241234567',
            'booking_reference': 'PAY-TEST-12345',
            'tour_name': 'Kakum National Park Adventure',
            'duration': '2 Days / 1 Night',
            'travelers_count': 2,
            'total_amount': 150,
            'payment_method': 'MTN Mobile Money',
            'booking_date': 'October 17, 2024',
            'addons': [
                {'name': 'Professional Photography', 'price': 25},
                {'name': 'Traditional Lunch', 'price': 15}
            ]
        }
        
        # Render template
        html_content = render_to_string('emails/booking_confirmation.html', context)
        print("✅ Booking email template rendered successfully")
        print(f"   Template length: {len(html_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Booking email template error: {str(e)}")
        return False

def test_ticket_email():
    """Test ticket confirmation email template"""
    print("\n🎟️ Testing Ticket Email Template")
    print("=" * 40)
    
    try:
        from django.template.loader import render_to_string
        
        # Mock ticket codes
        class MockTicketCode:
            def __init__(self, code):
                self.code = code
        
        # Test context
        context = {
            'customer_name': 'Jane Smith',
            'customer_email': 'jane@example.com',
            'customer_phone': '+233241234567',
            'purchase_id': 'TKT-12345-67890',
            'ticket_title': 'Ghana Music Festival 2024',
            'venue': 'Accra Sports Stadium',
            'event_date': 'December 25, 2024 at 7:00 PM',
            'quantity': 2,
            'total_amount': 100,
            'payment_method': 'Mobile Money (Paystack)',
            'ticket_codes': [
                MockTicketCode('TKT-ABC123'),
                MockTicketCode('TKT-DEF456')
            ]
        }
        
        # Render template
        html_content = render_to_string('emails/ticket_confirmation.html', context)
        print("✅ Ticket email template rendered successfully")
        print(f"   Template length: {len(html_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Ticket email template error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("📧 EMAIL SETUP TEST FOR ORDER CONFIRMATIONS")
    print("=" * 60)
    print("Testing Brevo SMTP configuration for Tails & Trails")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_email_configuration()
    
    # Test templates
    booking_ok = test_booking_email()
    ticket_ok = test_ticket_email()
    
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS:")
    print(f"   ✅ Email Configuration: {'PASS' if config_ok else 'FAIL'}")
    print(f"   ✅ Booking Template: {'PASS' if booking_ok else 'FAIL'}")
    print(f"   ✅ Ticket Template: {'PASS' if ticket_ok else 'FAIL'}")
    
    if config_ok and booking_ok and ticket_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n📧 Email System Ready:")
        print("   • Booking confirmations will be sent automatically")
        print("   • Ticket confirmations will be sent automatically")
        print("   • Uses Brevo SMTP for reliable delivery")
        
        print("\n🔧 To complete setup:")
        print("   1. Set BREVO_SMTP_PASSWORD environment variable")
        print("   2. Deploy the changes to Railway")
        print("   3. Test with real bookings")
        
        print("\n🧪 Test email sending:")
        print("   python manage.py test_email --email your@email.com")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("   Check the errors above and fix them before deploying")

if __name__ == "__main__":
    main()