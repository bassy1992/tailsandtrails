#!/usr/bin/env python
"""
Complete dashboard summary for wyarquah@gmail.com
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from destinations.models import Booking, Review
from tickets.models import TicketPurchase
from django.db.models import Sum, Count
from rest_framework.authtoken.models import Token

User = get_user_model()

def generate_dashboard_summary():
    """Generate complete dashboard summary"""
    user_email = 'wyarquah@gmail.com'
    
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        print(f"❌ User {user_email} not found")
        return
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    
    print("="*80)
    print("🎯 DASHBOARD DATA SUMMARY")
    print("="*80)
    print(f"👤 User: {user.email}")
    print(f"🔑 Auth Token: {token.key}")
    print(f"📅 Member Since: {user.date_joined.strftime('%B %d, %Y')}")
    
    # Bookings Summary
    bookings = Booking.objects.filter(user=user)
    booking_stats = bookings.aggregate(
        total_count=Count('id'),
        total_amount=Sum('total_amount')
    )
    
    print(f"\n🏞️  DESTINATION BOOKINGS:")
    print(f"   📊 Total Bookings: {booking_stats['total_count']}")
    print(f"   💰 Total Amount: GH₵{booking_stats['total_amount'] or 0}")
    
    status_counts = bookings.values('status').annotate(count=Count('id'))
    for status in status_counts:
        emoji = {'confirmed': '✅', 'pending': '⏳', 'completed': '✔️', 'cancelled': '❌'}.get(status['status'], '❓')
        print(f"   {emoji} {status['status'].title()}: {status['count']}")
    
    # Ticket Purchases Summary
    purchases = TicketPurchase.objects.filter(user=user)
    purchase_stats = purchases.aggregate(
        total_count=Count('id'),
        total_amount=Sum('total_amount')
    )
    
    print(f"\n🎫 TICKET PURCHASES:")
    print(f"   📊 Total Purchases: {purchase_stats['total_count']}")
    print(f"   💰 Total Amount: GH₵{purchase_stats['total_amount'] or 0}")
    
    ticket_status_counts = purchases.values('status').annotate(count=Count('id'))
    for status in ticket_status_counts:
        emoji = {'confirmed': '✅', 'pending': '⏳', 'completed': '✔️', 'used': '✔️', 'cancelled': '❌'}.get(status['status'], '❓')
        print(f"   {emoji} {status['status'].title()}: {status['count']}")
    
    # Reviews Summary
    reviews = Review.objects.filter(user=user)
    avg_rating = reviews.aggregate(avg_rating=Sum('rating'))['avg_rating']
    if reviews.count() > 0:
        avg_rating = avg_rating / reviews.count()
    
    print(f"\n⭐ REVIEWS:")
    print(f"   📊 Total Reviews: {reviews.count()}")
    if reviews.count() > 0:
        print(f"   🌟 Average Rating: {avg_rating:.1f}/5.0")
    
    # Overall Summary
    total_spent = float(booking_stats['total_amount'] or 0) + float(purchase_stats['total_amount'] or 0)
    total_activities = booking_stats['total_count'] + purchase_stats['total_count']
    completed_destinations = bookings.filter(status='completed').values('destination').distinct().count()
    
    # Member Level
    if total_spent >= 5000:
        member_level = 'Platinum 💎'
    elif total_spent >= 2000:
        member_level = 'Gold 🥇'
    elif total_spent >= 500:
        member_level = 'Silver 🥈'
    else:
        member_level = 'Bronze 🥉'
    
    print(f"\n💎 MEMBERSHIP SUMMARY:")
    print(f"   🏆 Member Level: {member_level}")
    print(f"   💰 Total Spent: GH₵{total_spent:.2f}")
    print(f"   📈 Total Activities: {total_activities}")
    print(f"   🌍 Destinations Visited: {completed_destinations}")
    print(f"   🎯 Loyalty Points: {int(total_spent * 0.1)}")
    
    print(f"\n🔗 API ENDPOINTS:")
    print(f"   📊 Overview: http://localhost:8000/api/dashboard/overview/")
    print(f"   📅 Bookings: http://localhost:8000/api/dashboard/bookings/")
    print(f"   📋 Activity: http://localhost:8000/api/dashboard/activity/")
    
    print(f"\n🌐 FRONTEND ACCESS:")
    print(f"   🎯 Dashboard: http://localhost:8080/dashboard")
    print(f"   🔐 Login with: {user.email}")
    
    print("\n" + "="*80)
    print("✅ DASHBOARD IS FULLY LOADED WITH REAL DATA!")
    print("="*80)
    
    # Recent bookings preview
    print(f"\n📋 RECENT BOOKINGS PREVIEW:")
    recent_bookings = bookings.order_by('-created_at')[:3]
    for i, booking in enumerate(recent_bookings, 1):
        status_emoji = {'confirmed': '✅', 'pending': '⏳', 'completed': '✔️', 'cancelled': '❌'}.get(booking.status, '❓')
        print(f"   {i}. {booking.destination.name}")
        print(f"      {status_emoji} {booking.status.title()} | GH₵{booking.total_amount} | {booking.participants} participants")
    
    # Recent tickets preview
    print(f"\n🎫 RECENT TICKETS PREVIEW:")
    recent_tickets = purchases.order_by('-created_at')[:3]
    for i, purchase in enumerate(recent_tickets, 1):
        status_emoji = {'confirmed': '✅', 'pending': '⏳', 'completed': '✔️', 'used': '✔️', 'cancelled': '❌'}.get(purchase.status, '❓')
        print(f"   {i}. {purchase.ticket.title}")
        print(f"      {status_emoji} {purchase.status.title()} | GH₵{purchase.total_amount} | {purchase.quantity} tickets")

if __name__ == '__main__':
    generate_dashboard_summary()