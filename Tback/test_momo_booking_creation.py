#!/usr/bin/env python
"""
Test MoMo payment with booking details creation
"""
import requests
import json
import time

def test_momo_payment_with_booking():
    """Test MoMo payment that should create a booking in database"""
    print("🧪 Testing MoMo Payment with Booking Creation")
    print("=" * 60)
    
    # Create sample booking details
    booking_details = {
        'type': 'destination',
        'destination': {
            'id': 17,  # Use existing destination ID
            'name': 'Cape Coast Castle Tour',
            'location': 'Cape Coast, Ghana',
            'price': 350.0
        },
        'travelers': {
            'adults': 2,
            'children': 0
        },
        'selected_date': '2025-10-15',
        'user_info': {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '0240381084'
        },
        'selected_options': {
            'accommodation': {
                'name': 'Standard Hotel',
                'price': 100.0
            },
            'transport': {
                'name': 'Private Car',
                'price': 80.0
            }
        },
        'pricing': {
            'base_total': 350.0,
            'options_total': 180.0,
            'final_total': 530.0
        }
    }
    
    # Create MoMo payment with booking details
    momo_data = {
        'amount': 530.0,
        'email': 'john.doe@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0240381084',
        'description': 'Cape Coast Castle Tour Booking',
        'booking_details': booking_details
    }
    
    print("1️⃣ Creating MoMo Payment with Booking Details...")
    print(f"   💰 Amount: GHS {momo_data['amount']}")
    print(f"   📱 Phone: {momo_data['phone_number']}")
    print(f"   🏰 Tour: {booking_details['destination']['name']}")
    print(f"   👥 Travelers: {booking_details['travelers']['adults']} adults")
    print()
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=momo_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result.get('payment', {}).get('reference', '')
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            
            print("✅ Payment Created Successfully!")
            print(f"📋 Reference: {payment_ref}")
            print(f"🔗 Paystack URL: {auth_url}")
            print()
            
            # Check if booking details were stored
            print("2️⃣ Checking Payment Metadata...")
            payment_check = check_payment_details(payment_ref)
            
            if payment_check:
                print("3️⃣ Simulating Payment Success...")
                success = simulate_payment_success(payment_ref)
                
                if success:
                    print("4️⃣ Checking Booking Creation...")
                    time.sleep(2)  # Give signals time to process
                    booking_check = check_booking_creation(payment_ref)
                    
                    return True, payment_ref, booking_check
                else:
                    print("❌ Failed to simulate payment success")
                    return False, payment_ref, None
            else:
                print("❌ Booking details not stored properly")
                return False, payment_ref, None
        else:
            print(f"❌ Payment creation failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False, None, None
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False, None, None

def check_payment_details(payment_ref):
    """Check if payment has booking details stored"""
    try:
        response = requests.get(f'http://localhost:8000/api/payments/paystack/verify/{payment_ref}/')
        
        if response.status_code == 200:
            result = response.json()
            payment = result.get('payment', {})
            
            if 'booking_details' in payment.get('metadata', {}):
                booking_details = payment['metadata']['booking_details']
                print(f"   ✅ Booking details stored")
                print(f"   🏰 Destination: {booking_details.get('destination', {}).get('name', 'N/A')}")
                print(f"   👥 Travelers: {booking_details.get('travelers', {})}")
                print(f"   💰 Total: GHS {booking_details.get('pricing', {}).get('final_total', 'N/A')}")
                return True
            else:
                print("   ❌ No booking details found in payment metadata")
                return False
        else:
            print(f"   ❌ Failed to check payment: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking payment: {e}")
        return False

def simulate_payment_success(payment_ref):
    """Simulate payment success to trigger booking creation"""
    try:
        response = requests.post(
            f'http://localhost:8000/api/payments/{payment_ref}/complete/',
            json={'status': 'successful'},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Payment marked as successful")
            return True
        else:
            print(f"   ❌ Failed to complete payment: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error completing payment: {e}")
        return False

def check_booking_creation(payment_ref):
    """Check if booking was created in database"""
    try:
        # Check via Django shell command
        import subprocess
        
        shell_command = f'''
from payments.models import Payment
from destinations.models import Booking

try:
    payment = Payment.objects.get(reference="{payment_ref}")
    print(f"Payment Status: {{payment.status}}")
    
    if payment.booking:
        booking = payment.booking
        print(f"Booking Created: {{booking.booking_reference}}")
        print(f"Destination: {{booking.destination.name}}")
        print(f"Participants: {{booking.participants}}")
        print(f"Total Amount: GHS {{booking.total_amount}}")
        print(f"Status: {{booking.status}}")
        print("SUCCESS")
    else:
        print("No booking linked to payment")
        print("FAILED")
        
except Payment.DoesNotExist:
    print("Payment not found")
    print("FAILED")
except Exception as e:
    print(f"Error: {{e}}")
    print("FAILED")
'''
        
        result = subprocess.run(
            ['python', 'manage.py', 'shell', '-c', shell_command],
            capture_output=True,
            text=True,
            cwd='.'
        )
        
        output = result.stdout.strip()
        print(f"   Database Check Output:")
        for line in output.split('\n'):
            if line.strip():
                print(f"   {line}")
        
        if 'SUCCESS' in output:
            print("   ✅ Booking created successfully!")
            return True
        else:
            print("   ❌ Booking not created")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking booking: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 MoMo Payment + Booking Creation Test")
    print("=" * 70)
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    print()
    
    # Test the complete flow
    success, payment_ref, booking_created = test_momo_payment_with_booking()
    
    print("\n" + "=" * 70)
    print("📊 Test Results")
    print("=" * 70)
    
    if success:
        print(f"✅ Payment Created: {payment_ref}")
        if booking_created:
            print("✅ Booking Created: Successfully")
            print()
            print("🎉 Complete Success!")
            print("   - MoMo payment created with booking details")
            print("   - Payment marked as successful")
            print("   - Booking automatically created in database")
            print("   - Payment and booking are properly linked")
        else:
            print("❌ Booking Created: Failed")
            print()
            print("⚠️ Partial Success")
            print("   - Payment created but booking not created")
            print("   - Check the signals and booking creation logic")
    else:
        print("❌ Payment Created: Failed")
        print()
        print("❌ Test Failed")
        print("   - Check payment creation API")
        print("   - Verify booking details format")
    
    print(f"\n🔍 Manual Check:")
    if payment_ref:
        print(f"   Payment: http://localhost:8000/admin/payments/payment/?q={payment_ref}")
        print(f"   Bookings: http://localhost:8000/admin/destinations/booking/")

if __name__ == '__main__':
    main()