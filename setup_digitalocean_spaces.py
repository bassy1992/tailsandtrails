#!/usr/bin/env python3
"""
Setup script for DigitalOcean Spaces integration
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up DigitalOcean Spaces for media storage...")
    
    # Check if we're in the right directory
    if not os.path.exists('Tback/tback_api/settings.py'):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Verify the configuration is in place
    with open('Tback/tback_api/settings.py', 'r') as f:
        content = f.read()
        if 'AWS_STORAGE_BUCKET_NAME' not in content:
            print("❌ Error: DigitalOcean Spaces configuration not found in settings.py")
            sys.exit(1)
    
    print("✅ DigitalOcean Spaces configuration found in settings.py")
    
    # Check requirements.txt
    with open('Tback/requirements.txt', 'r') as f:
        content = f.read()
        if 'django-storages' not in content or 'boto3' not in content:
            print("❌ Error: Required packages not found in requirements.txt")
            sys.exit(1)
    
    print("✅ Required packages found in requirements.txt")
    
    # Test Django configuration
    if not run_command("cd Tback && python manage.py check", "Django configuration check"):
        sys.exit(1)
    
    # Git operations
    if not run_command("git add .", "Adding changes to git"):
        sys.exit(1)
    
    if not run_command('git commit -m "Add DigitalOcean Spaces configuration for media storage"', "Committing changes"):
        print("ℹ️  No changes to commit (already committed)")
    
    if not run_command("git push", "Pushing to repository"):
        sys.exit(1)
    
    print("\n🎉 DigitalOcean Spaces setup completed!")
    
    print("\n📋 What was configured:")
    print("   • Added django-storages and boto3 to requirements.txt")
    print("   • Added 'storages' to INSTALLED_APPS")
    print("   • Configured AWS S3 settings for DigitalOcean Spaces")
    print("   • Set up CDN URL for media serving")
    print("   • Added fallback to local storage for development")
    
    print("\n🔧 Next steps:")
    print("   1. Create a DigitalOcean Spaces bucket named 'tailsandtrailsmedia'")
    print("   2. Generate Spaces API keys in DigitalOcean control panel")
    print("   3. Add these environment variables to Railway:")
    print("      - SPACES_KEY=your_spaces_access_key")
    print("      - SPACES_SECRET=your_spaces_secret_key")
    print("   4. Enable CDN for your Spaces bucket")
    
    print("\n📚 DigitalOcean Spaces Setup Guide:")
    print("   1. Go to https://cloud.digitalocean.com/spaces")
    print("   2. Create a new Space named 'tailsandtrailsmedia' in SFO3 region")
    print("   3. Go to API → Spaces Keys → Generate New Key")
    print("   4. Copy the Access Key and Secret Key")
    print("   5. In your Space settings, enable CDN")
    
    print("\n⏳ Railway will automatically deploy the changes.")
    print("   Media files will be served from DigitalOcean Spaces CDN.")

if __name__ == "__main__":
    main()