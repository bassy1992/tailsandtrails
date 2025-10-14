#!/usr/bin/env python3
"""
Check what files exist in DigitalOcean Spaces bucket
"""
import os
import boto3
from botocore.exceptions import ClientError

def check_spaces_files():
    print("🔍 Checking DigitalOcean Spaces Files")
    print("=" * 50)
    
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
    
    try:
        print(f"📦 Listing files in bucket: tailsandtrailsmedia")
        
        # List all objects in the bucket
        response = client.list_objects_v2(Bucket='tailsandtrailsmedia')
        
        if 'Contents' in response:
            print(f"\n✅ Found {len(response['Contents'])} files:")
            for obj in response['Contents']:
                key = obj['Key']
                size = obj['Size']
                modified = obj['LastModified']
                print(f"   📄 {key} ({size} bytes, {modified})")
                
                # Show the CDN URL for each file
                cdn_url = f"https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/{key}"
                print(f"      🔗 CDN URL: {cdn_url}")
        else:
            print(f"\n📭 Bucket is empty - no files found")
            
        # Check specifically for destinations folder
        print(f"\n🔍 Checking destinations/ folder...")
        response = client.list_objects_v2(
            Bucket='tailsandtrailsmedia',
            Prefix='destinations/'
        )
        
        if 'Contents' in response:
            print(f"✅ Found {len(response['Contents'])} files in destinations/:")
            for obj in response['Contents']:
                print(f"   📄 {obj['Key']}")
        else:
            print(f"📭 No files in destinations/ folder")
            
    except ClientError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    check_spaces_files()