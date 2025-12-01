from django.core.management.base import BaseCommand
from django.utils import timezone
from tickets.models import Ticket, TicketPurchase, TicketCode
from authentication.models import User
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate sample ticket purchases for testing the admin interface'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of sample purchases to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Get available tickets
        tickets = list(Ticket.objects.filter(status='active'))
        if not tickets:
            self.stdout.write(
                self.style.ERROR('No active tickets found. Please create some tickets first.')
            )
            return

        # Sample customer data
        customers = [
            {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '+233240000001'},
            {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'phone': '+233240000002'},
            {'name': 'Michael Johnson', 'email': 'michael.j@example.com', 'phone': '+233240000003'},
            {'name': 'Sarah Wilson', 'email': 'sarah.wilson@example.com', 'phone': '+233240000004'},
            {'name': 'David Brown', 'email': 'david.brown@example.com', 'phone': '+233240000005'},
            {'name': 'Lisa Davis', 'email': 'lisa.davis@example.com', 'phone': '+233240000006'},
            {'name': 'Robert Miller', 'email': 'robert.miller@example.com', 'phone': '+233240000007'},
            {'name': 'Emily Taylor', 'email': 'emily.taylor@example.com', 'phone': '+233240000008'},
            {'name': 'James Anderson', 'email': 'james.anderson@example.com', 'phone': '+233240000009'},
            {'name': 'Maria Garcia', 'email': 'maria.garcia@example.com', 'phone': '+233240000010'},
        ]

        payment_methods = ['mtn_momo', 'vodafone_cash', 'airteltigo_money']
        statuses = ['confirmed', 'pending', 'cancelled']
        payment_statuses = ['completed', 'pending', 'failed']

        # Get the first available user for purchases
        try:
            dummy_user = User.objects.first()
            if not dummy_user:
                self.stdout.write(
                    self.style.ERROR('No users found. Please create a user first.')
                )
                return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting user: {e}')
            )
            return

        created_purchases = []

        for i in range(count):
            # Random ticket and customer
            ticket = random.choice(tickets)
            customer = random.choice(customers)
            
            # Random quantity (1-3)
            quantity = random.randint(1, 3)
            
            # Calculate pricing
            unit_price = ticket.discount_price if ticket.discount_price else ticket.price
            total_amount = unit_price * quantity
            
            # Random status
            status = random.choice(statuses)
            payment_status = random.choice(payment_statuses)
            
            # Ensure logical consistency
            if status == 'confirmed':
                payment_status = 'completed'
            elif status == 'cancelled':
                payment_status = random.choice(['failed', 'refunded'])
            
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            created_at = timezone.now() - timedelta(days=days_ago)
            
            # Create purchase
            purchase = TicketPurchase.objects.create(
                ticket=ticket,
                user=dummy_user,
                quantity=quantity,
                unit_price=unit_price,
                total_amount=total_amount,
                customer_name=customer['name'],
                customer_email=customer['email'],
                customer_phone=customer['phone'],
                payment_method=random.choice(payment_methods),
                status=status,
                payment_status=payment_status,
                special_requests=f'Sample purchase #{i+1}' if random.choice([True, False]) else '',
                created_at=created_at
            )
            
            # Create ticket codes if purchase is confirmed
            if status == 'confirmed':
                for j in range(quantity):
                    TicketCode.objects.create(
                        purchase=purchase,
                        status='active' if random.choice([True, True, False]) else 'used',
                        is_transferable=random.choice([True, False]),
                        created_at=created_at
                    )
            
            created_purchases.append(purchase)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_purchases)} sample ticket purchases!'
            )
        )
        
        # Show summary
        confirmed_count = sum(1 for p in created_purchases if p.status == 'confirmed')
        pending_count = sum(1 for p in created_purchases if p.status == 'pending')
        cancelled_count = sum(1 for p in created_purchases if p.status == 'cancelled')
        
        total_revenue = sum(p.total_amount for p in created_purchases if p.payment_status == 'completed')
        
        self.stdout.write(f'  - Confirmed: {confirmed_count}')
        self.stdout.write(f'  - Pending: {pending_count}')
        self.stdout.write(f'  - Cancelled: {cancelled_count}')
        self.stdout.write(f'  - Total Revenue: GH₵{total_revenue}')
        
        # Count ticket codes
        total_codes = TicketCode.objects.filter(purchase__in=created_purchases).count()
        self.stdout.write(f'  - Ticket Codes Generated: {total_codes}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nYou can now view these purchases in the admin at:'
            )
        )
        self.stdout.write('  - /admin/tickets/ticketpurchase/')
        self.stdout.write('  - /admin/tickets/ticketcode/')