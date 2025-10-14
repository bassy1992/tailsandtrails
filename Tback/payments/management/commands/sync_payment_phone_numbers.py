from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment


class Command(BaseCommand):
    help = 'Sync phone numbers from users to their payments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get payments that don't have phone numbers but their users do
        payments = Payment.objects.filter(
            phone_number__in=['', None],
            user__phone_number__isnull=False
        ).exclude(
            user__phone_number=''
        )
        
        total_payments = payments.count()
        
        if total_payments == 0:
            self.stdout.write(
                self.style.SUCCESS('No payments need phone number updates.')
            )
            return
        
        self.stdout.write(f'Found {total_payments} payments that can get phone numbers from users.')
        
        updated_count = 0
        
        with transaction.atomic():
            for payment in payments:
                user_phone = payment.user.phone_number
                
                if dry_run:
                    self.stdout.write(
                        f'Would add phone {user_phone} to payment {payment.reference}'
                    )
                else:
                    payment.phone_number = user_phone
                    payment.save(update_fields=['phone_number'])
                    self.stdout.write(
                        f'Added phone {user_phone} to payment {payment.reference}'
                    )
                
                updated_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would update {updated_count} payments')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {updated_count} payments')
            )