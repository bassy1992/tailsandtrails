#!/usr/bin/env python
"""
Script to update destination dates in the database
This ensures all destinations have proper start_date and end_date values
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination

def update_destination_dates():
    """Update all destinations with proper date ranges"""
    destinations = Destination.objects.all()
    
    if not destinations.exists():
        print("No destinations found in database.")
        return
    
    today = datetime.now().date()
    
    for i, destination in enumerate(destinations):
        # Set start date to 7 days from now (to allow for booking preparation)
        start_date = today + timedelta(days=7 + (i * 14))  # Stagger destinations
        
        # Set end date based on duration
        duration_days_map = {
            '1_day': 90,      # Available for 90 days
            '2_days': 120,
            '3_days': 150,
            '4_days': 180,
            '5_days': 180,
            '6_days': 210,
            '7_days': 210,
            '7_plus_days': 240,
        }
        
        # Get the availability window (how long this tour is bookable)
        availability_days = duration_days_map.get(destination.duration, 180)
        end_date = start_date + timedelta(days=availability_days)
        
        # Update the destination
        destination.start_date = start_date
        destination.end_date = end_date
        destination.save()
        
        print(f"✓ Updated {destination.name}")
        print(f"  Start: {start_date.strftime('%Y-%m-%d')}")
        print(f"  End: {end_date.strftime('%Y-%m-%d')}")
        print(f"  Duration: {destination.duration_display}")
        print()
    
    print(f"\n✅ Successfully updated {destinations.count()} destinations with date ranges!")

if __name__ == '__main__':
    print("Updating destination dates...\n")
    update_destination_dates()
