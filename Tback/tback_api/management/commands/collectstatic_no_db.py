from django.core.management.commands.collectstatic import Command as CollectStaticCommand
from django.conf import settings
import os

class Command(CollectStaticCommand):
    """
    Custom collectstatic command that works without database connection
    """
    def handle(self, **options):
        # Temporarily disable database operations
        original_databases = settings.DATABASES
        settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
        
        try:
            super().handle(**options)
        finally:
            # Restore original database settings
            settings.DATABASES = original_databases