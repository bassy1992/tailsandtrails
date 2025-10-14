from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Run migrations only if not in build phase'

    def handle(self, *args, **options):
        if os.getenv('RAILWAY_SKIP_BUILD_MIGRATIONS') == 'true':
            self.stdout.write(
                self.style.WARNING('Skipping migrations during build phase')
            )
            return
        
        self.stdout.write('Running migrations...')
        call_command('migrate', verbosity=1)