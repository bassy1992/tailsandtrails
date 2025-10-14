#!/usr/bin/env python
"""
Fix test mode payment handling for better user experience
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
from django.utils import timezone

def create_test_mode_completion_endpoint():
    """Create an endpoint to simulate payment completion in test mode"""
    
    # Create the view file content
    view_content = '''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Payment

@api_view(['POST'])
@permission_classes([AllowAny])
def simulate_test_payment_success(request, reference):
    """Simulate payment success in test mode - for development only"""
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        # Only allow this in test mode (when using test keys)
        from django.conf import settings
        public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
        
        if not public_key.startswith('pk_test_'):
            return Response({
                'success': False,
                'error': 'This endpoint only works with test API keys'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Update payment to successful
        if payment.status in ['processing', 'failed']:
            payment.status = 'successful'
            payment.processed_at = timezone.now()
            payment.save()
            payment.log('info', 'Payment marked as successful via test mode simulation')
            
            return Response({
                'success': True,
                'message': 'Payment marked as successful (test mode)',
                'payment': {
                    'reference': payment.reference,
                    'status': payment.status,
                    'amount': payment.amount,
                    'processed_at': payment.processed_at
                }
            })
        else:
            return Response({
                'success': False,
                'error': f'Payment is already {payment.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''
    
    # Write to payments views
    with open('payments/test_mode_views.py', 'w') as f:
        f.write(view_content)
    
    print("✅ Created test mode completion endpoint")

def update_paystack_views():
    """Update Paystack views to handle test mode better"""
    
    # Read current paystack_views.py
    with open('payments/paystack_views.py', 'r') as f:
        content = f.read()
    
    # Add import for test mode view
    if 'from .test_mode_views import simulate_test_payment_success' not in content:
        # Add the import after existing imports
        import_line = "from .test_mode_views import simulate_test_payment_success"
        
        # Find the last import line
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('from ') or line.startswith('import '):
                last_import_idx = i
        
        # Insert the new import
        lines.insert(last_import_idx + 1, import_line)
        content = '\n'.join(lines)
        
        # Write back
        with open('payments/paystack_views.py', 'w') as f:
            f.write(content)
        
        print("✅ Updated paystack_views.py with test mode import")

def update_urls():
    """Add test mode endpoint to URLs"""
    
    # Read current URLs
    with open('payments/urls.py', 'r') as f:
        content = f.read()
    
    # Add test mode URL if not exists
    test_url = "path('paystack/test-complete/<str:reference>/', paystack_views.simulate_test_payment_success, name='paystack-test-complete'),"
    
    if 'test-complete' not in content:
        # Find the Paystack endpoints section
        lines = content.split('\n')
        
        # Find where to insert (after other Paystack endpoints)
        insert_idx = -1
        for i, line in enumerate(lines):
            if 'paystack/config/' in line:
                insert_idx = i + 1
                break
        
        if insert_idx > 0:
            lines.insert(insert_idx, f"    {test_url}")
            content = '\n'.join(lines)
            
            with open('payments/urls.py', 'w') as f:
                f.write(content)
            
            print("✅ Added test mode URL to payments/urls.py")

def create_frontend_helper():
    """Create a JavaScript helper for test mode"""
    
    js_content = '''
// Test Mode Payment Helper
// Add this to your frontend for easy test mode payment completion

class PaystackTestHelper {
    constructor(baseUrl = 'http://localhost:8000/api/payments') {
        this.baseUrl = baseUrl;
    }
    
    // Complete a payment in test mode
    async completeTestPayment(paymentReference) {
        try {
            const response = await fetch(`${this.baseUrl}/paystack/test-complete/${paymentReference}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Test payment completed:', result);
                return result;
            } else {
                console.error('❌ Test payment completion failed:', result.error);
                return null;
            }
        } catch (error) {
            console.error('❌ Test payment completion error:', error);
            return null;
        }
    }
    
    // Add a test completion button to the page
    addTestCompletionButton(paymentReference, containerId = 'test-controls') {
        const container = document.getElementById(containerId) || document.body;
        
        const button = document.createElement('button');
        button.innerHTML = '🧪 Complete Test Payment';
        button.style.cssText = `
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
            font-size: 14px;
        `;
        
        button.onclick = async () => {
            button.disabled = true;
            button.innerHTML = '⏳ Completing...';
            
            const result = await this.completeTestPayment(paymentReference);
            
            if (result) {
                button.innerHTML = '✅ Completed!';
                button.style.background = '#6c757d';
                
                // Trigger a page refresh or redirect
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                button.innerHTML = '❌ Failed';
                button.style.background = '#dc3545';
                button.disabled = false;
            }
        };
        
        container.appendChild(button);
        return button;
    }
}

// Usage:
// const testHelper = new PaystackTestHelper();
// testHelper.addTestCompletionButton('PAY-20251009202352-Q9J9D0');

// Or manually complete:
// testHelper.completeTestPayment('PAY-20251009202352-Q9J9D0');
'''
    
    with open('paystack_test_helper.js', 'w') as f:
        f.write(js_content)
    
    print("✅ Created paystack_test_helper.js")

def main():
    """Main setup function"""
    print("🔧 Setting up Test Mode Payment Completion")
    print("=" * 50)
    
    try:
        create_test_mode_completion_endpoint()
        update_paystack_views()
        update_urls()
        create_frontend_helper()
        
        print(f"\n🎉 Test Mode Setup Complete!")
        print(f"\n📝 How to Use:")
        print(f"1. Create a payment (it will show as 'failed' in test mode)")
        print(f"2. Use the test completion endpoint:")
        print(f"   POST /api/payments/paystack/test-complete/{{reference}}/")
        print(f"3. Or use the JavaScript helper in your frontend")
        print(f"4. Payment will be marked as 'successful'")
        
        print(f"\n🧪 Test Mode Behavior:")
        print(f"- Paystack test mode doesn't actually process payments")
        print(f"- Payments appear as 'failed' or 'cancelled'")
        print(f"- Use the test completion endpoint to simulate success")
        print(f"- This only works with test API keys (pk_test_...)")
        
        print(f"\n🚀 Production Mode:")
        print(f"- Switch to live Paystack keys (pk_live_...)")
        print(f"- Real payments will work normally")
        print(f"- Test completion endpoint will be disabled")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()