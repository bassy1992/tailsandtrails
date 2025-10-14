#!/usr/bin/env python
"""
Test booking details storage directly
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment, PaymentProvider
from payments.booking_details_utils import add_booking_details_to_payment

def test_direct_storage():
    """Test booking details storage directly"""
    print("🧪 Testing Direct Booking Details Storage")
    print("=" * 50)
    
    # Create a test payment
    provider, _ = PaymentProvider.objects.get_or_create(
        code='paystack',
        defaults={'name': 'Paystack Ghana', 'is_active': True}
    )
    
    payment = Payment.objects.create(
        reference='TEST-DIRECT-001',
        amount=100.0,
        currency='GHS',
        payment_method='mobile_money',
        provider=provider,
        phone_number='0240381084',
        description='Direct test payment'
    )
    
    print(f"✅ Created test payment: {payment.reference}")
    
    # Test booking details
    booking_details = {
        'type': 'destination',
        'destination': {
            'name': 'Direct Test Tour',
            'price': 100.0
        },
        'travelers': {
            'adults': 1
        }
    }
    
    print("📋 Adding booking details...")
    
    try:
        add_booking_details_to_payment(payment, booking_details)
        print("✅ Booking details added successfully")
        
        # Refresh from database
        payment.refresh_from_db()
        
        if payment.metadata and 'booking_details' in payment.metadata:
            stored_details = payment.metadata['booking_details']
            print("✅ Booking details found in database")
            print(f"   Destination: {stored_details.get('destination', {}).get('name', 'N/A')}")
            print(f"   Type: {stored_details.get('type', 'N/A')}")
            return True
        else:
            print("❌ Booking details not found in database")
            print(f"   Metadata: {payment.metadata}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding booking details: {e}")
        return False
    finally:
        # Clean up
        payment.delete()
        print("🧹 Cleaned up test payment")

def main():
    """Main test"""
    print("🧪 Direct Booking Details Storage Test")
    print("=" * 60)
    
    success = test_direct_storage()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Direct storage works!")
        print("   The issue might be in the API request handling")
    else:
        print("❌ Direct storage failed")
        print("   Check the booking_details_utils function")

if __name__ == '__main__':
    main()