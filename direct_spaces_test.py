#!/usr/bin/env python3
"""
Direct DigitalOcean Spaces upload test (bypass Django)
"""
import os
import boto3
from botocore.exceptions import ClientError

def test_direct_spaces_upload():
    print("🧪 Direct DigitalOcean Spaces Test")
    print("=" * 50)
    
    # Get credentials from environment
    spaces_key = os.getenv('SPACES_KEY')
    spaces_secret = os.getenv('SPACES_SECRET')
    
    print(f"SPACES_KEY: {'✅ Set' if spaces_key else '❌ Not set'}")
    print(f"SPACES_SECRET: {'✅ Set' if spaces_secret else '❌ Not set'}")
    
    if not spaces_key or not spaces_secret:
        print("❌ Missing credentials")
        return False
    
    try:
        # Create S3 client for DigitalOcean Spaces
        client = boto3.client(
            's3',
            region_name='sfo3',
            endpoint_url='https://sfo3.digitaloceanspaces.com',
            aws_access_key_id=spaces_key,
            aws_secret_access_key=spaces_secret
        )
        
        print(f"\n📤 Testing direct upload...")
        
        # Upload a test file
        test_content = b"Direct upload test from Railway"
        client.put_object(
            Bucket='tailsandtrailsmedia',
            Key='direct-test/railway-direct-test.txt',
            Body=test_content,
            ContentType='text/plain',
            ACL='public-read'
        )
        
        print(f"✅ Direct upload successful!")
        
        # Generate URL
        url = f"https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/direct-test/railway-direct-test.txt"
        print(f"📄 File URL: {url}")
        
        # Test if file exists
        try:
            client.head_object(Bucket='tailsandtrailsmedia', Key='direct-test/railway-direct-test.txt')
            print(f"✅ File exists in bucket")
        except ClientError:
            print(f"❌ File not found in bucket")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct upload failed: {e}")
        return False

if __name__ == "__main__":
    test_direct_spaces_upload()