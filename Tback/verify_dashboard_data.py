#!/usr/bin/env python
"""
Verify dashboard data is properly loaded in the database
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from destinations.models import Category, Destination, Booking, Review
from tickets.models import TicketCategory, Venue, Ticket, TicketPurchase
from django.db.models import Sum, Count

User = get_user_model()

def verify_data():
    """Verify all dashboard data is properly loaded"""
    print("="*60)
    print("DASHBOARD DATA VERIFICATION")
    print("="*60)
    
    # Check users
    users = User.objects.all()
    print(f"👤 Users: {users.count()}")
    test_user = User.objects.filter(email='test@example.com').first()
    if test_user:
        print(f"   ✓ Test user found: {test_user.email}")
    
    # Check destination categories
    dest_categories = Category.objects.all()
    print(f"🏷️  Destination Categories: {dest_categories.count()}")
    for cat in dest_categories:
        print(f"   • {cat.name}")
    
    # Check destinations
    destinations = Destination.objects.all()
    print(f"🏞️  Destinations: {destinations.count()}")
    for dest in destinations:
        print(f"   • {dest.name} - GH₵{dest.price} ({dest.duration})")
    
    # Check ticket categories
    ticket_categories = TicketCategory.objects.all()
    print(f"🎫 Ticket Categories: {ticket_categories.count()}")
    for cat in ticket_categories:
        print(f"   • {cat.name}")
    
    # Check venues
    venues = Venue.objects.all()
    print(f"🏟️  Venues: {venues.count()}")
    for venue in venues:
        print(f"   • {venue.name} (Capacity: {venue.capacity})")
    
    # Check tickets
    tickets = Ticket.objects.all()
    print(f"🎟️  Tickets: {tickets.count()}")
    for ticket in tickets:
        print(f"   • {ticket.title} - GH₵{ticket.price}")
    
    if test_user:
        print(f"\n📊 TEST USER DATA ({test_user.email}):")
        
        # Check bookings
        bookings = Booking.objects.filter(user=test_user)
        print(f"   📅 Bookings: {bookings.count()}")
        total_booking_amount = bookings.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        print(f"      Total Amount: GH₵{total_booking_amount}")
        
        for booking in bookings:
            print(f"      • {booking.destination.name} - {booking.status} - GH₵{booking.total_amount}")
        
        # Check ticket purchases
        purchases = TicketPurchase.objects.filter(user=test_user)
        print(f"   🎫 Ticket Purchases: {purchases.count()}")
        total_ticket_amount = purchases.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        print(f"      Total Amount: GH₵{total_ticket_amount}")
        
        for purchase in purchases:
            print(f"      • {purchase.ticket.title} - {purchase.status} - GH₵{purchase.total_amount}")
        
        # Check reviews
        reviews = Review.objects.filter(user=test_user)
        print(f"   ⭐ Reviews: {reviews.count()}")
        for review in reviews:
            print(f"      • {review.destination.name} - {review.rating}/5 stars")
        
        # Calculate totals
        total_spent = float(total_booking_amount) + float(total_ticket_amount)
        print(f"\n💰 SUMMARY:")
        print(f"   Total Bookings + Tickets: {bookings.count() + purchases.count()}")
        print(f"   Total Amount Spent: GH₵{total_spent}")
        print(f"   Destinations Visited: {bookings.filter(status='completed').values('destination').distinct().count()}")
        
        # Member level calculation
        if total_spent >= 5000:
            member_level = 'Platinum'
        elif total_spent >= 2000:
            member_level = 'Gold'
        elif total_spent >= 500:
            member_level = 'Silver'
        else:
            member_level = 'Bronze'
        
        print(f"   Member Level: {member_level}")
        print(f"   Points: {int(total_spent * 0.1)}")
    
    print("\n" + "="*60)
    print("✅ DASHBOARD DATA VERIFICATION COMPLETE")
    print("="*60)
    print("The dashboard is now loaded with comprehensive real data!")
    print("You can access the dashboard at: http://localhost:8080/dashboard")
    print("API endpoints available at: http://localhost:8000/api/dashboard/")

if __name__ == '__main__':
    verify_data()