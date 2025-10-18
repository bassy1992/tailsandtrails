#!/usr/bin/env python3
"""
Debug booking email issues
"""
import requests
import json

def check_environment_variables():
    """Check if environment variables are set on Railway"""
    print("🌍 Checking Environment Variables on Railway")
    print("=" * 50)
    
    # Test if we can create a payment to see if env vars are working
    try:
        # Create a test payment
        payment_data = {
            'amount': 50,
            'currency': 'GHS',
            'payment_method': 'mobile_money',
            'provider': 'mtn',
            'phone_number': '0241234567',
            'email': 'commey120jo@outlook.com',
            'description': 'Email Debug Test',
            'booking_details': {
                'type': 'tour',
                'tour_name': 'Email Debug Tour',
                'duration': '1 Day',
                'customer_name': 'Debug Customer',
                'customer_email': 'commey120jo@outlook.com',
                'customer_phone': '0241234567',
                'travelers': {'adults': 1, 'children': 0, 'total': 1},
                'selected_date': '2024-10-25',
                'payment_provider': 'mtn'
            }
        }
        
        response = requests.post(
            "https://tailsandtrails-production.up.railway.app/api/payments/paystack/create/",
            json=payment_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Payment creation status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                payment_ref = result['payment']['reference']
                print(f"✅ Payment created: {payment_ref}")
                
                # Check payment status
                verify_response = requests.get(
                    f"https://tailsandtrails-production.up.railway.app/api/payments/paystack/verify/{payment_ref}/"
                )
                
                if verify_response.status_code == 200:
                    verify_result = verify_response.json()
                    payment_status = verify_result.get('payment', {}).get('status', 'unknown')
                    print(f"Payment status: {payment_status}")
                    
                    if payment_status == 'successful':
                        print("✅ Payment is successful - email should have been triggered!")
                        return payment_ref
                    else:
                        print(f"⚠️ Payment status '{payment_status}' - emails only sent for 'successful' payments")
                        return payment_ref
                
            else:
                print(f"❌ Payment failed: {result.get('error')}")
        else:
            print(f"❌ Payment request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return None

def check_recent_successful_payments():
    """Check recent successful payments to see if emails should have been sent"""
    print("\n💳 Checking Recent Successful Payments")
    print("=" * 50)
    
    try:
        # We can't directly access the database, but we can check via API
        print("Recent successful payments should have triggered emails.")
        print("Check Railway logs for:")
        print("  ✅ 'Booking confirmation email sent for payment...'")
        print("  ❌ 'Failed to send booking confirmation email...'")
        print("  ❌ 'EMAIL_HOST_PASSWORD not set'")
        print("  ❌ 'Authentication failed'")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_email_endpoint():
    """Test if there's a direct email testing endpoint"""
    print("\n📧 Testing Email System Endpoints")
    print("=" * 50)
    
    # Check if management command endpoint exists
    try:
        # This won't work via HTTP, but we can suggest the command
        print("To test emails directly on Railway:")
        print("1. SSH into Railway container")
        print("2. Run: python manage.py send_test_confirmation --email commey120jo@outlook.com")
        print("3. Check the output for email sending status")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def check_email_triggers():
    """Check what triggers booking emails"""
    print("\n🔧 Email Trigger Analysis")
    print("=" * 50)
    
    print("Booking emails are triggered when:")
    print("1. ✅ Payment status changes from non-successful to 'successful'")
    print("2. ✅ Payment has booking_details in metadata")
    print("3. ✅ BREVO_SMTP_PASSWORD environment variable is set")
    print("4. ✅ Email templates exist and are accessible")
    
    print("\nCommon issues:")
    print("❌ BREVO_SMTP_PASSWORD not set in Railway")
    print("❌ Payments stuck in 'processing' or 'cancelled' status")
    print("❌ Missing booking_details in payment metadata")
    print("❌ SMTP authentication failures")
    print("❌ Email templates not found")

def main():
    """Main debug function"""
    print("🚨 BOOKING EMAIL DEBUG")
    print("=" * 60)
    print("Diagnosing why booking confirmation emails are not sending")
    print("=" * 60)
    
    # Check environment and create test payment
    payment_ref = check_environment_variables()
    
    # Check recent payments
    check_recent_successful_payments()
    
    # Test email endpoints
    test_email_endpoint()
    
    # Check triggers
    check_email_triggers()
    
    print("\n" + "=" * 60)
    print("🎯 DEBUGGING STEPS")
    print("=" * 60)
    
    print("1. 🚂 Check Railway Environment Variables:")
    print("   - Go to Railway Dashboard → Your Project → Variables")
    print("   - Ensure BREVO_SMTP_PASSWORD is set")
    print("   - Value should be: [Your Brevo SMTP Password]")
    
    print("\n2. 📋 Check Railway Logs:")
    print("   - Go to Railway Dashboard → Deployments → Latest → Logs")
    print("   - Look for email-related messages")
    print("   - Search for 'email', 'SMTP', 'Brevo'")
    
    print("\n3. 🧪 Test Email System:")
    print("   - SSH into Railway: railway shell")
    print("   - Run: python manage.py send_test_confirmation --email commey120jo@outlook.com")
    print("   - Check output for errors")
    
    print("\n4. 💳 Check Payment Status:")
    print("   - Emails only sent for payments with status='successful'")
    print("   - Check if payments are getting stuck in other statuses")
    
    print("\n5. 📧 Check Email Delivery:")
    print("   - Check commey120jo@outlook.com inbox")
    print("   - Check spam/junk folder")
    print("   - Look for emails from: TrailsAndTrails <awuleynovember@8508955.brevosend.com>")
    
    if payment_ref:
        print(f"\n🔍 Test Payment Created: {payment_ref}")
        print("   Monitor this payment to see if email is sent when it becomes successful")

if __name__ == "__main__":
    main()