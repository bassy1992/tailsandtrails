#!/usr/bin/env python
"""
Test script to verify booking details are stored in payment metadata
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from payments.booking_utils import store_booking_details_in_payment
import json

def test_booking_details_storage():
    """Test that booking details are properly stored in payment metadata"""
    
    print("=" * 80)
    print("TESTING BOOKING DETAILS STORAGE IN PAYMENT METADATA")
    print("=" * 80)
    
    # Get the most recent payment
    recent_payments = Payment.objects.all().order_by('-created_at')[:5]
    
    if not recent_payments:
        print("\n❌ No payments found in database")
        return
    
    print(f"\n✅ Found {recent_payments.count()} recent payments\n")
    
    for payment in recent_payments:
        print("-" * 80)
        print(f"Payment Reference: {payment.reference}")
        print(f"Amount: {payment.currency} {payment.amount}")
        print(f"Status: {payment.status}")
        print(f"User: {payment.user.email if payment.user else 'Anonymous'}")
        print(f"Created: {payment.created_at}")
        
        # Check if booking_details exists in metadata
        if payment.metadata and 'booking_details' in payment.metadata:
            print("\n✅ Booking details found in metadata:")
            booking_details = payment.metadata['booking_details']
            
            # Display user info
            if 'user_info' in booking_details:
                user_info = booking_details['user_info']
                print(f"\n👤 Customer Information:")
                print(f"   Name: {user_info.get('name', 'N/A')}")
                print(f"   Email: {user_info.get('email', 'N/A')}")
                print(f"   Phone: {user_info.get('phone', 'N/A')}")
            
            # Display destination info
            if 'destination' in booking_details:
                dest = booking_details['destination']
                print(f"\n🏖️ Destination:")
                print(f"   Name: {dest.get('name', 'N/A')}")
                print(f"   Location: {dest.get('location', 'N/A')}")
                print(f"   Duration: {dest.get('duration', 'N/A')}")
            
            # Display travelers
            if 'travelers' in booking_details:
                travelers = booking_details['travelers']
                print(f"\n👥 Travelers:")
                print(f"   Adults: {travelers.get('adults', 0)}")
                print(f"   Children: {travelers.get('children', 0)}")
            
            # Display selected date
            if 'selected_date' in booking_details:
                print(f"\n📅 Date: {booking_details['selected_date']}")
            
            # Display selected options
            if 'selected_options' in booking_details:
                options = booking_details['selected_options']
                print(f"\n⚙️ Selected Options:")
                
                if 'accommodation' in options:
                    acc = options['accommodation']
                    print(f"   Accommodation: {acc.get('name', 'N/A')} (GH₵{acc.get('price', 0)})")
                
                if 'transport' in options:
                    trans = options['transport']
                    print(f"   Transport: {trans.get('name', 'N/A')} (GH₵{trans.get('price', 0)})")
                
                if 'meals' in options:
                    meals = options['meals']
                    print(f"   Meals: {meals.get('name', 'N/A')} (GH₵{meals.get('price', 0)})")
                
                if 'medical' in options:
                    medical = options['medical']
                    print(f"   Medical: {medical.get('name', 'N/A')} (GH₵{medical.get('price', 0)})")
                
                if 'experiences' in options:
                    experiences = options['experiences']
                    if experiences:
                        print(f"   Experiences:")
                        for exp in experiences:
                            print(f"      - {exp.get('name', 'N/A')} (GH₵{exp.get('price', 0)})")
            
            # Display pricing
            if 'pricing' in booking_details:
                pricing = booking_details['pricing']
                print(f"\n💰 Pricing Breakdown:")
                print(f"   Base Total: GH₵{pricing.get('base_total', 0)}")
                print(f"   Options Total: GH₵{pricing.get('options_total', 0)}")
                print(f"   Final Total: GH₵{pricing.get('final_total', 0)}")
            
            # Show full JSON for debugging
            print(f"\n📋 Full Booking Details JSON:")
            print(json.dumps(booking_details, indent=2))
            
        else:
            print("\n❌ No booking details found in metadata")
            print(f"   Metadata: {payment.metadata}")
        
        print()
    
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    test_booking_details_storage()
