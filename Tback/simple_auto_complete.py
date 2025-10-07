#!/usr/bin/env python
"""
Simple auto-completion script that can be run as a background process
"""
import os
import sys
import django
import time
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def auto_complete_single_payment(payment_reference, delay_seconds=30, success_rate=0.9):
    """Auto-complete a single payment after delay"""
    
    print(f"Starting auto-completion for {payment_reference} (delay: {delay_seconds}s)")
    
    # Wait for the delay
    time.sleep(delay_seconds)
    
    try:
        payment = Payment.objects.get(reference=payment_reference)
        
        if payment.status in ['pending', 'processing']:
            # Simulate success/failure
            if random.random() < success_rate:
                # Success
                payment.status = 'successful'
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', f'Auto-completed successfully after {delay_seconds}s delay')
                print(f"✅ Payment {payment_reference} completed successfully")
            else:
                # Failure
                payment.status = 'failed'
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', f'Auto-failed after {delay_seconds}s delay')
                print(f"❌ Payment {payment_reference} failed")
        else:
            print(f"⚠️ Payment {payment_reference} already processed ({payment.status})")
            
    except Payment.DoesNotExist:
        print(f"❌ Payment {payment_reference} not found")
    except Exception as e:
        print(f"❌ Error processing payment {payment_reference}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_auto_complete.py <payment_reference> [delay_seconds] [success_rate]")
        sys.exit(1)
    
    payment_ref = sys.argv[1]
    delay = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    success_rate = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
    
    auto_complete_single_payment(payment_ref, delay, success_rate)