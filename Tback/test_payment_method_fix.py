import requests
import json

def test_payment_method_fix():
    """Test the payment method fix directly"""
    
    print("🔧 TESTING PAYMENT METHOD FIX")
    print("=" * 50)
    
    # Get any available ticket
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    if tickets_response.status_code != 200:
        print("❌ Failed to get tickets")
        return
    
    tickets = tickets_response.json()
    if not tickets:
        print("❌ No tickets available")
        return
    
    ticket = tickets[0]  # Use first available ticket
    print(f"✅ Using ticket: {ticket['title']}")
    print(f"   ID: {ticket['id']}")
    print(f"   Price: GH₵{ticket['price']}")
    
    # Test different payment methods
    payment_methods_to_test = [
        ('mtn_momo', 'Should work'),
        ('mtn_mobile_money', 'Should fail'),
        ('vodafone_cash', 'Should work'),
        ('airteltigo_money', 'Should work'),
        ('stripe', 'Should work'),
        ('invalid_method', 'Should fail')
    ]
    
    for payment_method, expected in payment_methods_to_test:
        print(f"\n🧪 Testing payment method: '{payment_method}' ({expected})")
        print("-" * 40)
        
        purchase_data = {
            "ticket_id": ticket['id'],
            "quantity": 1,
            "total_amount": float(ticket['price']),
            "customer_name": "Payment Method Test",
            "customer_email": "paymenttest@example.com",
            "customer_phone": "+233244123456",
            "payment_method": payment_method,
            "payment_reference": f"TEST-{payment_method.upper()}-123",
            "special_requests": f"Testing payment method: {payment_method}"
        }
        
        response = requests.post(
            'http://localhost:8000/api/tickets/purchase/direct/',
            json=purchase_data
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ SUCCESS: {result.get('message', 'No message')}")
                purchase = result['purchase']
                print(f"      Purchase ID: {purchase['purchase_id']}")
                print(f"      Payment Method: {purchase['payment_method']}")
            else:
                print(f"   ❌ FAILED: {result.get('error', 'Unknown error')}")
        elif response.status_code == 400:
            try:
                error_result = response.json()
                print(f"   ❌ BAD REQUEST: {error_result.get('error', 'Unknown error')}")
            except:
                print(f"   ❌ BAD REQUEST: {response.text}")
        else:
            print(f"   ❌ HTTP ERROR: {response.status_code}")
            print(f"      Response: {response.text}")
    
    print(f"\n" + "=" * 50)
    print(f"🎯 PAYMENT METHOD TEST COMPLETE")
    print(f"=" * 50)
    print(f"✅ Valid methods: mtn_momo, vodafone_cash, airteltigo_money, stripe")
    print(f"❌ Invalid methods: mtn_mobile_money, invalid_method")

if __name__ == "__main__":
    test_payment_method_fix()