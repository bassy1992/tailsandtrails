#!/usr/bin/env python
"""
Script to help upload images to destinations
"""
import os
import sys
import requests
import json
from pathlib import Path

def upload_destination_image(destination_id, image_path, admin_token):
    """Upload main image for a destination"""
    
    # Production API URL
    api_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # Prepare the upload
    upload_url = f"{api_url}/destinations/{destination_id}/upload-image/"
    
    headers = {
        'Authorization': f'Token {admin_token}'
    }
    
    # Open and upload the image
    with open(image_path, 'rb') as image_file:
        files = {
            'image': image_file
        }
        
        print(f"Uploading {image_path} to destination {destination_id}...")
        
        try:
            response = requests.patch(upload_url, headers=headers, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Image URL: {result.get('image_url', 'No URL returned')}")
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

def upload_gallery_image(destination_id, image_path, admin_token, alt_text="", is_primary=False):
    """Upload gallery image for a destination"""
    
    # Production API URL
    api_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # Prepare the upload
    upload_url = f"{api_url}/destinations/gallery/upload/"
    
    headers = {
        'Authorization': f'Token {admin_token}'
    }
    
    # Prepare form data
    data = {
        'destination': destination_id,
        'alt_text': alt_text,
        'is_primary': is_primary
    }
    
    # Open and upload the image
    with open(image_path, 'rb') as image_file:
        files = {
            'image': image_file
        }
        
        print(f"Uploading gallery image {image_path} to destination {destination_id}...")
        
        try:
            response = requests.post(upload_url, headers=headers, files=files, data=data, timeout=30)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Success! Gallery image uploaded")
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

def get_destinations():
    """Get list of destinations"""
    api_url = "https://tailsandtrails-production.up.railway.app/api"
    
    try:
        response = requests.get(f"{api_url}/destinations/", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get destinations: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting destinations: {e}")
        return []

def main():
    """Main upload function"""
    print("🖼️ DESTINATION IMAGE UPLOAD TOOL")
    print("=" * 50)
    
    # Get admin token (you'll need to provide this)
    admin_token = input("Enter your admin token: ").strip()
    if not admin_token:
        print("❌ Admin token is required!")
        return
    
    # Get destinations
    print("\n📋 Getting destinations...")
    destinations = get_destinations()
    
    if not destinations:
        print("❌ No destinations found!")
        return
    
    print(f"Found {len(destinations)} destinations:")
    for i, dest in enumerate(destinations, 1):
        print(f"{i}. {dest['name']} (ID: {dest['id']})")
    
    print("\n" + "=" * 50)
    print("📁 IMAGE UPLOAD INSTRUCTIONS:")
    print("1. Place your images in a folder on your PC")
    print("2. Name them clearly (e.g., 'volta_waterfall.jpg', 'kumasi_cultural.jpg')")
    print("3. Use this script to upload them one by one")
    print("\n💡 Example usage:")
    print("   python upload_images.py")
    print("   Then follow the prompts to upload images")
    
    # Interactive upload
    while True:
        print("\n" + "-" * 30)
        dest_id = input("Enter destination ID (or 'quit' to exit): ").strip()
        
        if dest_id.lower() == 'quit':
            break
            
        try:
            dest_id = int(dest_id)
        except ValueError:
            print("❌ Please enter a valid destination ID")
            continue
        
        image_path = input("Enter full path to image file: ").strip()
        
        if not os.path.exists(image_path):
            print("❌ Image file not found!")
            continue
        
        # Upload main image
        success = upload_destination_image(dest_id, image_path, admin_token)
        
        if success:
            # Ask if they want to upload gallery images too
            gallery_choice = input("Upload as gallery image too? (y/n): ").strip().lower()
            if gallery_choice == 'y':
                alt_text = input("Enter alt text (optional): ").strip()
                upload_gallery_image(dest_id, image_path, admin_token, alt_text, is_primary=True)

if __name__ == '__main__':
    main()