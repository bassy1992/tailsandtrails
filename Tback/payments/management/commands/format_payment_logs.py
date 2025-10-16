"""
Management command to reformat existing payment logs for better admin readability
"""
from django.core.management.base import BaseCommand
from payments.models import Payment, PaymentLog
import json


class Command(BaseCommand):
    help = 'Reformat existing payment logs for better admin readability'

    def add_arguments(self, parser):
        parser.add_argument(
            '--payment-ref',
            type=str,
            help='Specific payment reference to format (optional)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be formatted without making changes',
        )

    def format_booking_details_for_admin(self, booking_details):
        """Format booking details in a more readable format for admin logs"""
        try:
            if not booking_details:
                return "No booking details"
            
            # Handle both dict and string formats
            if isinstance(booking_details, str):
                booking_details = json.loads(booking_details)
            
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
            
            # Add pricing tiers if available
            pricing_data = booking_data.get('pricingData', {})
            if pricing_data.get('has_tiered_pricing') and pricing_data.get('pricing_tiers'):
                formatted["🎯 PRICING TIERS"] = {}
                for tier in pricing_data['pricing_tiers']:
                    tier_key = f"{tier['group_size_display']}"
                    formatted["🎯 PRICING TIERS"][tier_key] = f"GH₵{tier['price_per_person']} per person"
            
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
            return f"Formatting error: {str(e)}\nOriginal data: {json.dumps(booking_details, indent=2)}"

    def handle(self, *args, **options):
        payment_ref = options.get('payment_ref')
        dry_run = options.get('dry_run')
        
        # Get payments to process
        if payment_ref:
            payments = Payment.objects.filter(reference=payment_ref)
            if not payments.exists():
                self.stdout.write(
                    self.style.ERROR(f'Payment with reference {payment_ref} not found')
                )
                return
        else:
            payments = Payment.objects.all()
        
        self.stdout.write(f'Processing {payments.count()} payments...')
        
        formatted_count = 0
        
        for payment in payments:
            # Find logs with booking details that need formatting
            logs_to_format = PaymentLog.objects.filter(
                payment=payment,
                message__icontains='Booking details stored from request'
            )
            
            for log in logs_to_format:
                try:
                    # Check if the data field contains unformatted JSON
                    if log.data and isinstance(log.data, dict):
                        # Check if it looks like raw booking data (has bookingData key)
                        if 'bookingData' in log.data or 'baseTotal' in log.data:
                            formatted_details = self.format_booking_details_for_admin(log.data)
                            
                            if dry_run:
                                self.stdout.write(f'\n--- Payment: {payment.reference} ---')
                                self.stdout.write('Current format:')
                                self.stdout.write(json.dumps(log.data, indent=2)[:200] + '...')
                                self.stdout.write('\nWould format to:')
                                self.stdout.write(formatted_details[:300] + '...')
                            else:
                                # Update the log with formatted data
                                log.data = {'formatted_details': formatted_details, 'original_data': log.data}
                                log.save()
                                formatted_count += 1
                                
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error formatting log for payment {payment.reference}: {str(e)}')
                    )
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'Dry run complete. Found {formatted_count} logs that would be formatted.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully formatted {formatted_count} payment logs.')
            )