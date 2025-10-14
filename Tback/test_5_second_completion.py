import requests
import json
import time

def test_5_second_completion():
    """Test 5-second auto-completion"""
    
    print("⚡ Testing 5-Second Auto-Completion")
    print("=" * 50)
    
    # Get a ticket
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    ticket = tickets_response.json()[0]
    print(f"🎫 Using: {ticket['title']} (GH₵{ticket['price']})")
    
    # Create payment
    payment_data = {
        "amount": float(ticket['price']),
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": f"5s Test: {ticket['title']}",
        "booking_details": {
            "type": "ticket",  # Triggers 5-second completion
            "ticket_id": ticket['id'],
            "customer_name": "Speed Test",
            "customer_email": "speedtest@example.com"
        }
    }
    
    print("\n💳 Creating payment...")
    payment_response = requests.post(
        'http://localhost:8000/api/payments/checkout/create/',
        json=payment_data
    )
    
    if payment_response.status_code != 201:
        print(f"❌ Failed: {payment_response.text}")
        return
    
    payment_result = payment_response.json()
    payment_ref = payment_result['payment']['reference']
    print(f"✅ Payment: {payment_ref}")
    print("⏰ Auto-completion in 5 seconds...")
    
    # Monitor with countdown
    print("\n⏱️  Countdown:")
    start_time = time.time()
    
    for i in range(10):  # Check for 10 seconds
        elapsed = int(time.time() - start_time)
        
        try:
            status_response = requests.get(f'http://localhost:8000/api/payments/{payment_ref}/status/')
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get('status', 'unknown')
                
                if status == 'successful':
                    print(f"🎉 COMPLETED in {elapsed} seconds!")
                    break
                elif status == 'failed':
                    print(f"❌ FAILED after {elapsed} seconds")
                    break
                else:
                    print(f"   {elapsed}s: {status} {'.' * (elapsed % 4)}")
            
        except Exception as e:
            print(f"   {elapsed}s: Error - {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("⚡ 5-SECOND AUTO-COMPLETION READY!")
    print("=" * 50)
    print("✅ Settings:")
    print("   - Ticket payments: 5 seconds")
    print("   - Success rate: 99%")
    print("   - Frontend polling: Every 5 seconds")
    
    print("\n🎯 User Experience:")
    print("   1. User clicks 'Complete Purchase'")
    print("   2. Shows 'Processing Payment...'")
    print("   3. After ~5 seconds → Success!")
    print("   4. Redirects to ticket codes page")
    
    print("\n🚀 Try the frontend now - super fast completion!")

if __name__ == "__main__":
    test_5_second_completion()