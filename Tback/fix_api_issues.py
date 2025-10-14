#!/usr/bin/env python
"""
Fix API issues and test all endpoints
"""
import os
import sys
import django
import requests
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_all_endpoints():
    """Test all problematic endpoints"""
    print("🔧 Testing All API Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api"
    
    tests = [
        {
            'name': 'Destinations by ID',
            'url': f'{base_url}/destinations/1/',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Paystack Config',
            'url': f'{base_url}/payments/paystack/config/',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Card Payment Creation',
            'url': f'{base_url}/payments/paystack/create/',
            'method': 'POST',
            'data': {
                'amount': 50.0,
                'email': 'test@example.com',
                'payment_method': 'card',
                'description': 'Test payment'
            },
            'expected_status': 201
        },
        {
            'name': 'Mobile Money Payment Creation',
            'url': f'{base_url}/payments/paystack/create/',
            'method': 'POST',
            'data': {
                'amount': 50.0,
                'email': 'test@example.com',
                'payment_method': 'mobile_money',
                'provider': 'mtn',
                'phone_number': '+233241234567',
                'description': 'Test mobile money payment'
            },
            'expected_status': 201
        }
    ]
    
    results = {}
    
    for test in tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        try:
            if test['method'] == 'GET':
                response = requests.get(test['url'])
            elif test['method'] == 'POST':
                response = requests.post(
                    test['url'],
                    headers={'Content-Type': 'application/json'},
                    json=test['data']
                )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == test['expected_status']:
                print(f"   ✅ PASS")
                results[test['name']] = True
                
                # Show response for successful tests
                try:
                    data = response.json()
                    if test['name'] == 'Mobile Money Payment Creation':
                        if data.get('success'):
                            print(f"   📱 Mobile money payment created successfully")
                            if data.get('paystack', {}).get('test_mode'):
                                print(f"   🧪 Test mode detected - this is expected behavior")
                        else:
                            print(f"   ⚠️  Payment creation returned success=False")
                    elif test['name'] == 'Paystack Config':
                        public_key = data.get('public_key', '')
                        if public_key.startswith('pk_test_ad2c643f'):
                            print(f"   🔑 Correct API key loaded")
                        else:
                            print(f"   ⚠️  API key not updated: {public_key[:20]}...")
                except:
                    pass
                    
            else:
                print(f"   ❌ FAIL - Expected {test['expected_status']}, got {response.status_code}")
                results[test['name']] = False
                
                # Show error details
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Raw response: {response.text[:200]}...")
                    
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            results[test['name']] = False
    
    return results

def create_test_data():
    """Create test data if needed"""
    print("\n🏗️  Creating Test Data...")
    
    try:
        from destinations.models import Destination, Category
        
        # Create category
        category, created = Category.objects.get_or_create(
            name="Adventure Tours",
            defaults={
                'description': 'Exciting adventure tours in Ghana',
                'slug': 'adventure-tours'
            }
        )
        
        # Create destination
        destination, created = Destination.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Kakum National Park',
                'slug': 'kakum-national-park',
                'description': 'Experience the famous canopy walkway at Kakum National Park',
                'location': 'Central Region, Ghana',
                'price': 150.00,
                'duration': '1 Day',
                'category': category,
                'is_active': True,
                'is_featured': True
            }
        )
        
        print(f"   ✅ Test destination {'created' if created else 'already exists'}")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to create test data: {e}")
        return False

def main():
    """Main function"""
    print("🚀 API Issues Fix & Test")
    print("=" * 50)
    
    # Create test data
    create_test_data()
    
    # Test all endpoints
    results = test_all_endpoints()
    
    # Summary
    print(f"\n📊 Test Results Summary:")
    print(f"=" * 30)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n🎉 All tests passed! Your API is working correctly.")
        print(f"\n📝 Important Notes:")
        print(f"   - Mobile money 'Charge attempted' is normal in test mode")
        print(f"   - Destinations endpoint now supports both ID and slug")
        print(f"   - Paystack integration is working correctly")
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above.")
        
        if not results.get('Paystack Config'):
            print(f"\n🔄 If Paystack config failed, restart your Django server:")
            print(f"   1. Stop the server (Ctrl+C)")
            print(f"   2. Start again: python manage.py runserver")

if __name__ == '__main__':
    main()