"""
Django signals for automatic booking details storage and booking creation
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Payment
import logging

logger = logging.getLogger(__name__)

def format_booking_details_for_admin(booking_details):
    """Format booking details in a more readable format for admin logs"""
    try:
        if not booking_details:
            return "No booking details"
        
        # Extract key information
        booking_data = booking_details.get('bookingData', {})
        selected_addons = booking_details.get('selectedAddOns', [])
        
        # Format the main booking info
        formatted = {
            "📋 BOOKING SUMMARY": {
                "Tour": booking_data.get('tourName', 'N/A'),
                "Duration": booking_data.get('duration', 'N/A'),
                "Date": booking_details.get('selectedDate', 'N/A'),
                "Travelers": f"{booking_data.get('travelers', {}).get('adults', 0)} adults, {booking_data.get('travelers', {}).get('children', 0)} children"
            },
            "💰 PRICING": {
                "Base Price": f"GH₵{booking_details.get('baseTotal', 0)}",
                "Add-ons Total": f"GH₵{booking_details.get('addonTotal', 0)}",
                "Final Total": f"GH₵{booking_data.get('totalPrice', booking_details.get('baseTotal', 0))}"
            }
        }
        
        # Add selected add-ons if any
        if selected_addons:
            formatted["🎁 SELECTED ADD-ONS"] = {}
            for addon in selected_addons:
                addon_name = addon.get('name', 'Unknown Add-on')
                addon_price = addon.get('total_price', 0)
                formatted["🎁 SELECTED ADD-ONS"][addon_name] = f"GH₵{addon_price}"
        
        # Format as readable string
        result = []
        for section, content in formatted.items():
            result.append(f"\n{section}:")
            if isinstance(content, dict):
                for key, value in content.items():
                    result.append(f"  • {key}: {value}")
            else:
                result.append(f"  {content}")
        
        return "\n".join(result)
        
    except Exception as e:
        # Fallback to original format if formatting fails
        import json
        return f"Formatting error: {str(e)}\nOriginal data: {json.dumps(booking_details, indent=2)}"

@receiver(post_save, sender=Payment)
def add_booking_details_to_payment(sender, instance, created, **kwargs):
    """
    Automatically add appropriate booking details to newly created payments
    """
    if created:
        # First, ensure phone number is set from user if not already present
        if not instance.phone_number and instance.user and hasattr(instance.user, 'phone_number') and instance.user.phone_number:
            instance.phone_number = instance.user.phone_number
            instance.save(update_fields=['phone_number'])
            logger.info(f"Auto-added phone number {instance.phone_number} to payment {instance.reference}")
        
        # Then add booking details if not present
        if not instance.metadata or 'booking_details' not in instance.metadata:
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
                    
                    # Use actual phone number - prioritize payment phone, fallback to user phone
                    phone = instance.phone_number or (instance.user.phone_number if instance.user and hasattr(instance.user, 'phone_number') else '') or ''
                    if phone:
                        sample_data['user_phone'] = phone
                    
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
        
        # Get phone number - prioritize payment phone, fallback to user phone
        phone = payment.phone_number or (payment.user.phone_number if hasattr(payment.user, 'phone_number') else '') or ''
        
        user_info = {
            'name': user_name,
            'email': payment.user.email or '',
            'phone': phone
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


@receiver(pre_save, sender=Payment)
def track_payment_status_change(sender, instance, **kwargs):
    """Track when payment status changes to successful"""
    if instance.pk:  # Only for existing payments
        try:
            old_payment = Payment.objects.get(pk=instance.pk)
            instance._old_status = old_payment.status
        except Payment.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Payment)
def create_booking_on_successful_payment(sender, instance, created, **kwargs):
    """Create booking and send confirmation email when payment becomes successful"""
    if not created and hasattr(instance, '_old_status'):
        # Check if payment status changed to successful
        if (instance._old_status != 'successful' and 
            instance.status == 'successful'):
            
            try:
                from .booking_details_utils import create_booking_from_payment, create_ticket_purchase_from_payment
                from .email_service import EmailService
                
                # Get booking details from metadata
                booking_details = instance.metadata.get('booking_details', {}) if instance.metadata else {}
                booking_type = booking_details.get('type', 'destination')
                
                # Determine if this is a ticket or destination booking
                is_ticket = (
                    booking_type == 'ticket' or
                    (instance.description and any(word in instance.description.lower() for word in ['ticket', 'event', 'concert', 'festival']))
                )
                
                if is_ticket:
                    # Create ticket purchase if not already exists
                    from tickets.models import TicketPurchase
                    existing_purchase = TicketPurchase.objects.filter(payment_reference=instance.reference).first()
                    
                    if not existing_purchase:
                        ticket_purchase = create_ticket_purchase_from_payment(instance)
                        if ticket_purchase:
                            logger.info(f"Auto-created ticket purchase {ticket_purchase.purchase_id} for successful payment {instance.reference}")
                            
                            # Send ticket confirmation email
                            try:
                                email_sent = EmailService.send_ticket_confirmation(ticket_purchase)
                                if email_sent:
                                    logger.info(f"Ticket confirmation email sent for payment {instance.reference}")
                                    instance.log('info', 'Ticket confirmation email sent', {'purchase_id': str(ticket_purchase.purchase_id)})
                                else:
                                    logger.warning(f"Failed to send ticket confirmation email for payment {instance.reference}")
                                    instance.log('warning', 'Failed to send ticket confirmation email')
                            except Exception as email_error:
                                logger.error(f"Error sending ticket confirmation email for payment {instance.reference}: {str(email_error)}")
                                instance.log('error', f'Error sending ticket confirmation email: {str(email_error)}')
                        else:
                            logger.warning(f"Failed to create ticket purchase for successful payment {instance.reference}")
                            instance.log('warning', 'Failed to create ticket purchase - no valid ticket details found')
                    else:
                        logger.info(f"Ticket purchase already exists for payment {instance.reference}")
                else:
                    # Create destination booking if not already exists
                    if not instance.booking:
                        booking = create_booking_from_payment(instance)
                        if booking:
                            logger.info(f"Auto-created booking {booking.booking_reference} for successful payment {instance.reference}")
                            
                            # Send booking confirmation email
                            try:
                                email_sent = EmailService.send_booking_confirmation(instance, booking_details)
                                if email_sent:
                                    logger.info(f"Booking confirmation email sent for payment {instance.reference}")
                                    instance.log('info', 'Booking confirmation email sent', {'booking_reference': booking.booking_reference})
                                else:
                                    logger.warning(f"Failed to send booking confirmation email for payment {instance.reference}")
                                    instance.log('warning', 'Failed to send booking confirmation email')
                            except Exception as email_error:
                                logger.error(f"Error sending booking confirmation email for payment {instance.reference}: {str(email_error)}")
                                instance.log('error', f'Error sending booking confirmation email: {str(email_error)}')
                        else:
                            logger.warning(f"Failed to create booking for successful payment {instance.reference} - no valid booking details found")
                            instance.log('warning', 'Failed to create booking - no valid booking details found')
                            
                            # Still try to send a generic confirmation email
                            try:
                                email_sent = EmailService.send_booking_confirmation(instance, booking_details)
                                if email_sent:
                                    logger.info(f"Generic confirmation email sent for payment {instance.reference}")
                                    instance.log('info', 'Generic confirmation email sent')
                            except Exception as email_error:
                                logger.error(f"Error sending generic confirmation email for payment {instance.reference}: {str(email_error)}")
                    else:
                        logger.info(f"Booking already exists for payment {instance.reference}")
                    
            except Exception as e:
                logger.error(f"Error processing successful payment {instance.reference}: {str(e)}")
                instance.log('error', f'Error processing successful payment: {str(e)}')
        
        # Clean up the temporary attribute
        if hasattr(instance, '_old_status'):
            delattr(instance, '_old_status')