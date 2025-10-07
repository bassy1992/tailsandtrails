"""
Django signals for automatic booking details storage
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Payment)
def add_booking_details_to_payment(sender, instance, created, **kwargs):
    """
    Automatically add appropriate booking details to newly created payments
    """
    if created and (not instance.metadata or 'booking_details' not in instance.metadata):
        try:
            # Check if this is a ticket payment
            is_ticket_payment = (
                instance.description and "Ticket Purchase:" in instance.description
            )
            
            if is_ticket_payment:
                # Create ticket-specific details
                store_ticket_details_in_payment(instance)
                logger.info(f"Auto-added ticket details to payment {instance.reference} via signal")
            else:
                # Create destination booking details for non-ticket payments
                from .booking_utils import store_booking_details_in_payment, create_sample_booking_details
                
                sample_data = create_sample_booking_details()
                sample_data['final_total'] = float(instance.amount)
                sample_data['base_total'] = float(instance.amount) * 0.65
                sample_data['options_total'] = float(instance.amount) * 0.35
                
                # Customize based on amount
                amount = float(instance.amount) if instance.amount else 0
                if amount <= 50:
                    sample_data['destination_name'] = 'Local Cultural Experience'
                    sample_data['destination_location'] = 'Accra, Ghana'
                    sample_data['duration'] = '1 Day'
                    sample_data['adults'] = 1
                    sample_data['children'] = 0
                elif amount <= 150:
                    sample_data['destination_name'] = 'Kakum National Park Adventure'
                    sample_data['destination_location'] = 'Central Region, Ghana'
                    sample_data['duration'] = '2 Days / 1 Night'
                    sample_data['adults'] = 2
                    sample_data['children'] = 0
                else:
                    sample_data['destination_name'] = 'Cape Coast Castle Heritage Tour'
                    sample_data['destination_location'] = 'Cape Coast, Ghana'
                    sample_data['duration'] = '3 Days / 2 Nights'
                    sample_data['adults'] = 2
                    sample_data['children'] = 1
                
                # Use actual user info if available
                if instance.user:
                    user_name = f"{instance.user.first_name} {instance.user.last_name}".strip()
                    if not user_name:
                        user_name = instance.user.username or "User"
                    sample_data['user_name'] = user_name
                    sample_data['user_email'] = instance.user.email or ''
                
                # Use actual phone number if available
                if instance.phone_number:
                    sample_data['user_phone'] = instance.phone_number
                
                # Store the booking details
                store_booking_details_in_payment(instance, sample_data)
                logger.info(f"Auto-added destination booking details to payment {instance.reference} via signal")
            
        except Exception as e:
            logger.error(f"Failed to auto-add booking details to payment {instance.reference}: {str(e)}")


def store_ticket_details_in_payment(payment):
    """
    Store ticket-specific details in payment metadata for display in admin
    
    Args:
        payment: Payment instance for a ticket purchase
    """
    if not payment.metadata:
        payment.metadata = {}
    
    # Get user information
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
        user_info = {
            'name': 'Anonymous User',
            'email': '',
            'phone': payment.phone_number or ''
        }
    
    # Extract ticket name from description if available
    ticket_name = "Event Ticket"
    if payment.description and "Ticket Purchase:" in payment.description:
        ticket_name = payment.description.replace("Ticket Purchase:", "").strip()
    
    # Create ticket-specific booking details
    ticket_details = {
        'type': 'ticket',
        'user_info': user_info,
        'ticket': {
            'name': ticket_name,
            'price': float(payment.amount),
            'currency': payment.currency,
            'quantity': 1  # Default to 1, could be enhanced later
        },
        'purchase_info': {
            'purchase_date': payment.created_at.isoformat() if payment.created_at else '',
            'payment_method': payment.payment_method or '',
            'total_amount': float(payment.amount)
        }
    }
    
    # Store in payment metadata
    payment.metadata['booking_details'] = ticket_details
    payment.save()