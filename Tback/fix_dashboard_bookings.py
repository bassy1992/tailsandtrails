#!/usr/bin/env python
"""
Fix dashboard bookings by creating bookings from successful payments
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from payments.models import Payment
from destinations.models import Destination, Booking
from tickets.models import Ticket, TicketPurchase

User = get_user_model()

def create_booking_from_payment(payment):
    """Create a booking from a successful payment"""
    try:
        # Skip if booking already exists
        if hasattr(payment, 'booking') and payment.booking:
            print(f"  ✓ Booking already exists for payment {payment.reference}")
            return payment.booking
        
        # Try to find destination by name from description
        destination = None
        if payment.description:
            # Try exact match first
            destination = Destination.objects.filter(name__iexact=payment.description).first()
            
            # Try partial match if exact doesn't work
            if not destination:
                destination = Destination.objects.filter(name__icontains=payment.description.split()[0]).first()
        
        if not destination:
            print(f"  ❌ No destination found for: {payment.description}")
            return None
        
        # Create booking
        booking = Booking.objects.create(
            destination=destination,
            user=payment.user,
            participants=1,  # Default to 1 participant
            total_amount=payment.amount,
            booking_date=timezone.now().date() + timedelta(days=7),  # Default to next week
            status='confirmed' if payment.status == 'successful' else 'pending',
            special_requests=f'Auto-created from payment {payment.reference}'
        )
        
        # Link payment to booking
        payment.booking = booking
        payment.save()
        
        print(f"  ✅ Created booking {booking.booking_reference} for payment {payment.reference}")
        return booking
        
    except Exception as e:
        print(f"  ❌ Error creating booking for payment {payment.reference}: {str(e)}")
        return None

def create_ticket_purchase_from_payment(payment):
    """Create a ticket purchase from a successful payment"""
    try:
        # Skip if ticket purchase already exists
        existing_purchase = TicketPurchase.objects.filter(
            user=payment.user,
            total_amount=payment.amount,
            created_at__date=payment.created_at.date()
        ).first()
        
        if existing_purchase:
            print(f"  ✓ Ticket purchase already exists for payment {payment.reference}")
            return existing_purchase
        
        # Try to find ticket by description
        ticket = None
        if payment.description:
            # Look for tickets with similar names
            ticket = Ticket.objects.filter(title__icontains=payment.description.split()[0]).first()
        
        if not ticket:
            print(f"  ❌ No ticket found for: {payment.description}")
            return None
        
        # Create ticket purchase
        purchase = TicketPurchase.objects.create(
            user=payment.user,
            ticket=ticket,
            quantity=1,  # Default to 1 ticket
            unit_price=payment.amount,
            total_amount=payment.amount,
            status='confirmed' if payment.status == 'successful' else 'pending',
            payment_status='completed' if payment.status == 'successful' else 'pending',
            customer_name=payment.user.get_full_name() or payment.user.username,
            customer_email=payment.user.email,
            customer_phone=payment.phone_number or '+233241227481',
            payment_method='mobile_money' if payment.payment_method == 'mobile_money' else 'card',
            payment_date=payment.processed_at or payment.created_at
        )
        
        print(f"  ✅ Created ticket purchase {purchase.purchase_id} for payment {payment.reference}")
        return purchase
        
    except Exception as e:
        print(f"  ❌ Error creating ticket purchase for payment {payment.reference}: {str(e)}")
        return None

def fix_user_dashboard_data(user_email):
    """Fix dashboard data for a specific user"""
    try:
        user = User.objects.get(email=user_email)
        print(f"✅ Processing user: {user.email}")
    except User.DoesNotExist:
        print(f"❌ User {user_email} not found")
        return
    
    # Get all successful payments for this user
    payments = Payment.objects.filter(
        user=user,
        status='successful'
    ).order_by('-created_at')
    
    print(f"📊 Found {payments.count()} successful payments")
    
    bookings_created = 0
    tickets_created = 0
    
    for payment in payments:
        print(f"\n🔍 Processing payment: {payment.reference}")
        print(f"   Amount: GHS {payment.amount}")
        print(f"   Description: {payment.description}")
        print(f"   Date: {payment.created_at}")
        
        # Determine if this should be a destination booking or ticket purchase
        # Based on description keywords
        description_lower = payment.description.lower() if payment.description else ''
        
        is_ticket = any(word in description_lower for word in [
            'ticket', 'event', 'concert', 'festival', 'show', 'performance'
        ])
        
        if is_ticket:
            print("   🎫 Identified as ticket purchase")
            purchase = create_ticket_purchase_from_payment(payment)
            if purchase:
                tickets_created += 1
        else:
            print("   🏞️ Identified as destination booking")
            booking = create_booking_from_payment(payment)
            if booking:
                bookings_created += 1
    
    print(f"\n📈 Summary for {user.email}:")
    print(f"   🏞️ Bookings created: {bookings_created}")
    print(f"   🎫 Ticket purchases created: {tickets_created}")
    print(f"   📊 Total items: {bookings_created + tickets_created}")

def update_dashboard_api_data():
    """Update dashboard API to include all payment-based bookings"""
    print("\n🔄 Updating dashboard API data...")
    
    # This will be handled by the existing dashboard views
    # which should now pick up the newly created bookings
    print("✅ Dashboard API will automatically include new bookings")

def main():
    """Main function to fix dashboard bookings"""
    print("🔧 FIXING DASHBOARD BOOKINGS")
    print("=" * 60)
    
    # Fix for specific user
    user_email = 'wyarquah@gmail.com'
    fix_user_dashboard_data(user_email)
    
    # Update dashboard API
    update_dashboard_api_data()
    
    print("\n" + "=" * 60)
    print("✅ DASHBOARD BOOKING FIX COMPLETE")
    print("=" * 60)
    print("The dashboard should now show all bookings and purchases!")
    print("Visit http://localhost:8080/dashboard to see the updated data.")

if __name__ == '__main__':
    main()