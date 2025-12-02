#!/usr/bin/env python
"""
Script to inspect payments in Railway database
Run this on Railway to see what booking details exist
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
import json

def inspect_payments():
    """Inspect recent payments and their metadata"""
    
    print("=" * 80)
    print("RAILWAY DATABASE - PAYMENT INSPECTION")
    print("=" * 80)
    
    # Get all payments
    total_payments = Payment.objects.count()
    print(f"\n📊 Total Payments: {total_payments}")
    
    # Get recent payments
    recent_payments = Payment.objects.all().order_by('-created_at')[:10]
    
    print(f"\n🔍 Inspecting {recent_payments.count()} most recent payments:\n")
    
    payments_with_booking_details = 0
    payments_without_booking_details = 0
    
    for i, payment in enumerate(recent_payments, 1):
        print(f"\n{i}. Payment #{payment.reference}")
        print(f"   Amount: {payment.currency} {payment.amount}")
        print(f"   Status: {payment.status}")
        print(f"   User: {payment.user.email if payment.user else 'Anonymous'}")
        print(f"   Created: {payment.created_at}")
        print(f"   Description: {payment.description}")
        
        # Check metadata
        if payment.metadata:
            print(f"   Metadata keys: {list(payment.metadata.keys())}")
            
            if 'booking_details' in payment.metadata:
                payments_with_booking_details += 1
                print(f"   ✅ HAS booking_details")
                
                # Show summary of booking details
                bd = payment.metadata['booking_details']
                if 'user_info' in bd:
                    print(f"      Customer: {bd['user_info'].get('name', 'N/A')}")
                if 'destination' in bd:
                    print(f"      Destination: {bd['destination'].get('name', 'N/A')}")
                if 'travelers' in bd:
                    t = bd['travelers']
                    print(f"      Travelers: {t.get('adults', 0)} adults, {t.get('children', 0)} children")
            else:
                payments_without_booking_details += 1
                print(f"   ❌ NO booking_details")
        else:
            payments_without_booking_details += 1
            print(f"   ❌ NO metadata at all")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Payments: {total_payments}")
    print(f"Payments WITH booking_details: {payments_with_booking_details}")
    print(f"Payments WITHOUT booking_details: {payments_without_booking_details}")
    print("\n💡 Note: New payments will automatically have booking_details stored.")
    print("=" * 80)

if __name__ == '__main__':
    inspect_payments()
