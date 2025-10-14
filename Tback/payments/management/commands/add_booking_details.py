from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment
from destinations.models import Destination
import json


class Command(BaseCommand):
    help = 'Add booking details to payments that are missing them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--payment-reference',
            type=str,
            help='Update specific payment by reference',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        payment_reference = options.get('payment_reference')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get payments to update
        if payment_reference:
            payments = Payment.objects.filter(reference=payment_reference)
            if not payments.exists():
                self.stdout.write(
                    self.style.ERROR(f'Payment with reference {payment_reference} not found.')
                )
                return
        else:
            # Get payments that don't have booking_details in metadata
            payments = Payment.objects.exclude(
                metadata__has_key='booking_details'
            ).filter(
                metadata__isnull=False
            )
        
        total_payments = payments.count()
        
        if total_payments == 0:
            self.stdout.write(
                self.style.SUCCESS('No payments need booking details updates.')
            )
            return
        
        self.stdout.write(f'Found {total_payments} payments to update.')
        
        updated_count = 0
        
        with transaction.atomic():
            for payment in payments:
                booking_details = self._generate_booking_details(payment)
                
                if booking_details:
                    if not dry_run:
                        # Update the payment metadata
                        if not payment.metadata:
                            payment.metadata = {}
                        payment.metadata['booking_details'] = booking_details
                        payment.save(update_fields=['metadata'])
                    
                    updated_count += 1
                    
                    if dry_run:
                        self.stdout.write(
                            f'Would add booking details to payment {payment.reference}'
                        )
                        self.stdout.write(f'  Details: {json.dumps(booking_details, indent=2)}')
                    else:
                        self.stdout.write(
                            f'Added booking details to payment {payment.reference}'
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Could not generate booking details for payment {payment.reference}')
                    )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would update {updated_count} payments')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {updated_count} payments')
            )

    def _generate_booking_details(self, payment):
        """Generate booking details based on payment information"""
        booking_details = {}
        
        # Determine booking type from description
        if payment.description:
            description_lower = payment.description.lower()
            
            # Check if it's a ticket
            if any(word in description_lower for word in ['ticket', 'event', 'concert', 'show']):
                booking_details['type'] = 'ticket'
                booking_details = self._generate_ticket_details(payment, booking_details)
            else:
                booking_details['type'] = 'destination'
                booking_details = self._generate_destination_details(payment, booking_details)
        
        # Add user information
        if payment.user:
            # Prioritize user's phone number, fallback to payment phone number
            phone = payment.user.phone_number or payment.phone_number or ''
            booking_details['user_info'] = {
                'name': f"{payment.user.first_name} {payment.user.last_name}".strip() or payment.user.username,
                'email': payment.user.email,
                'phone': phone
            }
        
        # Add payment information
        booking_details['payment_info'] = {
            'amount': float(payment.amount),
            'currency': payment.currency,
            'payment_method': payment.get_payment_method_display(),
            'provider': payment.provider.name if payment.provider else None,
            'reference': payment.reference,
            'status': payment.get_status_display(),
            'created_at': payment.created_at.isoformat() if payment.created_at else None
        }
        
        return booking_details if booking_details else None

    def _generate_destination_details(self, payment, booking_details):
        """Generate destination-specific booking details"""
        
        # Try to find matching destination by name
        destination = None
        if payment.description:
            # Try exact match first
            destination = Destination.objects.filter(
                name__iexact=payment.description
            ).first()
            
            # Try partial match
            if not destination:
                destination = Destination.objects.filter(
                    name__icontains=payment.description.split()[0]
                ).first()
        
        if destination:
            booking_details['destination'] = {
                'id': destination.id,
                'name': destination.name,
                'location': destination.location,
                'duration': destination.get_duration_display(),
                'price': float(destination.price),
                'category': destination.category.name if destination.category else None,
                'image': destination.image
            }
        else:
            # Create generic destination info from payment description
            booking_details['destination'] = {
                'name': payment.description or 'Unknown Destination',
                'location': 'Ghana',  # Default location
                'duration': 'Unknown',
                'price': float(payment.amount),
                'category': 'Tour'
            }
        
        # Add default traveler info (since we don't have specific data)
        booking_details['travelers'] = {
            'adults': 1,  # Default assumption
            'children': 0
        }
        
        # Add booking date (use payment creation date as fallback)
        booking_details['selected_date'] = payment.created_at.strftime('%Y-%m-%d') if payment.created_at else None
        
        # Add pricing breakdown
        booking_details['pricing'] = {
            'base_total': float(payment.amount),
            'options_total': 0.0,
            'final_total': float(payment.amount)
        }
        
        return booking_details

    def _generate_ticket_details(self, payment, booking_details):
        """Generate ticket-specific booking details"""
        
        # Create ticket info from payment description
        booking_details['ticket'] = {
            'name': payment.description or 'Event Ticket',
            'price': float(payment.amount),
            'currency': payment.currency,
            'quantity': 1  # Default assumption
        }
        
        # Add purchase info
        booking_details['purchase_info'] = {
            'purchase_date': payment.created_at.strftime('%Y-%m-%d %H:%M:%S') if payment.created_at else None,
            'payment_method': payment.get_payment_method_display(),
            'total_amount': float(payment.amount)
        }
        
        return booking_details