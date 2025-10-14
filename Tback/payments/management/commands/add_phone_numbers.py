from django.core.management.base import BaseCommand
from django.db import transaction
from authentication.models import User
from payments.models import Payment


class Command(BaseCommand):
    help = 'Add phone numbers to users and update payment booking details'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to add (e.g., +233241234567)',
        )
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email of specific user to update',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        phone = options.get('phone')
        user_email = options.get('user_email')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get users to update
        if user_email:
            users = User.objects.filter(email=user_email)
            if not users.exists():
                self.stdout.write(
                    self.style.ERROR(f'User with email {user_email} not found.')
                )
                return
        else:
            # Get users who don't have phone numbers
            users = User.objects.filter(phone_number__in=['', None])
        
        total_users = users.count()
        
        if total_users == 0:
            self.stdout.write(
                self.style.SUCCESS('No users need phone number updates.')
            )
            return
        
        self.stdout.write(f'Found {total_users} users without phone numbers.')
        
        # Default phone number if not provided
        if not phone:
            phone = '+233241234567'  # Default Ghana phone number
        
        updated_count = 0
        
        with transaction.atomic():
            for user in users:
                if dry_run:
                    self.stdout.write(
                        f'Would add phone {phone} to user {user.email}'
                    )
                else:
                    user.phone_number = phone
                    user.save(update_fields=['phone_number'])
                    self.stdout.write(
                        f'Added phone {phone} to user {user.email}'
                    )
                
                updated_count += 1
        
        # Update payment booking details with phone numbers
        if not dry_run:
            self._update_payment_booking_details(phone)
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would update {updated_count} users')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {updated_count} users')
            )

    def _update_payment_booking_details(self, phone):
        """Update booking details in payments to include phone numbers"""
        payments = Payment.objects.filter(
            metadata__has_key='booking_details'
        )
        
        updated_payments = 0
        
        for payment in payments:
            booking_details = payment.metadata.get('booking_details', {})
            user_info = booking_details.get('user_info', {})
            
            # Update phone in user_info if it's empty
            if not user_info.get('phone'):
                user_info['phone'] = payment.user.phone_number if payment.user else phone
                booking_details['user_info'] = user_info
                payment.metadata['booking_details'] = booking_details
                payment.save(update_fields=['metadata'])
                updated_payments += 1
                
                self.stdout.write(
                    f'Updated phone in booking details for payment {payment.reference}'
                )
        
        if updated_payments > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Updated booking details for {updated_payments} payments')
            )