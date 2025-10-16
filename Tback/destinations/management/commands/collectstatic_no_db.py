from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand
from django.conf import settings
from django.core.management.base import CommandError
import os
import sys

class Command(CollectStaticCommand):
    """
    Custom collectstatic command that works without database connection.
    
    This is useful for deployment scenarios where static files need to be
    collected before the database is available or configured.
    
    Usage:
        python manage.py collectstatic_no_db --noinput
    """
    
    help = 'Collect static files without requiring database connection'
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--skip-db-backup',
            action='store_true',
            help='Skip backing up original database settings (faster but less safe)',
        )
    
    def handle(self, **options):
        self.verbosity = options.get('verbosity', 1)
        skip_backup = options.get('skip_db_backup', False)
        
        if self.verbosity >= 1:
            self.stdout.write("Starting collectstatic without database connection...")
        
        # Store original database settings if not skipping backup
        original_databases = None
        if not skip_backup:
            original_databases = getattr(settings, 'DATABASES', {}).copy()
            if self.verbosity >= 2:
                self.stdout.write("Backed up original database settings")
        
        # Set up in-memory SQLite database to avoid connection issues
        settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'OPTIONS': {
                    'timeout': 1,  # Quick timeout for any accidental DB access
                },
            }
        }
        
        if self.verbosity >= 2:
            self.stdout.write("Temporarily using in-memory database")
        
        try:
            # Disable any middleware that might try to access the database
            original_middleware = getattr(settings, 'MIDDLEWARE', [])
            
            # Filter out potentially problematic middleware
            safe_middleware = [
                mw for mw in original_middleware 
                if not any(problematic in mw.lower() for problematic in [
                    'session', 'auth', 'csrf', 'messages'
                ])
            ]
            
            if len(safe_middleware) != len(original_middleware):
                settings.MIDDLEWARE = safe_middleware
                if self.verbosity >= 2:
                    self.stdout.write("Temporarily disabled database-dependent middleware")
            
            # Run the actual collectstatic command
            if self.verbosity >= 1:
                self.stdout.write("Collecting static files...")
            
            super().handle(**options)
            
            if self.verbosity >= 1:
                self.stdout.write(
                    self.style.SUCCESS("Static files collected successfully without database!")
                )
                
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error during static file collection: {e}")
            )
            if self.verbosity >= 2:
                import traceback
                self.stderr.write(traceback.format_exc())
            raise CommandError(f"Failed to collect static files: {e}")
            
        finally:
            # Restore original settings
            if not skip_backup and original_databases is not None:
                settings.DATABASES = original_databases
                if self.verbosity >= 2:
                    self.stdout.write("Restored original database settings")
            
            # Restore original middleware
            if 'original_middleware' in locals():
                settings.MIDDLEWARE = original_middleware
                if self.verbosity >= 2:
                    self.stdout.write("Restored original middleware settings")
        
        if self.verbosity >= 1:
            self.stdout.write("collectstatic_no_db completed successfully!")