#!/usr/bin/env python
"""
Script to fix the PricingTier table structure on Railway
Run this on Railway: railway run python Tback/fix_pricingtier_table.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.db import connection

def fix_table():
    """Drop and recreate the PricingTier table with correct structure"""
    with connection.cursor() as cursor:
        print("Checking table structure...")
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'destinations_pricingtier'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✓ Table exists, dropping it...")
            cursor.execute("DROP TABLE IF EXISTS destinations_pricingtier CASCADE;")
            print("✓ Table dropped")
        
        # Now run the migration properly
        print("\nNow run: python manage.py migrate destinations")
        print("This will create the table with the correct structure")

if __name__ == '__main__':
    print("Fixing PricingTier table structure...\n")
    fix_table()
    print("\n✅ Done!")
