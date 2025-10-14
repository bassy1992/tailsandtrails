"""
Utility functions for managing booking details in payments
"""
from destinations.models import Destination, Booking
from tickets.models import Ticket, TicketPurchase


def generate_destination_booking_details(destination, user, travelers_info, selected_options=None, booking_date=None):
    """
    Generate booking details for a destination booking
    
    Args:
        destination: Destination model instance
        user: User model instance
        travelers_info: dict with 'adults' and 'children' counts
        selected_options: dict with selected add-on options
        booking_date: date string or date object
    
    Returns:
        dict: Formatted booking details for payment metadata
    """
    booking_details = {
        'type': 'destination',
        'destination': {
            'id': destination.id,
            'name': destination.name,
            'location': destination.location,
            'duration': destination.get_duration_display(),
            'price': float(destination.price),
            'category': destination.category.name if destination.category else None,
            'image': destination.image,
            'description': destination.description[:200] + '...' if len(destination.description) > 200 else destination.description
        },
        'travelers': travelers_info,
        'selected_date': str(booking_date) if booking_date else None,
        'user_info': {
            'name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
            'phone': getattr(user, 'phone_number', '') or ''
        }
    }
    
    # Add selected options if provided
    if selected_options:
        booking_details['selected_options'] = selected_options
        
        # Calculate pricing breakdown
        base_total = float(destination.price) * travelers_info.get('adults', 1)
        options_total = 0.0
        
        # Calculate options total (this would need to be implemented based on your pricing logic)
        # For now, we'll leave it as 0
        
        booking_details['pricing'] = {
            'base_total': base_total,
            'options_total': options_total,
            'final_total': base_total + options_total
        }
    
    return booking_details


def generate_ticket_booking_details(ticket, user, quantity=1, customer_info=None):
    """
    Generate booking details for a ticket purchase
    
    Args:
        ticket: Ticket model instance
        user: User model instance
        quantity: number of tickets
        customer_info: dict with customer details
    
    Returns:
        dict: Formatted booking details for payment metadata
    """
    booking_details = {
        'type': 'ticket',
        'ticket': {
            'id': ticket.id,
            'name': ticket.title,
            'price': float(ticket.effective_price),
            'currency': ticket.currency,
            'quantity': quantity,
            'event_date': ticket.event_date.isoformat() if ticket.event_date else None,
            'venue': {
                'name': ticket.venue.name if ticket.venue else None,
                'address': ticket.venue.address if ticket.venue else None,
                'city': ticket.venue.city if ticket.venue else None
            } if ticket.venue else None,
            'category': ticket.category.name if ticket.category else None,
            'description': ticket.description[:200] + '...' if len(ticket.description) > 200 else ticket.description
        },
        'purchase_info': {
            'quantity': quantity,
            'unit_price': float(ticket.effective_price),
            'total_amount': float(ticket.effective_price) * quantity,
            'purchase_date': None  # Will be set when payment is created
        },
        'user_info': {
            'name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
            'phone': getattr(user, 'phone_number', '') or ''
        }
    }
    
    # Override with custom customer info if provided
    if customer_info:
        booking_details['user_info'].update(customer_info)
    
    return booking_details


def add_booking_details_to_payment(payment, booking_details):
    """
    Add booking details to a payment's metadata
    
    Args:
        payment: Payment model instance
        booking_details: dict with booking details
    """
    if not payment.metadata:
        payment.metadata = {}
    
    # Add timestamp to booking details
    from django.utils import timezone
    booking_details['created_at'] = timezone.now().isoformat()
    
    payment.metadata['booking_details'] = booking_details
    payment.save(update_fields=['metadata'])


def get_booking_details_from_payment(payment):
    """
    Extract booking details from a payment's metadata
    
    Args:
        payment: Payment model instance
    
    Returns:
        dict or None: Booking details if available
    """
    if payment.metadata and 'booking_details' in payment.metadata:
        return payment.metadata['booking_details']
    return None


def create_booking_from_payment(payment):
    """
    Create a Booking record from payment booking details or payment description
    
    Args:
        payment: Payment model instance with booking_details in metadata or description
    
    Returns:
        Booking instance or None
    """
    # First try to get booking details from metadata
    booking_details = get_booking_details_from_payment(payment)
    
    if booking_details and booking_details.get('type') == 'destination':
        # Use metadata booking details
        destination_info = booking_details.get('destination', {})
        travelers_info = booking_details.get('travelers', {})
        
        try:
            destination = Destination.objects.get(id=destination_info.get('id'))
            
            booking = Booking.objects.create(
                destination=destination,
                user=payment.user,
                booking_type='destination',
                participants=travelers_info.get('adults', 1) + travelers_info.get('children', 0),
                total_amount=payment.amount,
                booking_date=booking_details.get('selected_date') or payment.created_at.date(),
                status='confirmed' if payment.status == 'successful' else 'pending'
            )
            
            # Link the payment to the booking
            payment.booking = booking
            payment.save(update_fields=['booking'])
            
            return booking
            
        except Destination.DoesNotExist:
            pass
    
    # Fallback: Try to create booking from payment description
    if payment.description:
        # Try to find destination by name
        destination = None
        
        # Try exact match first
        destination = Destination.objects.filter(name__iexact=payment.description).first()
        
        # Try partial match if exact doesn't work
        if not destination:
            destination = Destination.objects.filter(name__icontains=payment.description.split()[0]).first()
        
        if destination:
            try:
                from django.utils import timezone
                
                booking = Booking.objects.create(
                    destination=destination,
                    user=payment.user,
                    booking_type='destination',
                    participants=1,  # Default to 1 participant
                    total_amount=payment.amount,
                    booking_date=timezone.now().date() + timezone.timedelta(days=7),  # Default to next week
                    status='confirmed' if payment.status == 'successful' else 'pending',
                    special_requests=f'Auto-created from payment {payment.reference}'
                )
                
                # Link the payment to the booking
                payment.booking = booking
                payment.save(update_fields=['booking'])
                
                return booking
                
            except Exception as e:
                print(f"Error creating fallback booking: {str(e)}")
                return None
    
    return None


def create_ticket_purchase_from_payment(payment):
    """
    Create a TicketPurchase record from payment booking details or payment description
    
    Args:
        payment: Payment model instance with booking_details in metadata or description
    
    Returns:
        TicketPurchase instance or None
    """
    # First try to get booking details from metadata
    booking_details = get_booking_details_from_payment(payment)
    
    if booking_details and booking_details.get('type') == 'ticket':
        # Use metadata booking details
        ticket_info = booking_details.get('ticket', {})
        user_info = booking_details.get('user_info', {})
        
        try:
            ticket = Ticket.objects.get(id=ticket_info.get('id'))
            
            ticket_purchase = TicketPurchase.objects.create(
                ticket=ticket,
                user=payment.user,
                quantity=ticket_info.get('quantity', 1),
                unit_price=ticket_info.get('price', 0),
                total_amount=payment.amount,
                customer_name=user_info.get('name', ''),
                customer_email=user_info.get('email', ''),
                customer_phone=user_info.get('phone', ''),
                status='confirmed' if payment.status == 'successful' else 'pending',
                payment_status='completed' if payment.status == 'successful' else 'pending',
                payment_method=payment.get_payment_method_display(),
                payment_reference=payment.reference,
                payment_date=payment.processed_at or payment.created_at
            )
            
            return ticket_purchase
            
        except Ticket.DoesNotExist:
            pass
    
    # Fallback: Try to create ticket purchase from payment description
    if payment.description:
        description_lower = payment.description.lower()
        
        # Check if this looks like a ticket purchase
        is_ticket = any(word in description_lower for word in [
            'ticket', 'event', 'concert', 'festival', 'show', 'performance'
        ])
        
        if is_ticket:
            # Try to find ticket by description
            ticket = Ticket.objects.filter(title__icontains=payment.description.split()[0]).first()
            
            if ticket:
                try:
                    ticket_purchase = TicketPurchase.objects.create(
                        ticket=ticket,
                        user=payment.user,
                        quantity=1,  # Default to 1 ticket
                        unit_price=payment.amount,
                        total_amount=payment.amount,
                        customer_name=payment.user.get_full_name() or payment.user.username,
                        customer_email=payment.user.email,
                        customer_phone=getattr(payment.user, 'phone_number', '') or payment.phone_number or '+233241227481',
                        status='confirmed' if payment.status == 'successful' else 'pending',
                        payment_status='completed' if payment.status == 'successful' else 'pending',
                        payment_method='mobile_money' if payment.payment_method == 'mobile_money' else 'card',
                        payment_reference=payment.reference,
                        payment_date=payment.processed_at or payment.created_at
                    )
                    
                    return ticket_purchase
                    
                except Exception as e:
                    print(f"Error creating fallback ticket purchase: {str(e)}")
                    return None
    
    return None