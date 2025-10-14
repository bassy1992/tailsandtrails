#!/usr/bin/env python3
"""
Deploy script to fix the Paystack endpoint 404 issue
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
    """Main deployment function"""
    print("🚀 Deploying Paystack endpoint fix...")
    
    # Check if we're in the right directory
    if not os.path.exists('Tback/payments/urls.py'):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Verify the fix is in place
    with open('Tback/payments/urls.py', 'r') as f:
        content = f.read()
        if 'paystack/create/' not in content:
            print("❌ Error: Paystack URLs not found in payments/urls.py")
            print("Please ensure the URLs have been added correctly")
            sys.exit(1)
    
    print("✅ Paystack URLs found in payments/urls.py")
    
    # Test Django configuration
    if not run_command("cd Tback && python manage.py check", "Django configuration check"):
        sys.exit(1)
    
    # Git operations
    if not run_command("git add .", "Adding changes to git"):
        sys.exit(1)
    
    if not run_command('git commit -m "Fix: Add missing Paystack API endpoints to URL configuration"', "Committing changes"):
        print("ℹ️  No changes to commit (already committed)")
    
    if not run_command("git push", "Pushing to repository"):
        sys.exit(1)
    
    print("\n🎉 Deployment completed!")
    print("\n📋 What was fixed:")
    print("   • Added missing Paystack endpoints to payments/urls.py:")
    print("     - /api/payments/paystack/create/")
    print("     - /api/payments/paystack/verify/<reference>/")
    print("     - /api/payments/paystack/webhook/")
    print("     - /api/payments/paystack/callback/")
    print("     - /api/payments/paystack/config/")
    
    print("\n⏳ Railway will automatically deploy the changes.")
    print("   The endpoints should be available in a few minutes.")
    
    print("\n🧪 To test the fix:")
    print("   python test_paystack_endpoint.py")

if __name__ == "__main__":
    main()