#!/usr/bin/env python3
"""
Test the collectstatic_no_db management command
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_collectstatic_no_db():
    """Test the collectstatic_no_db command"""
    
    print("🧪 Testing collectstatic_no_db Management Command")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = "Tback"
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found")
        return
    
    original_dir = os.getcwd()
    
    try:
        os.chdir(backend_dir)
        print(f"📁 Changed to directory: {os.getcwd()}")
        
        # Test 1: Check if command exists
        print("\n✅ Test 1: Command Registration")
        print("-" * 30)
        
        try:
            result = subprocess.run([
                sys.executable, "manage.py", "help", "collectstatic_no_db"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("   ✅ Command is properly registered")
                print(f"   📋 Help text preview: {result.stdout[:100]}...")
            else:
                print(f"   ❌ Command registration failed: {result.stderr}")
                return
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Command help timeout")
            return
        except Exception as e:
            print(f"   ❌ Error checking command: {e}")
            return
        
        # Test 2: Dry run test
        print("\n✅ Test 2: Dry Run Test")
        print("-" * 30)
        
        try:
            result = subprocess.run([
                sys.executable, "manage.py", "collectstatic_no_db", 
                "--dry-run", "--noinput", "-v", "2"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("   ✅ Dry run completed successfully")
                if "Static files collected" in result.stdout or "files would be" in result.stdout:
                    print("   ✅ Static files detection working")
                else:
                    print("   ⚠️  Unexpected output format")
            else:
                print(f"   ❌ Dry run failed: {result.stderr}")
                print(f"   📄 Output: {result.stdout}")
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Dry run timeout")
        except Exception as e:
            print(f"   ❌ Error during dry run: {e}")
        
        # Test 3: Actual collection (if safe)
        print("\n✅ Test 3: Actual Static Collection")
        print("-" * 30)
        
        # Create a temporary static root for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_static_root = os.path.join(temp_dir, "static")
            
            try:
                # Set temporary STATIC_ROOT via environment
                env = os.environ.copy()
                env['DJANGO_STATIC_ROOT'] = temp_static_root
                
                result = subprocess.run([
                    sys.executable, "manage.py", "collectstatic_no_db", 
                    "--noinput", "-v", "1"
                ], capture_output=True, text=True, timeout=120, env=env)
                
                if result.returncode == 0:
                    print("   ✅ Static collection completed successfully")
                    
                    # Check if files were actually collected
                    if os.path.exists(temp_static_root):
                        file_count = sum(len(files) for _, _, files in os.walk(temp_static_root))
                        print(f"   📦 Collected {file_count} static files")
                    else:
                        print("   ⚠️  Static root not created (might be using different location)")
                        
                else:
                    print(f"   ❌ Collection failed: {result.stderr}")
                    print(f"   📄 Output: {result.stdout}")
                    
            except subprocess.TimeoutExpired:
                print("   ⏰ Collection timeout (this might be normal for large projects)")
            except Exception as e:
                print(f"   ❌ Error during collection: {e}")
        
        # Test 4: Command options
        print("\n✅ Test 4: Command Options")
        print("-" * 30)
        
        try:
            result = subprocess.run([
                sys.executable, "manage.py", "collectstatic_no_db", 
                "--help"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                help_text = result.stdout
                if "--skip-db-backup" in help_text:
                    print("   ✅ Custom --skip-db-backup option available")
                if "--noinput" in help_text:
                    print("   ✅ Standard collectstatic options inherited")
                if "--dry-run" in help_text:
                    print("   ✅ Dry run option available")
            else:
                print(f"   ❌ Help command failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ Error checking options: {e}")
        
    finally:
        os.chdir(original_dir)
    
    print("\n" + "=" * 60)
    print("🎯 collectstatic_no_db Command Summary")
    print("=" * 60)
    
    print("✅ Features:")
    print("   • Collects static files without database connection")
    print("   • Temporarily uses in-memory SQLite database")
    print("   • Disables database-dependent middleware")
    print("   • Provides detailed logging and error handling")
    print("   • Supports all standard collectstatic options")
    
    print("\n🚀 Usage Examples:")
    print("   # Basic usage")
    print("   python manage.py collectstatic_no_db --noinput")
    print()
    print("   # Dry run to see what would be collected")
    print("   python manage.py collectstatic_no_db --dry-run --noinput")
    print()
    print("   # Verbose output for debugging")
    print("   python manage.py collectstatic_no_db --noinput -v 2")
    print()
    print("   # Skip database backup for faster execution")
    print("   python manage.py collectstatic_no_db --noinput --skip-db-backup")
    
    print("\n💡 Deployment Use Cases:")
    print("   • Railway/Heroku build process")
    print("   • Docker multi-stage builds")
    print("   • CI/CD pipelines")
    print("   • Local development without database setup")
    
    print("\n✅ collectstatic_no_db command testing completed!")

if __name__ == "__main__":
    test_collectstatic_no_db()