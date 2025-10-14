#!/usr/bin/env python
"""
Start the auto-completion daemon for demo payments
"""
import subprocess
import sys
import os

def start_daemon():
    """Start the auto-completion daemon"""
    
    print("🚀 Starting Auto-Completion Daemon")
    print("=" * 40)
    print("This daemon will automatically complete demo payments after 30 seconds")
    print("Press Ctrl+C to stop the daemon")
    print()
    
    try:
        # Start the daemon
        subprocess.run([
            sys.executable, 'manage.py', 'auto_complete_daemon',
            '--interval', '10',  # Check every 10 seconds
            '--timeout', '30',   # Complete payments after 30 seconds
            '--success-rate', '0.9'  # 90% success rate
        ])
    except KeyboardInterrupt:
        print("\n🛑 Auto-completion daemon stopped")
    except Exception as e:
        print(f"❌ Error starting daemon: {str(e)}")
        print("\nAlternative: Run manually with:")
        print("python manage.py auto_complete_demo_payments --timeout 0")

if __name__ == "__main__":
    start_daemon()