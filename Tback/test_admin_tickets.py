#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib import admin
from tickets.models import TicketCategory, Venue, Ticket, TicketPurchase, TicketCode, TicketReview, TicketPromoCode

print("=== ADMIN REGISTRATION TEST ===")
print(f"Total registered models: {len(admin.site._registry)}")
print("\nTicket models registration status:")

ticket_models = [TicketCategory, Venue, Ticket, TicketPurchase, TicketCode, TicketReview, TicketPromoCode]

for model in ticket_models:
    is_registered = model in admin.site._registry
    print(f"✅ {model.__name__}: {'Registered' if is_registered else '❌ NOT Registered'}")

print(f"\nAll registered model names:")
for model in admin.site._registry.keys():
    if 'ticket' in model.__name__.lower():
        print(f"  - {model.__name__}")

print(f"\nTicket data in database:")
print(f"  Categories: {TicketCategory.objects.count()}")
print(f"  Venues: {Venue.objects.count()}")
print(f"  Tickets: {Ticket.objects.count()}")

if Ticket.objects.exists():
    print(f"  Sample ticket: {Ticket.objects.first().title}")