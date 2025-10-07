import stripe
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import StripeCustomer, StripePaymentIntent, StripePaymentMethod, StripeRefund

User = get_user_model()
logger = logging.getLogger(__name__)

class StripeService:
    """Service class for handling Stripe operations"""
    
    def __init__(self):
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        self.publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
        
    def get_or_create_customer(self, user: User) -> Dict[str, Any]:
        """Get or create a Stripe customer for the user"""
        try:
            # Check if customer already exists
            stripe_customer, created = StripeCustomer.objects.get_or_create(
                user=user,
                defaults={'stripe_customer_id': ''}
            )
            
            if created or not stripe_customer.stripe_customer_id:
                # Create customer in Stripe
                customer = stripe.Customer.create(
                    email=user.email,
                    name=f"{user.first_name} {user.last_name}".strip(),
                    metadata={
                        'user_id': str(user.id),
                        'username': user.username
                    }
                )
                
                stripe_customer.stripe_customer_id = customer.id
                stripe_customer.save()
                
                logger.info(f"Created Stripe customer {customer.id} for user {user.email}")
            
            return {
                'success': True,
                'customer_id': stripe_customer.stripe_customer_id,
                'customer': stripe_customer
            }
            
        except stripe.StripeError as e:
            logger.error(f"Stripe error creating customer for {user.email}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error creating customer for {user.email}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_payment_intent(self, user: User, amount: float, currency: str = 'USD', 
                            booking=None, description: str = '', metadata: Dict = None) -> Dict[str, Any]:
        """Create a Stripe Payment Intent"""
        try:
            # Get or create customer
            customer_result = self.get_or_create_customer(user)
            if not customer_result['success']:
                return customer_result
            
            customer_id = customer_result['customer_id']
            
            # Convert amount to cents
            amount_cents = int(amount * 100)
            
            # Prepare metadata
            intent_metadata = {
                'user_id': str(user.id),
                'user_email': user.email,
            }
            if booking:
                intent_metadata['booking_id'] = str(booking.id)
            if metadata:
                intent_metadata.update(metadata)
            
            # Create Payment Intent in Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency.lower(),
                customer=customer_id,
                description=description,
                metadata=intent_metadata,
                automatic_payment_methods={'enabled': True},
            )
            
            # Save Payment Intent to database
            payment_intent = StripePaymentIntent.objects.create(
                user=user,
                booking=booking,
                stripe_payment_intent_id=intent.id,
                client_secret=intent.client_secret,
                amount=amount,
                currency=currency.upper(),
                status=intent.status,
                description=description,
                metadata=intent_metadata
            )
            
            logger.info(f"Created Payment Intent {intent.id} for user {user.email}")
            
            return {
                'success': True,
                'payment_intent': payment_intent,
                'client_secret': intent.client_secret,
                'publishable_key': self.publishable_key
            }
            
        except stripe.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_payment_intent(self, payment_intent_id: str, payment_method_id: str = None) -> Dict[str, Any]:
        """Confirm a Payment Intent"""
        try:
            # Get payment intent from database
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            # Confirm in Stripe
            confirm_params = {}
            if payment_method_id:
                confirm_params['payment_method'] = payment_method_id
            
            stripe_intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                **confirm_params
            )
            
            # Update database
            payment_intent.status = stripe_intent.status
            payment_intent.payment_method_id = stripe_intent.payment_method
            payment_intent.confirmed_at = timezone.now()
            
            if stripe_intent.status == 'succeeded':
                payment_intent.succeeded_at = timezone.now()
            
            payment_intent.save()
            
            logger.info(f"Confirmed Payment Intent {payment_intent_id}")
            
            return {
                'success': True,
                'payment_intent': payment_intent,
                'status': stripe_intent.status,
                'requires_action': stripe_intent.status == 'requires_action',
                'client_secret': stripe_intent.client_secret if stripe_intent.status == 'requires_action' else None
            }
            
        except StripePaymentIntent.DoesNotExist:
            return {
                'success': False,
                'error': 'Payment Intent not found'
            }
        except stripe.StripeError as e:
            logger.error(f"Stripe error confirming payment intent {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error confirming payment intent {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def retrieve_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Retrieve and update Payment Intent status"""
        try:
            # Get from Stripe
            stripe_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            # Update database
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            old_status = payment_intent.status
            payment_intent.status = stripe_intent.status
            payment_intent.payment_method_id = stripe_intent.payment_method
            
            if stripe_intent.status == 'succeeded' and old_status != 'succeeded':
                payment_intent.succeeded_at = timezone.now()
            
            payment_intent.save()
            
            return {
                'success': True,
                'payment_intent': payment_intent,
                'status': stripe_intent.status,
                'status_changed': old_status != stripe_intent.status
            }
            
        except StripePaymentIntent.DoesNotExist:
            return {
                'success': False,
                'error': 'Payment Intent not found'
            }
        except stripe.StripeError as e:
            logger.error(f"Stripe error retrieving payment intent {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error retrieving payment intent {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def cancel_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Cancel a Payment Intent"""
        try:
            # Cancel in Stripe
            stripe_intent = stripe.PaymentIntent.cancel(payment_intent_id)
            
            # Update database
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            payment_intent.status = stripe_intent.status
            payment_intent.save()
            
            logger.info(f"Canceled Payment Intent {payment_intent_id}")
            
            return {
                'success': True,
                'payment_intent': payment_intent,
                'status': stripe_intent.status
            }
            
        except StripePaymentIntent.DoesNotExist:
            return {
                'success': False,
                'error': 'Payment Intent not found'
            }
        except stripe.StripeError as e:
            logger.error(f"Stripe error canceling payment intent {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error canceling payment intent {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_refund(self, payment_intent_id: str, amount: float = None, 
                     reason: str = '', description: str = '') -> Dict[str, Any]:
        """Create a refund for a Payment Intent"""
        try:
            # Get payment intent
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            if payment_intent.status != 'succeeded':
                return {
                    'success': False,
                    'error': 'Payment Intent must be succeeded to refund'
                }
            
            # Prepare refund parameters
            refund_params = {
                'payment_intent': payment_intent_id,
                'reason': reason or 'requested_by_customer',
                'metadata': {
                    'user_id': str(payment_intent.user.id),
                    'booking_id': str(payment_intent.booking.id) if payment_intent.booking else '',
                    'description': description
                }
            }
            
            if amount:
                refund_params['amount'] = int(amount * 100)  # Convert to cents
            
            # Create refund in Stripe
            stripe_refund = stripe.Refund.create(**refund_params)
            
            # Save refund to database
            refund = StripeRefund.objects.create(
                payment_intent=payment_intent,
                stripe_refund_id=stripe_refund.id,
                amount=stripe_refund.amount / 100,  # Convert from cents
                currency=stripe_refund.currency.upper(),
                status=stripe_refund.status,
                reason=stripe_refund.reason,
                description=description,
                metadata=stripe_refund.metadata
            )
            
            logger.info(f"Created refund {stripe_refund.id} for Payment Intent {payment_intent_id}")
            
            return {
                'success': True,
                'refund': refund,
                'status': stripe_refund.status
            }
            
        except StripePaymentIntent.DoesNotExist:
            return {
                'success': False,
                'error': 'Payment Intent not found'
            }
        except stripe.StripeError as e:
            logger.error(f"Stripe error creating refund for {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error creating refund for {payment_intent_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_payment_method(self, user: User, payment_method_id: str) -> Dict[str, Any]:
        """Save a payment method for future use"""
        try:
            # Get customer
            customer_result = self.get_or_create_customer(user)
            if not customer_result['success']:
                return customer_result
            
            customer_id = customer_result['customer_id']
            
            # Attach payment method to customer
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id
            )
            
            # Get payment method details
            stripe_pm = stripe.PaymentMethod.retrieve(payment_method_id)
            
            # Save to database
            payment_method = StripePaymentMethod.objects.create(
                user=user,
                stripe_payment_method_id=payment_method_id,
                type=stripe_pm.type,
                card_brand=stripe_pm.card.brand if stripe_pm.type == 'card' else '',
                card_last4=stripe_pm.card.last4 if stripe_pm.type == 'card' else '',
                card_exp_month=stripe_pm.card.exp_month if stripe_pm.type == 'card' else None,
                card_exp_year=stripe_pm.card.exp_year if stripe_pm.type == 'card' else None,
                details=stripe_pm.to_dict()
            )
            
            logger.info(f"Saved payment method {payment_method_id} for user {user.email}")
            
            return {
                'success': True,
                'payment_method': payment_method
            }
            
        except stripe.StripeError as e:
            logger.error(f"Stripe error saving payment method {payment_method_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error saving payment method {payment_method_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }  
  
    def process_webhook_event(self, webhook_event):
        """Process a Stripe webhook event"""
        event_type = webhook_event.event_type
        event_data = webhook_event.data
        
        try:
            if event_type == 'payment_intent.succeeded':
                self._handle_payment_intent_succeeded(event_data)
            elif event_type == 'payment_intent.payment_failed':
                self._handle_payment_intent_failed(event_data)
            elif event_type == 'payment_intent.canceled':
                self._handle_payment_intent_canceled(event_data)
            elif event_type == 'charge.dispute.created':
                self._handle_charge_dispute_created(event_data)
            else:
                logger.info(f"Unhandled webhook event type: {event_type}")
                
        except Exception as e:
            logger.error(f"Error processing webhook event {webhook_event.stripe_event_id}: {str(e)}")
            raise
    
    def _handle_payment_intent_succeeded(self, event_data):
        """Handle payment_intent.succeeded webhook"""
        payment_intent_data = event_data.get('object', {})
        payment_intent_id = payment_intent_data.get('id')
        
        try:
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            if payment_intent.status != 'succeeded':
                payment_intent.status = 'succeeded'
                payment_intent.succeeded_at = timezone.now()
                payment_intent.save()
                
                logger.info(f"Updated payment intent {payment_intent_id} to succeeded")
                
        except StripePaymentIntent.DoesNotExist:
            logger.warning(f"Payment intent {payment_intent_id} not found in database")
    
    def _handle_payment_intent_failed(self, event_data):
        """Handle payment_intent.payment_failed webhook"""
        payment_intent_data = event_data.get('object', {})
        payment_intent_id = payment_intent_data.get('id')
        
        try:
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            payment_intent.status = 'requires_payment_method'
            payment_intent.save()
            
            logger.info(f"Updated payment intent {payment_intent_id} to failed")
            
        except StripePaymentIntent.DoesNotExist:
            logger.warning(f"Payment intent {payment_intent_id} not found in database")
    
    def _handle_payment_intent_canceled(self, event_data):
        """Handle payment_intent.canceled webhook"""
        payment_intent_data = event_data.get('object', {})
        payment_intent_id = payment_intent_data.get('id')
        
        try:
            payment_intent = StripePaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            payment_intent.status = 'canceled'
            payment_intent.save()
            
            logger.info(f"Updated payment intent {payment_intent_id} to canceled")
            
        except StripePaymentIntent.DoesNotExist:
            logger.warning(f"Payment intent {payment_intent_id} not found in database")
    
    def _handle_charge_dispute_created(self, event_data):
        """Handle charge.dispute.created webhook"""
        dispute_data = event_data.get('object', {})
        charge_id = dispute_data.get('charge')
        
        logger.warning(f"Dispute created for charge {charge_id}")
        # Additional dispute handling logic can be added here