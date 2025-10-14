#!/usr/bin/env python
"""
Test the admin booking details display
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from payments.admin import PaymentAdmin

def test_admin_display():
    """Test the admin booking details display function"""
    
    print("🧪 Testing Admin Booking Details Display")
    print("=" * 50)
    
    # Get the specific payment
    try:
        payment = Payment.objects.get(reference='PAY-20250821000835-Y1ZZ9D')
        print(f"✅ Found payment: {payment.reference}")
        print(f"   Amount: {payment.currency} {payment.amount}")
        print(f"   Description: {payment.description}")
        print(f"   Phone: {payment.phone_number}")
        print()
        
        # Test the admin display function
        admin = PaymentAdmin(Payment, None)
        
        print("🔍 Testing booking_details_display function...")
        display_html = admin.booking_details_display(payment)
        
        # Check if it contains expected content
        if "No booking details available" in display_html:
            print("❌ Admin display shows 'No booking details available'")
            print("   This means the metadata is not being read correctly")
        elif "Elmina Castle" in display_html:
            print("✅ Admin display shows correct destination!")
            print("   Booking details are working correctly")
        else:
            print("⚠️ Admin display shows some content but not the expected destination")
        
        print()
        print("📋 Raw metadata check:")
        print(f"   Has metadata: {bool(payment.metadata)}")
        print(f"   Has booking_details: {'booking_details' in payment.metadata if payment.metadata else False}")
        
        if payment.metadata and 'booking_details' in payment.metadata:
            booking_details = payment.metadata['booking_details']
            print(f"   Destination name: {booking_details.get('destination', {}).get('name', 'Not found')}")
            print(f"   User name: {booking_details.get('user_info', {}).get('name', 'Not found')}")
            print(f"   User phone: {booking_details.get('user_info', {}).get('phone', 'Not found')}")
        
        # Show a snippet of the HTML (first 200 chars)
        print()
        print("📄 HTML snippet (first 200 chars):")
        print(display_html[:200] + "..." if len(display_html) > 200 else display_html)
        
    except Payment.DoesNotExist:
        print("❌ Payment PAY-20250821000835-Y1ZZ9D not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_admin_display()