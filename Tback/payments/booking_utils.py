"""
Utility functions for handling booking details in payments
"""

def store_booking_details_in_payment(payment, booking_data):
    """
    Store booking details in payment metadata for display in admin
    
    Args:
        payment: Payment instance
        booking_data: Dictionary containing booking information
    """
    if not payment.metadata:
        payment.metadata = {}
    
    # Get user information from payment or booking data
    user_info = {}
    if payment.user:
        user_name = f"{payment.user.first_name} {payment.user.last_name}".strip()
        if not user_name:
            user_name = payment.user.username or "User"
        user_info = {
            'name': user_name,
            'email': payment.user.email or '',
            'phone': payment.phone_number or ''
        }
    else:
        # Use provided user info or defaults
        user_info = {
            'name': booking_data.get('user_name', 'Anonymous User'),
            'email': booking_data.get('user_email', ''),
            'phone': booking_data.get('user_phone', payment.phone_number or '')
        }
    
    # Structure the booking details for easy display
    booking_details = {
        'user_info': user_info,
        'destination': {
            'name': booking_data.get('destination_name', ''),
            'location': booking_data.get('destination_location', ''),
            'duration': booking_data.get('duration', ''),
            'base_price': booking_data.get('base_price', 0)
        },
        'travelers': {
            'adults': booking_data.get('adults', 0),
            'children': booking_data.get('children', 0)
        },
        'selected_date': booking_data.get('selected_date', ''),
        'selected_options': {},
        'pricing': {
            'base_total': booking_data.get('base_total', 0),
            'options_total': booking_data.get('options_total', 0),
            'final_total': booking_data.get('final_total', 0)
        }
    }
    
    # Add selected options
    if 'accommodation' in booking_data:
        booking_details['selected_options']['accommodation'] = {
            'name': booking_data['accommodation'].get('name', ''),
            'price': booking_data['accommodation'].get('price', 0),
            'is_default': booking_data['accommodation'].get('is_default', False)
        }
    
    if 'transport' in booking_data:
        booking_details['selected_options']['transport'] = {
            'name': booking_data['transport'].get('name', ''),
            'price': booking_data['transport'].get('price', 0),
            'is_default': booking_data['transport'].get('is_default', False)
        }
    
    if 'meals' in booking_data:
        booking_details['selected_options']['meals'] = {
            'name': booking_data['meals'].get('name', ''),
            'price': booking_data['meals'].get('price', 0),
            'is_default': booking_data['meals'].get('is_default', False)
        }
    
    if 'medical' in booking_data:
        booking_details['selected_options']['medical'] = {
            'name': booking_data['medical'].get('name', ''),
            'price': booking_data['medical'].get('price', 0),
            'is_default': booking_data['medical'].get('is_default', False)
        }
    
    if 'experiences' in booking_data:
        booking_details['selected_options']['experiences'] = [
            {
                'name': exp.get('name', ''),
                'price': exp.get('price', 0)
            }
            for exp in booking_data['experiences']
        ]
    
    # Store in payment metadata
    payment.metadata['booking_details'] = booking_details
    payment.save()

def create_sample_booking_details():
    """
    Create sample booking details for testing
    """
    return {
        'user_name': 'John Doe',
        'user_email': 'john.doe@example.com',
        'user_phone': '+233244123456',
        'destination_name': 'Cape Coast Castle Heritage Tour',
        'destination_location': 'Cape Coast, Ghana',
        'duration': '3 Days / 2 Nights',
        'base_price': 1500.00,
        'adults': 2,
        'children': 1,
        'selected_date': '2025-09-20',
        'accommodation': {
            'name': 'Premium Hotel',
            'price': 500.00,
            'is_default': False
        },
        'transport': {
            'name': 'Private Van',
            'price': 800.00,
            'is_default': False
        },
        'meals': {
            'name': 'Standard Meals',
            'price': 0.00,
            'is_default': True
        },
        'medical': {
            'name': 'Travel Insurance',
            'price': 200.00,
            'is_default': False
        },
        'experiences': [
            {
                'name': 'Cultural Experience',
                'price': 250.00
            },
            {
                'name': 'Adventure Add-on',
                'price': 400.00
            }
        ],
        'base_total': 4500.00,  # 1500 * 3 people
        'options_total': 2150.00,  # 500*3 + 800 + 200 + 250 + 400
        'final_total': 6650.00
    }