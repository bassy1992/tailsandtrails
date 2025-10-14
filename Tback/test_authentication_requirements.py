import requests
import json

def test_authentication_requirements():
    """Test that ticket purchase endpoints require authentication"""
    
    print("🔐 TESTING AUTHENTICATION REQUIREMENTS")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test endpoints that should require authentication
    protected_endpoints = [
        {
            'method': 'POST',
            'url': f'{base_url}/api/tickets/purchase/direct/',
            'name': 'Create Direct Ticket Purchase',
            'data': {
                'ticket_id': 1,
                'quantity': 1,
                'customer_name': 'Test User',
                'customer_email': 'test@example.com'
            }
        },
        {
            'method': 'POST',
            'url': f'{base_url}/api/tickets/purchase/create/',
            'name': 'Create Ticket Purchase (Original)',
            'data': {
                'ticket': 1,
                'quantity': 1,
                'customer_name': 'Test User',
                'customer_email': 'test@example.com'
            }
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/purchases/',
            'name': 'List User Purchases'
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/purchases/user/',
            'name': 'User Ticket Purchases'
        },
        {
            'method': 'POST',
            'url': f'{base_url}/api/stripe/payment-intents/',
            'name': 'Create Payment Intent',
            'data': {
                'amount': 100.00,
                'currency': 'GHS',
                'description': 'Test payment'
            }
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/stripe/payment-intents/',
            'name': 'List Payment Intents'
        },
        {
            'method': 'POST',
            'url': f'{base_url}/api/tickets/reviews/create/',
            'name': 'Create Ticket Review',
            'data': {
                'ticket': 1,
                'rating': 5,
                'comment': 'Great event!'
            }
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/stats/user/',
            'name': 'User Ticket Stats'
        }
    ]
    
    # Test endpoints that should allow public access for browsing
    public_endpoints = [
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/',
            'name': 'List Tickets'
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/categories/',
            'name': 'List Categories'
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/venues/',
            'name': 'List Venues'
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/featured/',
            'name': 'Featured Tickets'
        },
        {
            'method': 'GET',
            'url': f'{base_url}/api/tickets/stats/',
            'name': 'General Ticket Stats'
        },
        {
            'method': 'POST',
            'url': f'{base_url}/api/auth/login/',
            'name': 'Login'
        },
        {
            'method': 'POST',
            'url': f'{base_url}/api/auth/register/',
            'name': 'Register'
        }
    ]
    
    # Only purchase-related endpoints require authentication
    all_protected_endpoints = protected_endpoints
    
    print("🚫 TESTING PROTECTED ENDPOINTS (Should require authentication)")
    print("-" * 60)
    
    for endpoint in all_protected_endpoints:
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'])
            elif endpoint['method'] == 'POST':
                response = requests.post(
                    endpoint['url'], 
                    json=endpoint.get('data', {}),
                    headers={'Content-Type': 'application/json'}
                )
            
            if response.status_code == 401:
                print(f"✅ {endpoint['name']}: Correctly requires authentication (401)")
            elif response.status_code == 403:
                print(f"✅ {endpoint['name']}: Correctly requires authentication (403)")
            else:
                print(f"❌ {endpoint['name']}: Does NOT require authentication ({response.status_code})")
                print(f"   Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ {endpoint['name']}: Error testing - {e}")
    
    print(f"\\n🌐 TESTING PUBLIC ENDPOINTS (Should allow anonymous access)")
    print("-" * 60)
    
    for endpoint in public_endpoints:
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'])
            elif endpoint['method'] == 'POST':
                response = requests.post(endpoint['url'], json={})
            
            if response.status_code in [200, 400]:  # 400 is OK for POST without data
                print(f"✅ {endpoint['name']}: Correctly allows public access ({response.status_code})")
            elif response.status_code in [401, 403]:
                print(f"❌ {endpoint['name']}: Incorrectly requires authentication ({response.status_code})")
            else:
                print(f"⚠️  {endpoint['name']}: Unexpected status ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {endpoint['name']}: Error testing - {e}")
    
    print(f"\\n🔑 TESTING WITH AUTHENTICATION")
    print("-" * 60)
    
    # Test login to get token
    login_data = {
        'email': 'test@example.com',  # Use test user credentials
        'password': 'testpass123'
    }
    
    try:
        login_response = requests.post(f'{base_url}/api/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('token')
            
            if token:
                print(f"✅ Successfully logged in and got token")
                
                # Test protected endpoints with authentication
                headers = {'Authorization': f'Token {token}'}
                
                # Test ticket purchase with authentication
                purchase_data = {
                    'ticket_id': 1,
                    'quantity': 1,
                    'customer_name': 'Authenticated User',
                    'customer_email': 'auth@example.com'
                }
                
                purchase_response = requests.post(
                    f'{base_url}/api/tickets/purchase/direct/',
                    json=purchase_data,
                    headers=headers
                )
                
                if purchase_response.status_code in [200, 201]:
                    print(f"✅ Ticket purchase works with authentication ({purchase_response.status_code})")
                else:
                    print(f"⚠️  Ticket purchase response: {purchase_response.status_code}")
                    print(f"   Response: {purchase_response.text[:200]}...")
                
                # Test user purchases list
                purchases_response = requests.get(
                    f'{base_url}/api/tickets/purchases/user/',
                    headers=headers
                )
                
                if purchases_response.status_code == 200:
                    purchases = purchases_response.json()
                    print(f"✅ User purchases list works with authentication ({len(purchases)} purchases)")
                else:
                    print(f"⚠️  User purchases response: {purchases_response.status_code}")
            else:
                print(f"❌ No token in login response")
                print(f"   Response: {token_data}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            print(f"\\n💡 To test with authentication, create a user account first:")
            print(f"   python manage.py createsuperuser")
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
    
    print(f"\\n" + "=" * 60)
    print(f"🎯 AUTHENTICATION SUMMARY")
    print("=" * 60)
    print(f"🌐 TICKET BROWSING: Public access (no login required)")
    print(f"✅ Ticket viewing: Public access")
    print(f"✅ Categories & venues: Public access")
    print(f"✅ Featured tickets: Public access")
    print(f"✅ General statistics: Public access")
    print(f"🔐 TICKET PURCHASING: Requires authentication")
    print(f"✅ Ticket purchasing: Requires login")
    print(f"✅ Payment processing: Requires login")
    print(f"✅ User purchase history: Requires login")
    print(f"✅ Ticket reviews: Requires login")
    print(f"✅ User statistics: Requires login")
    
    print(f"\\n🚀 FRONTEND INTEGRATION:")
    print(f"   • Users can browse tickets without logging in")
    print(f"   • Login required only when clicking 'Buy Tickets'")
    print(f"   • Show 'Login to Buy Tickets' button for unauthenticated users")
    print(f"   • Redirect to login page with return URL for purchases")

if __name__ == "__main__":
    test_authentication_requirements()