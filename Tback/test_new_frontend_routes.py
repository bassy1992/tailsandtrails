import requests

def test_frontend_routes():
    """Test the new frontend routes"""
    
    print("🧪 Testing Frontend Routes")
    print("=" * 40)
    
    # Test different ports
    ports = [8080, 8081, 8082]
    working_port = None
    
    for port in ports:
        try:
            response = requests.get(f'http://localhost:{port}/', timeout=3)
            if response.status_code == 200:
                working_port = port
                print(f"✅ Frontend running on port {port}")
                break
        except:
            continue
    
    if not working_port:
        print("❌ Frontend not accessible on any port")
        return
    
    base_url = f'http://localhost:{working_port}'
    
    # Test routes
    routes_to_test = [
        ('/', 'Home page'),
        ('/tickets', 'Tickets list'),
        ('/ticket-checkout', 'Ticket checkout'),
        ('/ticket-purchase-success', 'Purchase success')
    ]
    
    print(f"\n📋 Testing routes on {base_url}:")
    
    for route, description in routes_to_test:
        try:
            response = requests.get(f'{base_url}{route}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {route} - {description}: Working")
            else:
                print(f"❌ {route} - {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {route} - {description}: Error - {e}")
    
    print(f"\n🎯 Try visiting: {base_url}/ticket-checkout")
    print(f"🎫 Or start with: {base_url}/tickets")

if __name__ == "__main__":
    test_frontend_routes()