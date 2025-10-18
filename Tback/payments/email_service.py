"""
Email service for sending booking and ticket confirmation emails
"""
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending confirmation emails"""
    
    @staticmethod
    def send_booking_confirmation(payment, booking_details=None):
        """Send booking confirmation email"""
        try:
            if not payment.user and not booking_details:
                logger.warning(f"No user or booking details for payment {payment.reference}")
                return False
            
            # Extract customer information
            customer_email = booking_details.get('customer_email') if booking_details else payment.user.email
            customer_name = booking_details.get('customer_name') if booking_details else payment.user.get_full_name()
            customer_phone = booking_details.get('customer_phone', '')
            
            if not customer_email:
                logger.warning(f"No email address for payment {payment.reference}")
                return False
            
            # Prepare email context
            context = {
                'customer_name': customer_name or 'Valued Customer',
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'booking_reference': payment.reference,
                'total_amount': payment.amount,
                'payment_method': EmailService._format_payment_method(payment.payment_method),
                'booking_date': datetime.now().strftime('%B %d, %Y'),
            }
            
            # Add booking-specific details if available
            if booking_details:
                context.update({
                    'tour_name': booking_details.get('tour_name', 'Tour Experience'),
                    'duration': booking_details.get('duration', ''),
                    'travelers_count': booking_details.get('travelers', {}).get('total', 1),
                    'addons': booking_details.get('selected_addons', []),
                })
            
            # Render email templates
            html_message = render_to_string('emails/booking_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            success = send_mail(
                subject=f'Booking Confirmation - {context["tour_name"]} | Tails & Trails',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            if success:
                logger.info(f"Booking confirmation email sent to {customer_email} for payment {payment.reference}")
                return True
            else:
                logger.error(f"Failed to send booking confirmation email for payment {payment.reference}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending booking confirmation email for payment {payment.reference}: {str(e)}")
            return False
    
    @staticmethod
    def send_ticket_confirmation(ticket_purchase):
        """Send ticket confirmation email"""
        try:
            # Get customer information
            customer_email = ticket_purchase.customer_email
            customer_name = ticket_purchase.customer_name
            customer_phone = ticket_purchase.customer_phone
            
            if not customer_email:
                logger.warning(f"No email address for ticket purchase {ticket_purchase.purchase_id}")
                return False
            
            # Get ticket codes
            ticket_codes = ticket_purchase.ticket_codes.all()
            
            # Prepare email context
            context = {
                'customer_name': customer_name or 'Valued Customer',
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'purchase_id': str(ticket_purchase.purchase_id),
                'ticket_title': ticket_purchase.ticket.title,
                'venue': getattr(ticket_purchase.ticket.venue, 'name', '') if ticket_purchase.ticket.venue else '',
                'event_date': ticket_purchase.ticket.event_date.strftime('%B %d, %Y at %I:%M %p') if ticket_purchase.ticket.event_date else '',
                'quantity': ticket_purchase.quantity,
                'total_amount': ticket_purchase.total_amount,
                'payment_method': EmailService._format_payment_method(ticket_purchase.payment_method),
                'ticket_codes': ticket_codes,
            }
            
            # Render email templates
            html_message = render_to_string('emails/ticket_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            success = send_mail(
                subject=f'Ticket Confirmation - {context["ticket_title"]} | Tails & Trails',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            if success:
                logger.info(f"Ticket confirmation email sent to {customer_email} for purchase {ticket_purchase.purchase_id}")
                return True
            else:
                logger.error(f"Failed to send ticket confirmation email for purchase {ticket_purchase.purchase_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending ticket confirmation email for purchase {ticket_purchase.purchase_id}: {str(e)}")
            return False
    
    @staticmethod
    def _format_payment_method(payment_method):
        """Format payment method for display"""
        method_map = {
            'mtn_momo': 'MTN Mobile Money',
            'vodafone_cash': 'Vodafone Cash',
            'airteltigo_money': 'AirtelTigo Money',
            'paystack_momo': 'Mobile Money (Paystack)',
            'momo': 'Mobile Money',
            'card': 'Credit/Debit Card',
            'stripe': 'Credit/Debit Card (Stripe)',
        }
        return method_map.get(payment_method, payment_method.replace('_', ' ').title())
    
    @staticmethod
    def test_email_configuration():
        """Test email configuration"""
        try:
            success = send_mail(
                subject='Test Email - Tails & Trails',
                message='This is a test email to verify SMTP configuration.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['test@example.com'],  # Replace with your test email
                fail_silently=False,
            )
            return success
        except Exception as e:
            logger.error(f"Email configuration test failed: {str(e)}")
            return False