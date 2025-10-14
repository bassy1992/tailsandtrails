from django.core.management.base import BaseCommand
from django.utils import timezone
from tickets.models import Ticket, TicketPurchase, TicketCode
from authentication.models import User

class Command(BaseCommand):
    help = 'Test ticket purchase creation'

    def handle(self, *args, **options):
        # Get first available ticket
        ticket = Ticket.objects.filter(status='published').first()
        
        if not ticket:
            self.stdout.write(self.style.ERROR('No published tickets found'))
            return
        
        self.stdout.write(f'Found ticket: {ticket.title} - GH₵{ticket.price}')
        
        try:
            # Get or create a test user
            user, created = User.objects.get_or_create(
                email='test@example.com',
                defaults={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created test user: {user.email}')
            else:
                self.stdout.write(f'Using existing user: {user.email}')
            
            # Create a ticket purchase
            purchase = TicketPurchase.objects.create(
                ticket=ticket,
                user=user,
                quantity=2,
                unit_price=ticket.price,
                total_amount=ticket.price * 2,
                customer_name='Test Customer',
                customer_email='test@example.com',
                customer_phone='+233240000000',
                payment_method='mtn_momo',
                status='confirmed',
                payment_status='completed',
                payment_date=timezone.now()
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created ticket purchase: {purchase.purchase_id}')
            )
            
            # Generate ticket codes
            for i in range(purchase.quantity):
                code = TicketCode.objects.create(
                    purchase=purchase,
                    status='active'
                )
                self.stdout.write(f'  Generated ticket code: {code.code}')
            
            # Update ticket availability
            ticket.available_quantity -= purchase.quantity
            ticket.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated ticket availability: {ticket.available_quantity} remaining')
            )
            
            # Show summary
            total_purchases = TicketPurchase.objects.count()
            self.stdout.write(f'\n📊 Total ticket purchases in database: {total_purchases}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎫 Ticket purchase created successfully!'
                    f'\n   Purchase ID: {purchase.purchase_id}'
                    f'\n   Ticket: {purchase.ticket.title}'
                    f'\n   Quantity: {purchase.quantity}'
                    f'\n   Total: GH₵{purchase.total_amount}'
                    f'\n   Status: {purchase.status}'
                    f'\n   Codes Generated: {purchase.ticket_codes.count()}'
                    f'\n\n✅ Check /admin/tickets/ticketpurchase/ to see this purchase!'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating ticket purchase: {str(e)}')
            )