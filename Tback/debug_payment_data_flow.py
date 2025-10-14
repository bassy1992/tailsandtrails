#!/usr/bin/env python
"""
Debug script to check payment data flow and booking details structure
"""
import os
import sys
import django
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

def debug_payment_data():
    """Debug payment data structure for wyarquah@gmail.com"""
    user_email = 'wyarquah@gmail.com'
    
    try:
        user = User.objects.get(email=user_email)
        print(f"✅ User found: {user.email}")
    except User.DoesNotExist:
        print(f"❌ User {user_email} not found")
        return
    
    # Get recent payments for this user
    payments = Payment.objects.filter(user=user).order_by('-created_at')[:5]
    
    print(f"\n📊 Found {payments.count()} recent payments:")
    print("=" * 80)
    
    for i, payment in enumerate(payments, 1):
        print(f"\n{i}. Payment: {payment.reference}")
        print(f"   Amount: GHS {payment.amount}")
        print(f"   Status: {payment.status}")
        print(f"   Description: {payment.description}")
        print(f"   Created: {payment.created_at}")
        
        # Check metadata structure
        if payment.metadata:
            print(f"\n   📋 Metadata Structure:")
            print(f"   Keys: {list(payment.metadata.keys())}")
            
            # Check booking_details
            if 'booking_details' in payment.metadata:
                booking_details = payment.metadata['booking_details']
                print(f"\n   🏞️ Booking Details Structure:")
                print(f"   Type: {type(booking_details)}")
                print(f"   Keys: {list(booking_details.keys()) if isinstance(booking_details, dict) else 'Not a dict'}")
                
                # Check nested structure
                if isinstance(booking_details, dict):
                    if 'bookingData' in booking_details:
                        booking_data = booking_details['bookingData']
                        print(f"\n   📊 Booking Data:")
                        print(f"   Keys: {list(booking_data.keys()) if isinstance(booking_data, dict) else 'Not a dict'}")
                        
                        if isinstance(booking_data, dict):
                            print(f"   Tour Name: {booking_data.get('tourName', 'Not found')}")
                            print(f"   Duration: {booking_data.get('duration', 'Not found')}")
                            print(f"   Selected Date: {booking_data.get('selectedDate', 'Not found')}")
                            print(f"   Travelers: {booking_data.get('travelers', 'Not found')}")
                            print(f"   Base Price: {booking_data.get('basePrice', 'Not found')}")
                    
                    if 'selectedOptions' in booking_details:
                        selected_options = booking_details['selectedOptions']
                        print(f"\n   ⚙️ Selected Options:")
                        print(f"   Keys: {list(selected_options.keys()) if isinstance(selected_options, dict) else 'Not a dict'}")
                        
                        if isinstance(selected_options, dict):
                            print(f"   Accommodation: {selected_options.get('accommodation', 'Not found')}")
                            print(f"   Transport: {selected_options.get('transport', 'Not found')}")
                            print(f"   Meals: {selected_options.get('meals', 'Not found')}")
                            print(f"   Medical: {selected_options.get('medical', 'Not found')}")
                    
                    if 'addOns' in booking_details:
                        add_ons = booking_details['addOns']
                        print(f"\n   🎁 Add-ons:")
                        print(f"   Type: {type(add_ons)}")
                        print(f"   Count: {len(add_ons) if isinstance(add_ons, list) else 'Not a list'}")
                
                # Show raw booking details (truncated)
                booking_details_str = json.dumps(booking_details, indent=2, default=str)
                if len(booking_details_str) > 1000:
                    booking_details_str = booking_details_str[:1000] + "... (truncated)"
                print(f"\n   📄 Raw Booking Details:")
                print(f"   {booking_details_str}")
            
            else:
                print(f"   ❌ No 'booking_details' key in metadata")
                print(f"   Available keys: {list(payment.metadata.keys())}")
        else:
            print(f"   ❌ No metadata found")
        
        print("-" * 80)

def check_payment_success_data_structure():
    """Check what data structure should be passed to PaymentSuccess"""
    print(f"\n🎯 Expected PaymentSuccess Data Structure:")
    print("=" * 80)
    
    expected_structure = {
        "tourName": "Tour name from booking",
        "total": "Payment amount",
        "paymentMethod": "mobile_money or card",
        "bookingDetails": {
            "bookingData": {
                "tourId": "Tour ID",
                "tourName": "Tour name",
                "duration": "Tour duration",
                "basePrice": "Base price per person",
                "selectedDate": "Selected travel date",
                "travelers": {
                    "adults": "Number of adults",
                    "children": "Number of children"
                }
            },
            "selectedOptions": {
                "accommodation": "standard/premium/luxury",
                "transport": "shared/private",
                "meals": "standard/premium",
                "medical": "basic/comprehensive"
            },
            "addOns": "Array of selected add-ons"
        },
        "customerInfo": {
            "name": "Customer name",
            "email": "Customer email",
            "phone": "Customer phone"
        },
        "paymentDetails": {
            "method": "Payment method",
            "provider": "Payment provider",
            "transactionId": "Transaction ID",
            "timestamp": "Payment timestamp"
        }
    }
    
    print(json.dumps(expected_structure, indent=2))

def suggest_fixes():
    """Suggest fixes for the booking details issue"""
    print(f"\n🔧 Suggested Fixes:")
    print("=" * 80)
    
    fixes = [
        "1. Check MomoCheckout.tsx - ensure booking details are passed correctly to PaymentSuccess",
        "2. Verify PaymentCallback.tsx - check if booking details are preserved during callback",
        "3. Check payment metadata structure - ensure booking_details key exists and has correct structure",
        "4. Add console.log in PaymentSuccess component to see actual received data",
        "5. Verify that booking data is being stored correctly in payment metadata during checkout",
        "6. Check if there's a mismatch between camelCase and snake_case in data structure",
        "7. Ensure that the booking details are not being lost during payment processing"
    ]
    
    for fix in fixes:
        print(f"   {fix}")
    
    print(f"\n📝 Debug Steps:")
    print("   1. Complete a new booking and check browser console for PaymentSuccess logs")
    print("   2. Check payment metadata in Django admin for the new payment")
    print("   3. Compare expected vs actual data structure")
    print("   4. Fix data flow if booking details are missing or malformed")

if __name__ == '__main__':
    print("🔍 Payment Data Flow Debug")
    print("=" * 80)
    
    debug_payment_data()
    check_payment_success_data_structure()
    suggest_fixes()
    
    print(f"\n✅ Debug complete!")
    print("Check the output above to identify where booking details are missing or malformed.")