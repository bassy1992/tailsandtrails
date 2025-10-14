import requests
import json

def test_direct_payment():
    """Test payment endpoint directly"""
    
    url = 'http://localhost:8000/api/payments/checkout/create/'
    data = {
        "amount": 80.00,
        "currency": "GHS", 
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Test payment"
    }
    
    print("Testing payment endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                print("✅ Payment created successfully!")
                return result['payment']['reference']
            else:
                print("❌ Payment creation failed")
        else:
            print("❌ HTTP error")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    return None

if __name__ == "__main__":
    test_direct_payment()