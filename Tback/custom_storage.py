"""
Custom storage configuration for DigitalOcean Spaces
"""
import os
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for DigitalOcean Spaces media files
    """
    bucket_name = 'tailsandtrailsmedia'
    region_name = 'sfo3'
    endpoint_url = 'https://sfo3.digitaloceanspaces.com'
    default_acl = 'public-read'
    custom_domain = 'tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com'
    
    def __init__(self, *args, **kwargs):
        # Only use S3 if credentials are available
        if not (os.getenv('SPACES_KEY') and os.getenv('SPACES_SECRET')):
            raise ValueError("DigitalOcean Spaces credentials not available")
        super().__init__(*args, **kwargs)


def get_storage():
    """
    Return appropriate storage backend based on credentials
    """
    if os.getenv('SPACES_KEY') and os.getenv('SPACES_SECRET'):
        try:
            return MediaStorage()
        except Exception:
            # Fall back to filesystem if S3 fails
            pass
    
    # Return filesystem storage as fallback
    return FileSystemStorage()