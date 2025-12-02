#!/usr/bin/env python
"""
Script to mark migration as applied when table already exists
Run this on Railway: railway run python Tback/fix_migration.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

def fix_migration():
    """Mark the PricingTier migration as applied"""
    recorder = MigrationRecorder(connection)
    
    # Check if migration is already recorded
    migration = recorder.migration_qs.filter(
        app='destinations',
        name='0004_pricingtier'
    ).first()
    
    if migration:
        print("✓ Migration 0004_pricingtier is already recorded")
    else:
        # Record the migration as applied
        recorder.record_applied('destinations', '0004_pricingtier')
        print("✓ Marked migration 0004_pricingtier as applied")
    
    # Verify the table exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'destinations_pricingtier'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✓ Table destinations_pricingtier exists")
        else:
            print("✗ Table destinations_pricingtier does NOT exist")
            print("  You may need to run: python manage.py migrate destinations")

if __name__ == '__main__':
    print("Fixing migration status...\n")
    fix_migration()
    print("\n✅ Done! You can now run setup_pricing_tiers.py")
