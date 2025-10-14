#!/usr/bin/env python
"""
Script to set up phone numbers for users and payments.
Run this script from the Tback directory.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def main():
    print("📞 Setting up phone numbers for users and payments...")
    print()
    
    # Step 1: Add phone numbers to users who don't have them
    print("1. Adding phone numbers to users...")
    try:
        execute_from_command_line(['manage.py', 'add_phone_numbers', '--phone', '+233241234567'])
        print("✅ Phone numbers added to users!")
    except Exception as e:
        print(f"❌ Adding phone numbers failed: {e}")
        return
    
    print()
    
    # Step 2: Sync phone numbers from users to payments
    print("2. Syncing phone numbers to payments...")
    try:
        execute_from_command_line(['manage.py', 'sync_payment_phone_numbers'])
        print("✅ Phone numbers synced to payments!")
    except Exception as e:
        print(f"❌ Syncing phone numbers failed: {e}")
        return
    
    print()
    
    # Step 3: Update booking details with phone numbers
    print("3. Updating booking details...")
    try:
        execute_from_command_line(['manage.py', 'add_booking_details'])
        print("✅ Booking details updated with phone numbers!")
    except Exception as e:
        print(f"❌ Updating booking details failed: {e}")
        return
    
    print()
    
    # Step 4: Show summary
    print("4. Checking results...")
    try:
        from payments.models import Payment
        from authentication.models import User
        
        users_with_phone = User.objects.exclude(phone_number__in=['', None]).count()
        payments_with_phone = Payment.objects.exclude(phone_number__in=['', None]).count()
        total_users = User.objects.count()
        total_payments = Payment.objects.count()
        
        print(f"📊 Summary:")
        print(f"   Users with phone numbers: {users_with_phone}/{total_users}")
        print(f"   Payments with phone numbers: {payments_with_phone}/{total_payments}")
        
        # Check a sample payment
        if Payment.objects.exists():
            sample_payment = Payment.objects.first()
            print(f"   Sample payment {sample_payment.reference}:")
            print(f"     User phone: {sample_payment.user.phone_number if sample_payment.user else 'No user'}")
            print(f"     Payment phone: {sample_payment.phone_number}")
            booking_phone = sample_payment.metadata.get('booking_details', {}).get('user_info', {}).get('phone', 'Not set')
            print(f"     Booking details phone: {booking_phone}")
        
    except Exception as e:
        print(f"❌ Summary failed: {e}")
        return
    
    print()
    print("🎉 Phone numbers have been set up successfully!")
    print()
    print("Now the admin interface will show phone numbers in:")
    print("- The 'Phone number' column")
    print("- The detailed booking information")
    print("- User contact details")

if __name__ == '__main__':
    main()