import requests
import json

def complete_payment(reference, status='successful'):
    """Complete a payment via API"""
    url = f'http://localhost:8000/api/payments/{reference}/complete/'
    
    data = {'status': status}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def force_complete_payment(reference, status='successful'):
    """Force complete a payment via API"""
    url = f'http://localhost:8000/api/payments/{reference}/force-complete/'
    
    data = {'status': status}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_payment_status(reference):
    """Check payment status"""
    url = f'http://localhost:8000/api/payments/{reference}/status/'
    
    try:
        response = requests.get(url)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Payment Status: {result.get('status', 'Unknown')}")
        print(f"Amount: {result.get('currency', '')} {result.get('amount', '')}")
        print(f"Created: {result.get('created_at', '')}")
        print(f"Processed: {result.get('processed_at', 'Not processed')}")
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Test with the payment reference from your issue
    reference = "PAY-20250826213643-67HJE2"
    
    print("=== Checking Payment Status ===")
    check_payment_status(reference)
    
    print("\n=== Testing Payment Completion ===")
    # This should show it's already completed
    complete_payment(reference)
    
    print("\n=== Available Commands ===")
    print("1. Check status: check_payment_status('REFERENCE')")
    print("2. Complete payment: complete_payment('REFERENCE', 'successful')")
    print("3. Force complete: force_complete_payment('REFERENCE', 'successful')")
    print("4. Fail payment: complete_payment('REFERENCE', 'failed')")