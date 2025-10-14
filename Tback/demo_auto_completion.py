#!/usr/bin/env python
"""
Demo script showing auto-completion functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment, PaymentProvider
from payments.views import auto_complete_payment_after_delay
import time

def create_demo_payment():
    """Create a demo payment for testing"""
    
    # Get or create MTN MoMo provider
    provider, created = PaymentProvider.objects.get_or_create(
        code='mtn_momo',
        defaults={
            'name': 'MTN Mobile Money',
            'is_active': True
        }
    )
    
    # Create a test payment
    payment = Payment.objects.create(
        reference=f"DEMO_{int(time.time())}",
        amount=25.00,
        currency='GHS',
        payment_method='momo',
        provider=provider,
        phone_number='+233244123456',
        description='Demo auto-completion test',
        status='processing'
    )
    
    payment.log('info', 'Demo payment created for auto-completion test')
    
    return payment

def demo_auto_completion():
    """Demonstrate auto-completion functionality"""
    
    print("🚀 Demo: Auto-Completion System")
    print("=" * 50)
    
    # Create demo payment
    print("1. Creating demo payment...")
    payment = create_demo_payment()
    print(f"   ✅ Payment created: {payment.reference}")
    print(f"   💰 Amount: {payment.currency} {payment.amount}")
    print(f"   📱 Phone: {payment.phone_number}")
    print(f"   📊 Status: {payment.status}")
    
    # Start auto-completion with short delay for demo
    print("\n2. Starting auto-completion (10 second delay)...")
    auto_complete_payment_after_delay(payment.reference, delay_seconds=10, success_rate=0.8)
    print("   ⏰ Auto-completion task started")
    print("   🎯 Success rate: 80%")
    
    # Monitor status
    print("\n3. Monitoring payment status...")
    for i in range(12):  # Monitor for 12 seconds
        time.sleep(1)
        payment.refresh_from_db()
        print(f"   [{i+1}s] Status: {payment.status}")
        
        if payment.status in ['successful', 'failed']:
            print(f"\n   🎉 Auto-completion completed!")
            print(f"   📊 Final Status: {payment.status}")
            if payment.processed_at:
                print(f"   ⏰ Processed At: {payment.processed_at}")
            break
    
    # Show logs
    print("\n4. Payment logs:")
    logs = payment.logs.all().order_by('created_at')
    for log in logs:
        print(f"   [{log.created_at.strftime('%H:%M:%S')}] {log.level.upper()}: {log.message}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    print("\nHow it works:")
    print("- When a payment is created, auto-completion starts automatically")
    print("- After 30 seconds (configurable), payment is auto-completed")
    print("- 90% success rate by default (configurable)")
    print("- Perfect for demo environments without real payment providers")

if __name__ == "__main__":
    demo_auto_completion()