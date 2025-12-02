"""
Quick script to check if Paystack provider exists
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import PaymentProvider

print("=" * 60)
print("CHECKING PAYSTACK PROVIDER")
print("=" * 60)

# Check if Paystack provider exists
try:
    paystack = PaymentProvider.objects.get(code='paystack')
    print(f"\n✅ Paystack provider EXISTS")
    print(f"   ID: {paystack.id}")
    print(f"   Name: {paystack.name}")
    print(f"   Code: {paystack.code}")
    print(f"   Is Active: {paystack.is_active}")
    
    if not paystack.is_active:
        print(f"\n⚠️  WARNING: Paystack provider is INACTIVE")
        print(f"   Run: python Tback/setup_paystack_provider.py")
    else:
        print(f"\n✅ Paystack provider is ACTIVE and ready to use")
        
except PaymentProvider.DoesNotExist:
    print(f"\n❌ Paystack provider DOES NOT EXIST")
    print(f"\n   To fix this, run:")
    print(f"   python Tback/setup_paystack_provider.py")
    print(f"\n   Or on Railway:")
    print(f"   railway run python Tback/setup_paystack_provider.py")

# List all providers
print(f"\n" + "=" * 60)
print("ALL PAYMENT PROVIDERS")
print("=" * 60)

all_providers = PaymentProvider.objects.all()
if all_providers.exists():
    for provider in all_providers:
        status = "✅ ACTIVE" if provider.is_active else "❌ INACTIVE"
        print(f"\n{status}")
        print(f"   ID: {provider.id}")
        print(f"   Name: {provider.name}")
        print(f"   Code: {provider.code}")
else:
    print(f"\n❌ No payment providers found in database")
    print(f"   Run: python Tback/setup_paystack_provider.py")

print(f"\n" + "=" * 60)
