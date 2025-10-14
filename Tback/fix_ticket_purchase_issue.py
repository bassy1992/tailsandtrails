import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from tickets.models import TicketPurchase, TicketCode
from django.utils import timezone
import re

def fix_ticket_purchase_issue():
    """Fix the ticket purchase issue by connecting successful payments to pending purchases"""
    
    print("🔧 FIXING TICKET PURCHASE ISSUE")
    print("=" * 50)
    
    # Get successful ticket payments
    successful_ticket_payments = Payment.objects.filter(
        status='successful',
        description__icontains='Ticket Purchase:'
    ).order_by('-created_at')
    
    print(f"Found {successful_ticket_payments.count()} successful ticket payments")
    
    # Get pending ticket purchases
    pending_purchases = TicketPurchase.objects.filter(
        status='pending',
        payment_reference__isnull=True
    ).order_by('-created_at')
    
    print(f"Found {pending_purchases.count()} pending ticket purchases")
    
    fixed_count = 0
    
    for payment in successful_ticket_payments:
        print(f"\n🔍 Processing payment: {payment.reference}")
        print(f"   Amount: {payment.amount}")
        print(f"   Description: {payment.description}")
        
        # Extract ticket name from description
        match = re.search(r'Ticket Purchase: (.+?) \((\d+) tickets?\)', payment.description)
        if match:
            ticket_name = match.group(1)
            quantity = int(match.group(2))
            print(f"   Extracted: {ticket_name} x{quantity}")
            
            # Find matching pending purchase
            matching_purchase = pending_purchases.filter(
                ticket__title=ticket_name,
                quantity=quantity,
                payment_reference__isnull=True
            ).first()
            
            if matching_purchase:
                print(f"   ✅ Found matching purchase: {matching_purchase.purchase_id}")
                
                # Update the purchase
                matching_purchase.payment_reference = payment.reference
                matching_purchase.status = 'confirmed'
                matching_purchase.payment_status = 'completed'
                matching_purchase.payment_date = payment.processed_at or timezone.now()
                matching_purchase.total_amount = payment.amount  # Update to match payment amount
                matching_purchase.unit_price = payment.amount / matching_purchase.quantity
                matching_purchase.save()
                
                # Generate ticket codes if not already generated
                if not matching_purchase.ticket_codes.exists():
                    print(f"   🎫 Generating {matching_purchase.quantity} ticket codes...")
                    for i in range(matching_purchase.quantity):
                        TicketCode.objects.create(
                            purchase=matching_purchase,
                            status='active'
                        )
                
                print(f"   ✅ Fixed purchase: {matching_purchase.purchase_id}")
                fixed_count += 1
            else:
                print(f"   ❌ No matching pending purchase found")
        else:
            print(f"   ⚠️  Could not parse ticket info from description")
    
    print(f"\n" + "=" * 50)
    print(f"🎉 FIXED {fixed_count} TICKET PURCHASES!")
    print("=" * 50)
    
    # Show summary
    confirmed_purchases = TicketPurchase.objects.filter(status='confirmed').count()
    pending_purchases_remaining = TicketPurchase.objects.filter(status='pending').count()
    
    print(f"✅ Confirmed purchases: {confirmed_purchases}")
    print(f"⏳ Pending purchases remaining: {pending_purchases_remaining}")
    
    # Show recent confirmed purchases
    recent_confirmed = TicketPurchase.objects.filter(
        status='confirmed'
    ).order_by('-updated_at')[:5]
    
    print(f"\n🎫 Recent confirmed purchases:")
    for purchase in recent_confirmed:
        codes_count = purchase.ticket_codes.count()
        print(f"   • {purchase.ticket.title} - {purchase.quantity}x - GH₵{purchase.total_amount} - {codes_count} codes")
    
    print(f"\n🔍 Check admin panels:")
    print(f"   • Ticket Purchases: http://localhost:8000/admin/tickets/ticketpurchase/")
    print(f"   • Payments: http://localhost:8000/admin/payments/payment/")

if __name__ == "__main__":
    fix_ticket_purchase_issue()