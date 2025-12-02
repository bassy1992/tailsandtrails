#!/usr/bin/env python
"""
Script to backfill booking details for existing payments
This adds sample/placeholder booking details to payments that don't have them
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from payments.booking_utils import store_booking_details_in_payment, create_sample_booking_details
import json

def backfill_booking_details(dry_run=True):
    """
    Backfill booking details for payments that don't have them
    
    Args:
        dry_run: If True, only show what would be done without making changes
    """
    
    print("=" * 80)
    print("BACKFILL BOOKING DETAILS FOR EXISTING PAYMENTS")
    print("=" * 80)
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No changes will be made")
        print("Run with dry_run=False to actually update payments\n")
    else:
        print("\n🔥 LIVE MODE - Payments will be updated\n")
    
    # Find payments without booking_details
    all_payments = Payment.objects.all().order_by('-created_at')
    
    payments_to_update = []
    for payment in all_payments:
        if not payment.metadata or 'booking_details' not in payment.metadata:
            payments_to_update.append(payment)
    
    print(f"📊 Total Payments: {all_payments.count()}")
    print(f"📝 Payments needing booking_details: {len(payments_to_update)}")
    
    if not payments_to_update:
        print("\n✅ All payments already have booking_details!")
        return
    
    print(f"\n{'Would update' if dry_run else 'Updating'} {len(payments_to_update)} payments:\n")
    
    updated_count = 0
    for i, payment in enumerate(payments_to_update, 1):
        print(f"{i}. Payment {payment.reference}")
        print(f"   Amount: {payment.currency} {payment.amount}")
        print(f"   User: {payment.user.email if payment.user else 'Anonymous'}")
        print(f"   Description: {payment.description}")
        
        if not dry_run:
            # Create booking details based on payment info
            booking_data = create_sample_booking_details()
            
            # Customize with actual payment data
            booking_data['final_total'] = float(payment.amount)
            booking_data['base_total'] = float(payment.amount) * 0.7
            booking_data['options_total'] = float(payment.amount) * 0.3
            
            # Use actual user info if available
            if payment.user:
                user_name = f"{payment.user.first_name} {payment.user.last_name}".strip()
                if not user_name:
                    user_name = payment.user.username or payment.user.email.split('@')[0] if payment.user.email else "User"
                booking_data['user_name'] = user_name
                booking_data['user_email'] = payment.user.email or ''
                booking_data['user_phone'] = payment.phone_number or ''
            
            # Extract destination name from description if available
            if payment.description:
                if 'Booking for' in payment.description:
                    dest_name = payment.description.replace('Booking for', '').strip()
                    booking_data['destination_name'] = dest_name
                elif 'Ticket Purchase:' in payment.description:
                    # This is a ticket payment, skip it
                    print(f"   ⏭️  Skipping (ticket payment)")
                    continue
            
            # Store the booking details
            try:
                store_booking_details_in_payment(payment, booking_data)
                updated_count += 1
                print(f"   ✅ Updated with booking details")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        else:
            print(f"   📝 Would add booking details")
        
        print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    if dry_run:
        print(f"Would update {len(payments_to_update)} payments")
        print("\nTo actually update, run:")
        print("python backfill_booking_details.py --live")
    else:
        print(f"Successfully updated {updated_count} payments")
        print(f"Failed: {len(payments_to_update) - updated_count}")
    print("=" * 80)

if __name__ == '__main__':
    # Check for --live flag
    import sys
    dry_run = '--live' not in sys.argv
    
    backfill_booking_details(dry_run=dry_run)
