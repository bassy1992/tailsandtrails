#!/usr/bin/env python
"""
Script to apply the booking_type changes to the database.
Run this script from the Tback directory.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def main():
    print("🚀 Applying booking_type changes to the database...")
    print()
    
    # Run migrations
    print("1. Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', 'destinations'])
        print("✅ Migrations applied successfully!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return
    
    print()
    
    # Run the update command in dry-run mode first
    print("2. Checking existing bookings (dry-run)...")
    try:
        execute_from_command_line(['manage.py', 'update_booking_types', '--dry-run'])
    except Exception as e:
        print(f"❌ Dry-run failed: {e}")
        return
    
    print()
    
    # Ask user if they want to proceed with actual update
    response = input("Do you want to proceed with updating the bookings? (y/N): ")
    if response.lower() in ['y', 'yes']:
        print("3. Updating existing bookings...")
        try:
            execute_from_command_line(['manage.py', 'update_booking_types'])
            print("✅ Bookings updated successfully!")
        except Exception as e:
            print(f"❌ Update failed: {e}")
            return
    else:
        print("3. Skipping booking updates.")
    
    print()
    print("🎉 Booking type changes have been applied!")
    print()
    print("Summary of changes:")
    print("- Added 'booking_type' field to Booking model")
    print("- Added database indexes for better performance")
    print("- Updated admin interface to show booking types")
    print("- Updated API serializers to include booking type info")
    print("- Added helper properties: is_destination_booking, is_ticket_booking")
    print()
    print("You can now distinguish between destination bookings and ticket bookings!")

if __name__ == '__main__':
    main()