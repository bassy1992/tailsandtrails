#!/usr/bin/env python
"""
Restart Django server to pick up new environment variables
"""
import os
import sys
import subprocess
import signal
import time

def kill_django_servers():
    """Kill existing Django server processes"""
    print("🔄 Stopping existing Django servers...")
    
    try:
        # On Windows, use taskkill to stop Python processes running Django
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True)
        
        if 'python.exe' in result.stdout:
            print("   Found Python processes, attempting to stop Django servers...")
            # Kill processes that might be Django servers
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                          capture_output=True)
            time.sleep(2)
            print("   ✅ Stopped existing processes")
        else:
            print("   No Python processes found")
            
    except Exception as e:
        print(f"   ⚠️  Could not stop processes: {e}")

def check_environment():
    """Check if environment variables are loaded correctly"""
    print("\n🔍 Checking Environment Variables...")
    
    # Load environment manually to verify
    from dotenv import load_dotenv
    load_dotenv('.env')
    
    public_key = os.getenv('PAYSTACK_PUBLIC_KEY', '')
    secret_key = os.getenv('PAYSTACK_SECRET_KEY', '')
    
    print(f"   Public Key: {public_key[:20]}..." if public_key else "   Public Key: NOT SET")
    print(f"   Secret Key: {secret_key[:20]}..." if secret_key else "   Secret Key: NOT SET")
    
    if public_key and secret_key:
        print("   ✅ Environment variables loaded correctly")
        return True
    else:
        print("   ❌ Environment variables not loaded")
        return False

def start_server():
    """Start Django development server"""
    print("\n🚀 Starting Django Server...")
    
    try:
        # Start server in background
        print("   Starting server on http://localhost:8000")
        print("   Press Ctrl+C to stop the server")
        
        # Run the server
        subprocess.run([sys.executable, 'manage.py', 'runserver'], 
                      cwd=os.path.dirname(os.path.abspath(__file__)))
        
    except KeyboardInterrupt:
        print("\n   Server stopped by user")
    except Exception as e:
        print(f"   ❌ Failed to start server: {e}")

def main():
    """Main function"""
    print("🔄 Django Server Restart Script")
    print("=" * 40)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Kill existing servers
    kill_django_servers()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment variables not configured correctly")
        print("   Please check your .env file")
        return
    
    # Start server
    start_server()

if __name__ == '__main__':
    main()