#!/usr/bin/env python
"""
Sync successful Mobile Money payments to Paystack dashboard
This script will make MoMo payments visible in your Paystack dashboard
"""
import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from payments.paystack_service import PaystackService

def sync_momo_payments():
    """Sync successful MoMo payments to Paystack dashboard"""
    print("🔄 Syncing Mobile Money Payments to Paystack Dashboard")
    print("=" * 60)
    
    # Get successful MoMo payments from today
    today = datetime.now().date()
    momo_payments = Payment.objects.filter(
        payment_method='mobile_money',
        status='successful',
        created_at__date=today
    ).order_by('-created_at')
    
    if not momo_payments.exists():
        print("ℹ️  No successful MoMo payments found for today")
        return
    
    print(f"📱 Found {momo_payments.count()} successful MoMo payments to sync")
    print()
    
    paystack_service = PaystackService()
    synced_count = 0
    failed_count = 0
    
    for payment in momo_payments:
        print(f"🔄 Syncing payment {payment.reference}...")
        print(f"   Amount: GHS {payment.amount}")
        print(f"   Created: {payment.created_at}")
        
        # Prepare sync data
        sync_data = {
            'reference': payment.reference,
            'amount': float(payment.amount),
            'email': 'customer@example.com',  # Default email for test
            'provider': 'mtn',
            'phone_number': payment.phone_number or '233244123456',
            'description': payment.description or f'Mobile Money Payment - {payment.reference}'
        }
        
        try:
            result = paystack_service.sync_successful_payment_to_paystack(sync_data)
            
            if result['success']:
                print(f"   ✅ Successfully synced to Paystack")
                payment.log('info', 'Payment synced to Paystack dashboard via sync script')
                synced_count += 1
            else:
                print(f"   ❌ Failed to sync: {result.get('error')}")
                failed_count += 1
                
        except Exception as e:
            print(f"   ❌ Sync error: {str(e)}")
            failed_count += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("📊 Sync Summary")
    print("=" * 60)
    print(f"✅ Successfully synced: {synced_count}")
    print(f"❌ Failed to sync: {failed_count}")
    print(f"📱 Total processed: {momo_payments.count()}")
    
    if synced_count > 0:
        print()
        print("🎉 Success! Your MoMo payments should now be visible in:")
        print("   👉 Paystack Dashboard: https://dashboard.paystack.com/#/transactions")
        print("   👉 Look for transactions with your payment references")
        print()
        print("ℹ️  Note: These will show as 'Card' payments in Paystack")
        print("   but the metadata will indicate they were originally MoMo")

def sync_specific_payment(reference):
    """Sync a specific payment by reference"""
    print(f"🔄 Syncing specific payment: {reference}")
    
    try:
        payment = Payment.objects.get(reference=reference)
        
        if payment.payment_method != 'mobile_money':
            print(f"❌ Payment {reference} is not a mobile money payment")
            return
        
        if payment.status != 'successful':
            print(f"❌ Payment {reference} is not successful (status: {payment.status})")
            return
        
        paystack_service = PaystackService()
        
        sync_data = {
            'reference': payment.reference,
            'amount': float(payment.amount),
            'email': 'customer@example.com',
            'provider': 'mtn',
            'phone_number': payment.phone_number or '233244123456',
            'description': payment.description or f'Mobile Money Payment - {payment.reference}'
        }
        
        result = paystack_service.sync_successful_payment_to_paystack(sync_data)
        
        if result['success']:
            print(f"✅ Successfully synced payment {reference} to Paystack")
            payment.log('info', 'Payment synced to Paystack dashboard via manual sync')
        else:
            print(f"❌ Failed to sync payment {reference}: {result.get('error')}")
            
    except Payment.DoesNotExist:
        print(f"❌ Payment {reference} not found")
    except Exception as e:
        print(f"❌ Error syncing payment {reference}: {str(e)}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Sync specific payment
        reference = sys.argv[1]
        sync_specific_payment(reference)
    else:
        # Sync all today's payments
        sync_momo_payments()

if __name__ == '__main__':
    main()