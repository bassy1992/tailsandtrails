#!/usr/bin/env python3
"""
Test the direct ticket purchase endpoint
"""
import requests
import json

def test_direct_ticket_purchase():
    """Test the direct ticket purchase endpoint"""
    print("🎫 Testing Direct Ticket Purchase Endpoint")
    print("=" * 50)
    
    # Test data (similar to what frontend sends)
    test_data = {
        'ticket_id': 2,  # Black Stars vs Nigeria
        'quantity': 1,
        'total_amount': 50,
        'customer_name': 'Test Customer',
        'customer_email': 'test@example.com',
        'customer_phone': '0241234567',
        'payment_method': 'mtn_momo',
        'payment_reference': 'PAY-TEST-12345',
        'special_requests': 'Mobile Money Payment - MTN - 0241234567 - Account: Test Account'
    }
    
    print("📋 Test Data:")
    print(json.dumps(test_data, indent=2))
    print()
    
    try:
        # Test the direct purchase endpoint
        api_url = "http://localhost:8000/api/tickets/purchase/direct/"
        print(f"🌐 Testing endpoint: {api_url}")
        
        response = requests.post(api_url, json=test_data, headers={
            'Content-Type': 'application/json'
        })
        
        print(f"📡 Response Status: {response.status_code}")
        
        try:
            result = response.json()
            print("📋 Response Data:")
            print(json.dumps(result, indent=2))
            
            if result.get('success'):
                print("✅ Direct ticket purchase successful!")
                purchase_id = result.get('purchase', {}).get('purchase_id')
                if purchase_id:
                    print(f"🎫 Purchase ID: {purchase_id}")
                    print(f"💰 Payment Reference: {result.get('payment_reference')}")
            else:
                print(f"❌ Direct ticket purchase failed: {result.get('error')}")
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_direct_ticket_purchase()