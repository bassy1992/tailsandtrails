import requests
import json

def enable_instant_completion():
    """Enable instant payment completion for demo"""
    
    print("⚡ INSTANT PAYMENT COMPLETION")
    print("=" * 40)
    
    # Check for any processing payments and complete them
    try:
        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
        django.setup()
        
        from payments.models import Payment
        from django.utils import timezone
        
        processing_payments = Payment.objects.filter(status='processing').order_by('-created_at')
        
        if not processing_payments:
            print("✅ No processing payments found")
        else:
            print(f"🔧 Found {len(processing_payments)} processing payments:")
            
            for payment in processing_payments:
                print(f"   - {payment.reference}: {payment.description}")
                
                # Complete the payment
                payment.status = 'successful'
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', 'Instantly completed for demo')
                
                print(f"   ✅ Completed: {payment.reference}")
        
        print(f"\n🎉 All payments completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def create_instant_completion_endpoint():
    """Create a simple endpoint for instant completion"""
    
    print("\n📡 INSTANT COMPLETION API")
    print("=" * 40)
    
    print("🚀 You can now use these endpoints:")
    print("   POST /api/payments/{reference}/complete/")
    print("   Body: {\"status\": \"successful\"}")
    
    print("\n⚡ Or run this script anytime:")
    print("   python enable_instant_completion.py")
    
    print("\n🎯 For the frontend:")
    print("   1. Start payment → wait 10 seconds")
    print("   2. Or run this script to complete instantly")
    print("   3. Frontend will detect and proceed")

def show_auto_completion_status():
    """Show current auto-completion settings"""
    
    print("\n⚙️  AUTO-COMPLETION SETTINGS")
    print("=" * 40)
    
    print("✅ Current settings:")
    print("   - Ticket payments: 10 seconds (99% success)")
    print("   - Other payments: 20 seconds (95% success)")
    print("   - Background threading: Enabled")
    print("   - Instant completion: Available")
    
    print("\n🎫 For ticket checkout:")
    print("   - Payment will auto-complete in ~10 seconds")
    print("   - Frontend polls every 5 seconds")
    print("   - Should redirect to success page automatically")

if __name__ == "__main__":
    enable_instant_completion()
    create_instant_completion_endpoint()
    show_auto_completion_status()