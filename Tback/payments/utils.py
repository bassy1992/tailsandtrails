import uuid
import string
import random
from typing import Dict, Any
from django.utils import timezone

def generate_payment_reference() -> str:
    """Generate a unique payment reference"""
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"PAY-{timestamp}-{random_part}"

def generate_payment_id() -> str:
    """Generate a unique payment ID"""
    return str(uuid.uuid4())

def format_phone_number(phone_number: str, country_code: str = '+233') -> str:
    """Format phone number with country code (default Ghana +233)"""
    if not phone_number:
        return phone_number
    
    # Remove any spaces, dashes, or parentheses
    cleaned = ''.join(filter(str.isdigit, phone_number))
    
    # If it starts with 0, replace with country code
    if cleaned.startswith('0'):
        cleaned = country_code[1:] + cleaned[1:]
    
    # Add + if not present
    if not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    return cleaned

def validate_payment_amount(amount: float, currency: str = 'GHS') -> Dict[str, Any]:
    """Validate payment amount based on currency"""
    validation_rules = {
        'GHS': {'min': 1, 'max': 50000},  # Ghana Cedis
        'KES': {'min': 1, 'max': 1000000},  # Kenya Shillings
        'USD': {'min': 0.01, 'max': 10000},
        'EUR': {'min': 0.01, 'max': 10000},
    }
    
    rules = validation_rules.get(currency, {'min': 0.01, 'max': 1000000})
    
    if amount < rules['min']:
        return {
            'valid': False,
            'message': f'Minimum amount for {currency} is {rules["min"]}'
        }
    
    if amount > rules['max']:
        return {
            'valid': False,
            'message': f'Maximum amount for {currency} is {rules["max"]}'
        }
    
    return {'valid': True}

def get_payment_method_config(payment_method: str) -> Dict[str, Any]:
    """Get configuration for payment method"""
    configs = {
        'momo': {
            'requires_phone': True,
            'supported_currencies': ['GHS', 'KES', 'UGX', 'TZS'],
            'processing_time': '1-5 minutes'
        },
        'mobile_money': {  # Alias for momo
            'requires_phone': True,
            'supported_currencies': ['GHS', 'KES', 'UGX', 'TZS'],
            'processing_time': '1-5 minutes'
        },
        'bank_transfer': {
            'requires_phone': False,
            'supported_currencies': ['GHS', 'KES', 'USD', 'EUR'],
            'processing_time': '1-3 business days'
        },
        'card': {
            'requires_phone': False,
            'supported_currencies': ['GHS', 'USD', 'EUR'],
            'processing_time': 'Instant'
        }
    }
    
    return configs.get(payment_method, {})

def calculate_payment_fees(amount: float, payment_method: str, currency: str = 'GHS') -> Dict[str, Any]:
    """Calculate payment processing fees"""
    fee_structures = {
        'momo': {
            'GHS': {
                'type': 'tiered',
                'tiers': [
                    {'min': 1, 'max': 100, 'fee': 0},
                    {'min': 101, 'max': 500, 'fee': 2},
                    {'min': 501, 'max': 1000, 'fee': 5},
                    {'min': 1001, 'max': 5000, 'fee': 10},
                    {'min': 5001, 'max': float('inf'), 'fee': 20}
                ]
            }
        },
        'mobile_money': {  # Alias for momo
            'GHS': {
                'type': 'tiered',
                'tiers': [
                    {'min': 1, 'max': 100, 'fee': 0},
                    {'min': 101, 'max': 500, 'fee': 2},
                    {'min': 501, 'max': 1000, 'fee': 5},
                    {'min': 1001, 'max': 5000, 'fee': 10},
                    {'min': 5001, 'max': float('inf'), 'fee': 20}
                ]
            },
            'KES': {
                'type': 'tiered',
                'tiers': [
                    {'min': 1, 'max': 100, 'fee': 0},
                    {'min': 101, 'max': 500, 'fee': 5},
                    {'min': 501, 'max': 1000, 'fee': 10},
                    {'min': 1001, 'max': 5000, 'fee': 15},
                    {'min': 5001, 'max': float('inf'), 'fee': 25}
                ]
            }
        },
        'card': {
            'GHS': {'type': 'percentage', 'rate': 0.035, 'min_fee': 2},
            'KES': {'type': 'percentage', 'rate': 0.035, 'min_fee': 10},
            'USD': {'type': 'percentage', 'rate': 0.029, 'min_fee': 0.30},
            'EUR': {'type': 'percentage', 'rate': 0.029, 'min_fee': 0.30}
        },
        'bank_transfer': {
            'GHS': {'type': 'flat', 'fee': 5},
            'KES': {'type': 'flat', 'fee': 50},
            'USD': {'type': 'flat', 'fee': 1.00},
            'EUR': {'type': 'flat', 'fee': 1.00}
        }
    }
    
    method_config = fee_structures.get(payment_method, {})
    currency_config = method_config.get(currency, {})
    
    if not currency_config:
        return {'fee': 0, 'total': amount}
    
    fee_type = currency_config.get('type')
    
    if fee_type == 'flat':
        fee = currency_config.get('fee', 0)
    elif fee_type == 'percentage':
        rate = currency_config.get('rate', 0)
        min_fee = currency_config.get('min_fee', 0)
        fee = max(amount * rate, min_fee)
    elif fee_type == 'tiered':
        fee = 0
        for tier in currency_config.get('tiers', []):
            if tier['min'] <= amount <= tier['max']:
                fee = tier['fee']
                break
    else:
        fee = 0
    
    return {
        'fee': round(fee, 2),
        'total': round(amount + fee, 2)
    }

def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Mask sensitive data in logs and responses"""
    sensitive_keys = [
        'password', 'token', 'secret', 'key', 'authorization',
        'phone_number', 'account_number', 'card_number'
    ]
    
    masked_data = data.copy()
    
    for key, value in masked_data.items():
        if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
            if isinstance(value, str) and len(value) > 4:
                masked_data[key] = value[:2] + '*' * (len(value) - 4) + value[-2:]
            else:
                masked_data[key] = '***'
        elif isinstance(value, dict):
            masked_data[key] = mask_sensitive_data(value)
    
    return masked_data