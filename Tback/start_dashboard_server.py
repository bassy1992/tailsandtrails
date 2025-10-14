#!/usr/bin/env python
"""
Start Django server for dashboard testing
"""
import os
import sys
import subprocess
import requests
import time

def check_server_running():
    """Check if Django server is already running"""
    try:
        response = requests.get('http://localhost:8000/api/health/', timeout=2)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start Django development server"""
    if check_server_running():
        print("✅ Django server is already running at http://localhost:8000")
        print("✅ Dashboard API is available at http://localhost:8000/api/dashboard/")
        return True
    
    print("🚀 Starting Django development server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📊 Dashboard API endpoints:")
    print("   • Overview: http://localhost:8000/api/dashboard/overview/")
    print("   • Bookings: http://localhost:8000/api/dashboard/bookings/")
    print("   • Activity: http://localhost:8000/api/dashboard/activity/")
    print("\n💡 Use Ctrl+C to stop the server")
    print("="*60)
    
    # Start the server
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '8000'
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    start_server()