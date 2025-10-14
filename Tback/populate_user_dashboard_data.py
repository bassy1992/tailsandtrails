#!/usr/bin/env python
"""
Script to populate dashboard data for a specific user
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from destinations.models import (
    Category, Destination, DestinationImage, DestinationHighlight, 
    DestinationInclude, Booking, Review
)
from tickets.models import (
    TicketCategory, Venue, Ticket, TicketPurchase, TicketCode
)

User = get_user_model()

def get_or_create_user(email):
    """Get or create user with the specified email"""
    try:
        user = User.objects.get(email=email)
        print(f"✓ Found existing user: {user.email}")
        return user
    except User.DoesNotExist:
        print(f"❌ User {email} not found in database")
        print("Available users:")
        for u in User.objects.all():
            print(f"  - {u.email}")
        return None

def create_bookings_for_user(user):
    """Create sample bookings for the specified user"""
    print(f"Creating bookings for user: {user.email}")
    
    # Get available destinations
    destinations = list(Destination.objects.all()[:6])
    if not destinations:
        print("❌ No destinations found. Please run populate_dashboard_data.py first")
        return []
    
    bookings_data = [
        {
            'destination': destinations[0],  # Cape Coast Castle
            'participants': 2,
            'total_amount': destinations[0].price * 2,
            'booking_date': timezone.now().date() + timedelta(days=20),
            'status': 'confirmed',
            'created_at': timezone.now() - timedelta(days=3)
        },
        {
            'destination': destinations[1],  # Kakum Canopy Walk
            'participants': 1,
            'total_amount': destinations[1].price,
            'booking_date': timezone.now().date() + timedelta(days=35),
            'status': 'pending',
            'created_at': timezone.now() - timedelta(days=1)
        },
        {
            'destination': destinations[2],  # Mole Safari
            'participants': 3,
            'total_amount': destinations[2].price * 3,
            'booking_date': timezone.now().date() - timedelta(days=20),
            'status': 'completed',
            'created_at': timezone.now() - timedelta(days=35)
        },
        {
            'destination': destinations[3],  # Kumasi Cultural
            'participants': 2,
            'total_amount': destinations[3].price * 2,
            'booking_date': timezone.now().date() + timedelta(days=45),
            'status': 'confirmed',
            'created_at': timezone.now() - timedelta(days=2)
        },
        {
            'destination': destinations[4],  # Labadi Beach
            'participants': 4,
            'total_amount': destinations[4].price * 4,
            'booking_date': timezone.now().date() - timedelta(days=15),
            'status': 'completed',
            'created_at': timezone.now() - timedelta(days=30)
        }
    ]
    
    bookings = []
    for booking_data in bookings_data:
        # Check if booking already exists
        existing_booking = Booking.objects.filter(
            user=user,
            destination=booking_data['destination'],
            booking_date=booking_data['booking_date']
        ).first()
        
        if existing_booking:
            print(f"  ✓ Booking already exists: {existing_booking.booking_reference}")
            bookings.append(existing_booking)
        else:
            booking = Booking.objects.create(
                user=user,
                **booking_data
            )
            # Update created_at manually
            Booking.objects.filter(id=booking.id).update(
                created_at=booking_data['created_at'],
                updated_at=booking_data['created_at']
            )
            print(f"  ✓ Created booking: {booking.booking_reference} - {booking.destination.name}")
            bookings.append(booking)
    
    return bookings

def create_ticket_purchases_for_user(user):
    """Create sample ticket purchases for the specified user"""
    print(f"Creating ticket purchases for user: {user.email}")
    
    # Get available tickets
    tickets = list(Ticket.objects.all()[:4])
    if not tickets:
        print("❌ No tickets found. Please run populate_dashboard_data.py first")
        return []
    
    purchases_data = [
        {
            'ticket': tickets[0],  # Afrobeats Concert
            'quantity': 2,
            'unit_price': tickets[0].price,
            'total_amount': tickets[0].price * 2,
            'status': 'confirmed',
            'payment_status': 'completed',
            'created_at': timezone.now() - timedelta(days=5)
        },
        {
            'ticket': tickets[1],  # Independence Festival
            'quantity': 1,
            'unit_price': tickets[1].price,
            'total_amount': tickets[1].price,
            'status': 'confirmed',
            'payment_status': 'completed',
            'created_at': timezone.now() - timedelta(days=2)
        },
        {
            'ticket': tickets[2],  # Sports Event
            'quantity': 3,
            'unit_price': tickets[2].price,
            'total_amount': tickets[2].price * 3,
            'status': 'pending',
            'payment_status': 'pending',
            'created_at': timezone.now() - timedelta(days=1)
        }
    ]
    
    purchases = []
    for purchase_data in purchases_data:
        # Check if purchase already exists
        existing_purchase = TicketPurchase.objects.filter(
            user=user,
            ticket=purchase_data['ticket']
        ).first()
        
        if existing_purchase:
            print(f"  ✓ Purchase already exists: {existing_purchase.purchase_id}")
            purchases.append(existing_purchase)
        else:
            purchase = TicketPurchase.objects.create(
                user=user,
                **purchase_data,
                customer_name=f"{user.first_name} {user.last_name}" if user.first_name else user.username,
                customer_email=user.email,
                customer_phone=user.phone_number or '+233244123456',
                payment_method='paystack',
                payment_date=purchase_data['created_at'] if purchase_data['payment_status'] == 'completed' else None
            )
            
            # Update created_at manually
            TicketPurchase.objects.filter(id=purchase.id).update(
                created_at=purchase_data['created_at'],
                updated_at=purchase_data['created_at']
            )
            print(f"  ✓ Created ticket purchase: {purchase.purchase_id} - {purchase.ticket.title}")
            
            # Create ticket codes for confirmed purchases
            if purchase.status == 'confirmed':
                for i in range(purchase.quantity):
                    TicketCode.objects.create(
                        purchase=purchase,
                        status='active'
                    )
            
            purchases.append(purchase)
    
    return purchases

def create_reviews_for_user(user):
    """Create sample reviews for completed bookings"""
    print(f"Creating reviews for user: {user.email}")
    
    # Get completed bookings for this user
    completed_bookings = Booking.objects.filter(user=user, status='completed')
    
    reviews_data = [
        {
            'rating': 5,
            'title': 'Absolutely Amazing Experience!',
            'comment': 'This was one of the best travel experiences I\'ve ever had. The guides were knowledgeable, the scenery was breathtaking, and everything was well organized. Highly recommend!'
        },
        {
            'rating': 4,
            'title': 'Great Trip, Minor Issues',
            'comment': 'Overall a fantastic experience. The destination was beautiful and the activities were fun. Only minor complaint was the transportation could have been more comfortable.'
        },
        {
            'rating': 5,
            'title': 'Perfect Family Adventure',
            'comment': 'My family and I had an incredible time. The kids loved every moment and we made memories that will last a lifetime. Professional service throughout.'
        }
    ]
    
    reviews = []
    for i, booking in enumerate(completed_bookings[:3]):  # Review up to 3 completed bookings
        if i < len(reviews_data):
            review_data = reviews_data[i]
            
            # Check if review already exists
            existing_review = Review.objects.filter(
                user=user,
                destination=booking.destination
            ).first()
            
            if existing_review:
                print(f"  ✓ Review already exists for: {booking.destination.name}")
                reviews.append(existing_review)
            else:
                review = Review.objects.create(
                    user=user,
                    destination=booking.destination,
                    **review_data
                )
                print(f"  ✓ Created review for: {booking.destination.name} - {review.rating}/5 stars")
                reviews.append(review)
    
    return reviews

def main():
    """Main function to populate data for specific user"""
    user_email = 'wyarquah@gmail.com'
    
    print("="*60)
    print(f"POPULATING DASHBOARD DATA FOR: {user_email}")
    print("="*60)
    
    # Get the user
    user = get_or_create_user(user_email)
    if not user:
        return
    
    # Create bookings
    bookings = create_bookings_for_user(user)
    
    # Create ticket purchases
    purchases = create_ticket_purchases_for_user(user)
    
    # Create reviews
    reviews = create_reviews_for_user(user)
    
    # Calculate summary
    total_bookings = len(bookings)
    total_purchases = len(purchases)
    total_reviews = len(reviews)
    
    booking_total = sum(float(b.total_amount) for b in bookings)
    purchase_total = sum(float(p.total_amount) for p in purchases)
    total_spent = booking_total + purchase_total
    
    completed_destinations = Booking.objects.filter(
        user=user, status='completed'
    ).values('destination').distinct().count()
    
    # Determine member level
    if total_spent >= 5000:
        member_level = 'Platinum'
    elif total_spent >= 2000:
        member_level = 'Gold'
    elif total_spent >= 500:
        member_level = 'Silver'
    else:
        member_level = 'Bronze'
    
    print("\n" + "="*60)
    print("✅ DASHBOARD DATA POPULATION COMPLETE")
    print("="*60)
    print(f"User: {user.email}")
    print(f"📅 Total Bookings: {total_bookings}")
    print(f"🎫 Total Ticket Purchases: {total_purchases}")
    print(f"⭐ Total Reviews: {total_reviews}")
    print(f"💰 Total Spent: GH₵{total_spent:.2f}")
    print(f"🏆 Member Level: {member_level}")
    print(f"🎯 Points: {int(total_spent * 0.1)}")
    print(f"🌍 Destinations Visited: {completed_destinations}")
    print("\n🚀 Dashboard is now loaded with real data!")
    print("📊 Access dashboard at: http://localhost:8080/dashboard")

if __name__ == '__main__':
    main()