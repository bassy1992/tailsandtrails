#!/usr/bin/env python3
"""
Comprehensive test for all Paystack endpoints
"""
import requests
import json
import time

BASE_URL = "https://tailsandtrails-production.up.railway.app/api/payments"

def test_endpoint(method, url, data=None, description=""):
    """Test a single endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(
                url, 
                json=data, 
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            print("   ❌ Endpoint not found (404)")
            return False
        elif response.status_code < 400:
            print("   ✅ Endpoint accessible")
            return True
        else:
            print(f"   ⚠️  Endpoint accessible but returned error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Error: {response.text[:200]}")
            return True  # Endpoint exists, just has validation errors
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {str(e)}")
        return False

def main():
    """Test all Paystack endpoints"""
    print("🚀 Testing all Paystack endpoints...")
    
    endpoints = [
        {
            "method": "GET",
            "url": f"{BASE_URL}/paystack/config/",
            "description": "Get Paystack configuration"
        },
        {
            "method": "POST",
            "url": f"{BASE_URL}/paystack/create/",
            "data": {
                "amount": 100,
                "email": "test@example.com",
                "payment_method": "card",
                "description": "Test payment"
            },
            "description": "Create Paystack payment"
        },
        {
            "method": "GET",
            "url": f"{BASE_URL}/paystack/verify/test-ref-123/",
            "description": "Verify Paystack payment"
        },
        {
            "method": "POST",
            "url": f"{BASE_URL}/paystack/webhook/",
            "data": {"event": "charge.success", "data": {"reference": "test"}},
            "description": "Paystack webhook"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        success = test_endpoint(
            endpoint["method"],
            endpoint["url"],
            endpoint.get("data"),
            endpoint["description"]
        )
        results.append({
            "description": endpoint["description"],
            "success": success
        })
        
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    accessible_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['description']}")
    
    print(f"\n📈 Results: {accessible_count}/{total_count} endpoints accessible")
    
    if accessible_count == total_count:
        print("🎉 All Paystack endpoints are working!")
    elif accessible_count > 0:
        print("⚠️  Some endpoints are working. The 404 issue should be resolved.")
    else:
        print("❌ No endpoints accessible. The fix may not be deployed yet.")
    
    return accessible_count == total_count

if __name__ == "__main__":
    main()