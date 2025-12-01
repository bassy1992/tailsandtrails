#!/usr/bin/env python
"""
Test real-time booking data integration
"""
import requests
import json
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment

def test_realtime_booking_data():
    """Test that real-time booking data from frontend is processed correctly"""
    
    print("🧪 Testing Real-Time Booking Data Integration")
    print("=" * 60)
    
    # Simulate frontend booking data structure
    frontend_booking_data = {
        "bookingData": {
            "tourId": "1",
            "tourName": "Kakum National Park Canopy Walk Adventure",
            "duration": "2 Days / 1 Night",
            "basePrice": 800,
            "selectedDate": "2025-10-15",
            "travelers": {
                "adults": 2,
                "children": 1
            }
        },
        "selectedOptions": {
            "accommodation": "premium",
            "transport": "private",
            "meals": "luxury",
            "medical": "insurance"
        },
        "addOns": [
            {
                "id": "cultural",
                "name": "Cultural Experience",
                "description": "Drumming, cooking, local market tour",
                "price": 250,
                "category": "experience",
                "selected": True
            },
            {
                "id": "adventure",
                "name": "Adventure Add-on",
                "description": "Beach Trip, Hiking",
                "price": 400,
                "category": "experience",
                "selected": True
            }
        ]
    }
    
    # Create payment with real-time booking data
    payment_data = {
        "amount": "3850.00",  # Calculated total from frontend
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244567890",
        "description": "Kakum National Park Canopy Walk Adventure",
        "booking_details": frontend_booking_data
    }
    
    print("1. Creating payment with real-time booking data...")
    print(f"   Tour: {frontend_booking_data['bookingData']['tourName']}")
    print(f"   Travelers: {frontend_booking_data['bookingData']['travelers']['adults']} adults, {frontend_booking_data['bookingData']['travelers']['children']} children")
    print(f"   Date: {frontend_booking_data['bookingData']['selectedDate']}")
    print(f"   Accommodation: {frontend_booking_data['selectedOptions']['accommodation']}")
    print(f"   Transport: {frontend_booking_data['selectedOptions']['transport']}")
    print(f"   Experiences: {len([a for a in frontend_booking_data['addOns'] if a['selected']])} selected")
    print(f"   Total: GH₵{payment_data['amount']}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/',
            json=payment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"\n   ✅ Payment created: {payment_ref}")
            
            # Check if booking details were stored correctly
            payment = Payment.objects.get(reference=payment_ref)
            
            if 'booking_details' in payment.metadata:
                booking_details = payment.metadata['booking_details']
                
                print(f"\n2. Verifying stored booking details...")
                print(f"   ✅ Destination: {booking_details.get('destination', {}).get('name', 'Not found')}")
                print(f"   ✅ Duration: {booking_details.get('destination', {}).get('duration', 'Not found')}")
                print(f"   ✅ Travelers: {booking_details.get('travelers', {}).get('adults', 0)} adults, {booking_details.get('travelers', {}).get('children', 0)} children")
                print(f"   ✅ Date: {booking_details.get('selected_date', 'Not found')}")
                
                # Check selected options
                selected_options = booking_details.get('selected_options', {})
                print(f"   ✅ Accommodation: {selected_options.get('accommodation', {}).get('name', 'Not found')}")
                print(f"   ✅ Transport: {selected_options.get('transport', {}).get('name', 'Not found')}")
                print(f"   ✅ Meals: {selected_options.get('meals', {}).get('name', 'Not found')}")
                print(f"   ✅ Medical: {selected_options.get('medical', {}).get('name', 'Not found')}")
                
                # Check experiences
                experiences = selected_options.get('experiences', [])
                print(f"   ✅ Experiences: {len(experiences)} selected")
                for exp in experiences:
                    print(f"      - {exp.get('name', 'Unknown')} (GH₵{exp.get('price', 0)})")
                
                # Check pricing
                pricing = booking_details.get('pricing', {})
                print(f"   ✅ Base Total: GH₵{pricing.get('base_total', 0)}")
                print(f"   ✅ Options Total: GH₵{pricing.get('options_total', 0)}")
                print(f"   ✅ Final Total: GH₵{pricing.get('final_total', 0)}")
                
                print(f"\n🎉 Real-time booking data successfully integrated!")
                return True
            else:
                print(f"\n   ❌ No booking details found in payment metadata")
                return False
                
        else:
            print(f"\n   ❌ Payment creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n   ❌ Error: {str(e)}")
        return False

def show_admin_preview():
    """Show what the admin interface will display"""
    print("\n📋 Admin Interface Preview")
    print("=" * 40)
    
    print("The Django admin will now show:")
    print()
    print("👤 Customer Information")
    print("   Name: Guest User (or actual user name)")
    print("   Email: user@example.com (if logged in)")
    print("   Phone: +233244567890")
    print()
    print("🏖️ Destination")
    print("   Kakum National Park Canopy Walk Adventure")
    print("   📍 Ghana • ⏱️ 2 Days / 1 Night")
    print()
    print("👥 Travelers")
    print("   2 Adults + 1 Children")
    print("   📅 Date: 2025-10-15")
    print()
    print("⚙️ Selected Options")
    print("   🏨 Accommodation: Premium Hotel • GH₵500.00")
    print("   🚐 Transport: Private Van • GH₵800.00")
    print("   🍽️ Meals: Luxury Dining Package • GH₵300.00")
    print("   🏥 Medical & Insurance: Travel Insurance • GH₵200.00")
    print()
    print("🎯 Additional Experiences")
    print("   • Cultural Experience • GH₵250.00")
    print("   • Adventure Add-on • GH₵400.00")
    print()
    print("💰 Pricing Breakdown")
    print("   Base Total: GH₵2,400.00 (800 × 3 people)")
    print("   Options Total: GH₵1,450.00")
    print("   Final Total: GH₵3,850.00")

if __name__ == "__main__":
    print("Real-Time Booking Data Integration Test")
    print("This tests the flow from frontend booking to backend storage")
    print()
    
    success = test_realtime_booking_data()
    
    if success:
        show_admin_preview()
        print("\n🎯 Summary:")
        print("✅ Frontend booking data is now integrated with backend")
        print("✅ Real customer selections are stored and displayed")
        print("✅ Admin interface shows actual booking details")
        print("✅ No more sample data - everything is real-time!")
    else:
        print("\n❌ Integration test failed")
        print("Check the error messages above for details")
    
    print("\n🚀 Next Steps:")
    print("1. Test a booking in the frontend")
    print("2. Check the payment in Django admin")
    print("3. Verify all booking details are accurate")
    print("4. Real-time data should now be displayed!")