#!/usr/bin/env python3
"""
Test DigitalOcean Spaces connection with current credentials
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

def test_spaces_connection():
    print("🧪 Testing DigitalOcean Spaces Connection")
    print("=" * 50)
    
    # Check environment variables
    spaces_key = os.getenv('SPACES_KEY')
    spaces_secret = os.getenv('SPACES_SECRET')
    
    print(f"SPACES_KEY: {'✅ Set' if spaces_key else '❌ Not set'}")
    print(f"SPACES_SECRET: {'✅ Set' if spaces_secret else '❌ Not set'}")
    
    if not spaces_key or not spaces_secret:
        print("\n❌ Missing credentials - set SPACES_KEY and SPACES_SECRET")
        return False
    
    # Test boto3 connection
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        # Create S3 client for DigitalOcean Spaces
        client = boto3.client(
            's3',
            region_name='sfo3',
            endpoint_url='https://sfo3.digitaloceanspaces.com',
            aws_access_key_id=spaces_key,
            aws_secret_access_key=spaces_secret
        )
        
        print(f"\n🔍 Testing connection to bucket: tailsandtrailsmedia")
        
        # Test bucket access
        response = client.head_bucket(Bucket='tailsandtrailsmedia')
        print("✅ Bucket access successful!")
        
        # Test list objects
        response = client.list_objects_v2(Bucket='tailsandtrailsmedia', MaxKeys=1)
        print(f"✅ Bucket listing successful! Objects: {response.get('KeyCount', 0)}")
        
        # Test upload permissions with a small test file
        test_content = b"test file content"
        client.put_object(
            Bucket='tailsandtrailsmedia',
            Key='test-connection.txt',
            Body=test_content,
            ContentType='text/plain'
        )
        print("✅ Upload test successful!")
        
        # Clean up test file
        client.delete_object(Bucket='tailsandtrailsmedia', Key='test-connection.txt')
        print("✅ Delete test successful!")
        
        print(f"\n🎉 All tests passed! Your Spaces configuration is working.")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        print(f"\n❌ Connection failed: {error_code}")
        print(f"   Message: {error_msg}")
        
        if error_code == 'AccessDenied':
            print("\n💡 Possible solutions:")
            print("   1. Check your SPACES_KEY and SPACES_SECRET are correct")
            print("   2. Verify the API key has Read + Write permissions")
            print("   3. Make sure the bucket 'tailsandtrailsmedia' exists in sfo3")
        
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_spaces_connection()