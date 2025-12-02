#!/usr/bin/env python
"""
Script to add missing columns to PricingTier table
Run this on Railway: railway run python Tback/add_pricing_columns.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.db import connection

def add_columns():
    """Add missing columns to destinations_pricingtier table"""
    with connection.cursor() as cursor:
        print("Checking table structure...")
        
        # Get current columns
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'destinations_pricingtier';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Existing columns: {', '.join(existing_columns)}")
        
        # Add total_price if missing
        if 'total_price' not in existing_columns:
            print("\nAdding total_price column...")
            cursor.execute("""
                ALTER TABLE destinations_pricingtier 
                ADD COLUMN total_price NUMERIC(10, 2) NOT NULL DEFAULT 0;
            """)
            print("✓ Added total_price column")
        else:
            print("\n✓ total_price column already exists")
        
        # Add price_per_person if missing
        if 'price_per_person' not in existing_columns:
            print("Adding price_per_person column...")
            cursor.execute("""
                ALTER TABLE destinations_pricingtier 
                ADD COLUMN price_per_person NUMERIC(10, 2) NOT NULL DEFAULT 0;
            """)
            print("✓ Added price_per_person column")
        else:
            print("✓ price_per_person column already exists")
        
        # Add created_at if missing
        if 'created_at' not in existing_columns:
            print("Adding created_at column...")
            cursor.execute("""
                ALTER TABLE destinations_pricingtier 
                ADD COLUMN created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW();
            """)
            print("✓ Added created_at column")
        else:
            print("✓ created_at column already exists")
        
        # Add updated_at if missing
        if 'updated_at' not in existing_columns:
            print("Adding updated_at column...")
            cursor.execute("""
                ALTER TABLE destinations_pricingtier 
                ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW();
            """)
            print("✓ Added updated_at column")
        else:
            print("✓ updated_at column already exists")
        
        print("\n✅ Table structure updated successfully!")
        print("\nYou can now:")
        print("1. Add pricing tiers via Django admin")
        print("2. Or run: python setup_pricing_tiers.py")

if __name__ == '__main__':
    print("Adding missing columns to PricingTier table...\n")
    add_columns()
