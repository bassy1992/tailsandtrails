#!/usr/bin/env python3
"""
Deploy the mobile money test mode fix
"""
import os
import subprocess
import sys

def deploy_fix():
    """Deploy the mobile money fix"""
    
    print("🚀 Deploying Mobile Money Test Mode Fix")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('Tback/payments/paystack_service.py'):
        print("❌ Error: Not in the correct directory")
        print("Please run this from the project root directory")
        return False
    
    try:
        # Step 1: Check current git status
        print("📋 Checking git status...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("📝 Found changes to commit:")
            print(result.stdout)
            
            # Step 2: Add changes
            print("➕ Adding changes...")
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Step 3: Commit changes
            print("💾 Committing changes...")
            commit_message = "Fix mobile money payments in test mode - auto-approve after 10 seconds"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Step 4: Push to Railway
            print("🚂 Pushing to Railway...")
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            
            print("✅ Fix deployed successfully!")
            print("\n📋 What was fixed:")
            print("   • Mobile money payments now work in test mode")
            print("   • Payments auto-approve after 10 seconds in test mode")
            print("   • Users get clear feedback about test mode")
            print("   • No more 'Payment declined or cancelled' errors")
            
            print("\n⏰ Deployment will take 2-3 minutes to go live")
            print("   Test again after deployment completes")
            
            return True
        else:
            print("ℹ️  No changes to deploy")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

def check_deployment_status():
    """Check if the deployment is ready"""
    print("\n🔍 Checking deployment status...")
    
    try:
        import requests
        
        # Test the API endpoint
        response = requests.get(
            "https://tailsandtrails-production.up.railway.app/api/payments/checkout/methods/",
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API is responding - deployment likely complete")
            return True
        else:
            print(f"⚠️  API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Could not reach API: {e}")
        return False

if __name__ == "__main__":
    success = deploy_fix()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Wait 2-3 minutes for Railway deployment")
        print("2. Test mobile money payments again")
        print("3. Payments should auto-approve after 10 seconds in test mode")
        
        # Check if we can test deployment status
        if check_deployment_status():
            print("\n✨ You can test the fix now with:")
            print("   python test_momo_fix.py")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")