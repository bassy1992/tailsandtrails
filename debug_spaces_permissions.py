#!/usr/bin/env python3
"""
Debug DigitalOcean Spaces permissions and configuration
"""
import os
import boto3
from botocore.exceptions import ClientError

def debug_spaces_permissions():
    print("🔍 Debugging DigitalOcean Spaces Permissions")
    print("=" * 60)
    
    spaces_key = os.getenv('SPACES_KEY')
    spaces_secret = os.getenv('SPACES_SECRET')
    
    if not spaces_key or not spaces_secret:
        print("❌ Credentials not set")
        return
    
    # Create S3 client
    client = boto3.client(
        's3',
        region_name='sfo3',
        endpoint_url='https://sfo3.digitaloceanspaces.com',
        aws_access_key_id=spaces_key,
        aws_secret_access_key=spaces_secret
    )
    
    print(f"🔑 Using credentials:")
    print(f"   Key: {spaces_key[:20]}...")
    print(f"   Secret: {spaces_secret[:10]}...")
    print(f"   Endpoint: https://sfo3.digitaloceanspaces.com")
    print(f"   Bucket: tailsandtrailsmedia")
    
    # Test different operations to see what's allowed
    tests = [
        ("List all buckets", lambda: client.list_buckets()),
        ("Check bucket exists", lambda: client.head_bucket(Bucket='tailsandtrailsmedia')),
        ("List bucket contents", lambda: client.list_objects_v2(Bucket='tailsandtrailsmedia', MaxKeys=1)),
        ("Get bucket location", lambda: client.get_bucket_location(Bucket='tailsandtrailsmedia')),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 {test_name}...")
            result = test_func()
            print(f"   ✅ Success!")
            
            if test_name == "List all buckets":
                buckets = [b['Name'] for b in result.get('Buckets', [])]
                print(f"   📦 Available buckets: {buckets}")
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            print(f"   ❌ Failed: {error_code} - {error_msg}")
            
            if error_code == 'AccessDenied':
                print(f"   💡 This operation requires additional permissions")
            elif error_code == 'NoSuchBucket':
                print(f"   💡 The bucket 'tailsandtrailsmedia' doesn't exist or isn't accessible")
                
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📋 RECOMMENDATIONS:")
    print(f"1. Check your DigitalOcean Spaces API key has these permissions:")
    print(f"   • Read access to Spaces")
    print(f"   • Write access to Spaces")
    print(f"2. Verify the bucket 'tailsandtrailsmedia' exists in sfo3 region")
    print(f"3. Consider regenerating your API key if permissions look correct")

if __name__ == "__main__":
    debug_spaces_permissions()