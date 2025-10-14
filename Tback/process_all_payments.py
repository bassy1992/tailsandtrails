#!/usr/bin/env python
"""
Script to process all payments and ensure they have proper booking details and records.
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
    print("🔄 Processing all payments to ensure proper booking details...")
    print()
    
    # Step 1: Add booking details to payments that don't have them
    print("1. Adding booking details to payments...")
    try:
        execute_from_command_line(['manage.py', 'add_booking_details'])
        print("✅ Booking details added successfully!")
    except Exception as e:
        print(f"❌ Adding booking details failed: {e}")
        return
    
    print()
    
    # Step 2: Create booking records from payments
    print("2. Creating booking records from payments...")
    try:
        execute_from_command_line(['manage.py', 'create_bookings_from_payments'])
        print("✅ Booking records created successfully!")
    except Exception as e:
        print(f"❌ Creating booking records failed: {e}")
        return
    
    print()
    
    # Step 3: Show summary
    print("3. Checking results...")
    try:
        from payments.models import Payment
        from destinations.models import Booking
        
        total_payments = Payment.objects.count()
        payments_with_details = Payment.objects.filter(metadata__has_key='booking_details').count()
        payments_with_bookings = Payment.objects.filter(booking__isnull=False).count()
        total_bookings = Booking.objects.count()
        
        print(f"📊 Summary:")
        print(f"   Total payments: {total_payments}")
        print(f"   Payments with booking details: {payments_with_details}")
        print(f"   Payments linked to bookings: {payments_with_bookings}")
        print(f"   Total booking records: {total_bookings}")
        
    except Exception as e:
        print(f"❌ Summary failed: {e}")
        return
    
    print()
    print("🎉 All payments have been processed!")
    print()
    print("Now all payments should show proper booking types in the admin interface:")
    print("- 🏝️ DESTINATION for tour/destination bookings")
    print("- 🎫 TICKET for event/ticket purchases")
    print("- ❓ UNKNOWN only for truly unclear payments")

if __name__ == '__main__':
    main()