"""
Django management command to test storage configuration
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Test storage configuration and upload'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Testing Storage Configuration")
        self.stdout.write("=" * 50)
        
        # Check environment
        spaces_key = os.getenv('SPACES_KEY')
        spaces_secret = os.getenv('SPACES_SECRET')
        
        self.stdout.write(f"Environment Variables:")
        self.stdout.write(f"  SPACES_KEY: {'✅ Set' if spaces_key else '❌ Not set'}")
        self.stdout.write(f"  SPACES_SECRET: {'✅ Set' if spaces_secret else '❌ Not set'}")
        
        # Check Django settings
        self.stdout.write(f"\nDjango Settings:")
        self.stdout.write(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        self.stdout.write(f"  MEDIA_URL: {settings.MEDIA_URL}")
        self.stdout.write(f"  AWS_ACCESS_KEY_ID: {'✅ Set' if settings.AWS_ACCESS_KEY_ID else '❌ Not set'}")
        self.stdout.write(f"  AWS_SECRET_ACCESS_KEY: {'✅ Set' if settings.AWS_SECRET_ACCESS_KEY else '❌ Not set'}")
        
        # Check actual storage
        self.stdout.write(f"\nActual Storage:")
        self.stdout.write(f"  Backend: {default_storage.__class__.__name__}")
        self.stdout.write(f"  Module: {default_storage.__class__.__module__}")
        
        # Test upload
        self.stdout.write(f"\n📤 Testing Upload:")
        try:
            test_content = b"Test file from Railway management command"
            test_file = ContentFile(test_content, name="railway-test.txt")
            
            file_path = default_storage.save("management-test/railway-test.txt", test_file)
            self.stdout.write(f"  ✅ Upload successful: {file_path}")
            
            file_url = default_storage.url(file_path)
            self.stdout.write(f"  📄 File URL: {file_url}")
            
            exists = default_storage.exists(file_path)
            self.stdout.write(f"  🔍 File exists: {'✅ Yes' if exists else '❌ No'}")
            
            if 'digitaloceanspaces.com' in file_url:
                self.stdout.write(f"  🎉 Using DigitalOcean Spaces!")
            else:
                self.stdout.write(f"  ⚠️  Using local storage")
                
        except Exception as e:
            self.stdout.write(f"  ❌ Upload failed: {e}")
        
        self.stdout.write("=" * 50)