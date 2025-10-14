/**
 * Payment Methods Integration for Trails & Trails
 * Replace your current payment method selection with this code
 */

class PaymentMethodsManager {
    constructor(apiBase = '/api/payments', authToken = null) {
        this.apiBase = apiBase;
        this.authToken = authToken;
        this.paymentMethods = [];
        this.selectedMethod = null;
        // Stripe removed - using MTN MoMo only
        this.elements = null;
    }

    // Initialize payment methods
    async init() {
        try {
            await this.loadPaymentMethods();
            this.renderPaymentMethods();
        } catch (error) {
            console.error('Error initializing payment methods:', error);
        }
    }

    // Load payment methods from API
    async loadPaymentMethods() {
        const response = await fetch(`${this.apiBase}/checkout/methods/`);
        const data = await response.json();
        this.paymentMethods = data.payment_methods;
        return data;
    }

    // Render payment methods (replace your current HTML)
    renderPaymentMethods() {
        const container = document.getElementById('payment-methods-container');
        if (!container) {
            console.error('Payment methods container not found');
            return;
        }

        container.innerHTML = `
            <h3>Choose your preferred payment option</h3>
            ${this.paymentMethods.map(method => this.renderPaymentMethod(method)).join('')}
        `;

        // Add click handlers
        this.paymentMethods.forEach(method => {
            const element = document.getElementById(`payment-method-${method.id}`);
            if (element) {
                element.addEventListener('click', () => this.selectPaymentMethod(method));
            }
        });
    }

    // Render individual payment method
    renderPaymentMethod(method) {
        // Only show methods with providers or bank transfer
        if (method.providers.length === 0 && method.id !== 'bank_transfer') {
            return '';
        }

        return `
            <div id="payment-method-${method.id}" class="payment-method" data-method="${method.id}">
                <div class="payment-method-content">
                    <div class="payment-icon">${method.icon}</div>
                    <div class="payment-info">
                        <h4>${method.name}</h4>
                        <p>${method.description}</p>
                        <span class="processing-time">${method.processing_time}</span>
                    </div>
                </div>
            </div>
        `;
    }

    // Select payment method
    selectPaymentMethod(method) {
        // Remove previous selection
        document.querySelectorAll('.payment-method').forEach(el => {
            el.classList.remove('selected');
        });

        // Select new method
        const element = document.getElementById(`payment-method-${method.id}`);
        element.classList.add('selected');
        this.selectedMethod = method;

        // Show appropriate form
        this.showPaymentForm(method.id);
    }

    // Show payment form based on method
    showPaymentForm(methodId) {
        // Hide all forms
        document.querySelectorAll('.payment-form').forEach(form => {
            form.style.display = 'none';
        });

        // Show selected form
        const formId = `${methodId}-form`;
        const form = document.getElementById(formId);
        if (form) {
            form.style.display = 'block';
        }

        // Card payments removed - using MTN MoMo only
        if (methodId === 'card') {
            alert('Card payments are no longer supported. Please use MTN MoMo.');
            return;
        }
    }

    // Stripe initialization removed - using MTN MoMo only

    // Process Mobile Money Payment
    async processMoMoPayment(phoneNumber, amount, currency = 'GHS') {
        try {
            const response = await fetch(`${this.apiBase}/checkout/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${this.authToken}`
                },
                body: JSON.stringify({
                    amount: amount,
                    currency: currency,
                    payment_method: 'momo',
                    provider_code: 'mtn_momo',
                    phone_number: phoneNumber,
                    description: 'Travel booking payment'
                })
            });

            const result = await response.json();

            if (result.success) {
                this.showMessage('Payment request sent to your phone. Please check your mobile money app.', 'success');
                this.pollPaymentStatus(result.payment.reference);
                return result;
            } else {
                this.showMessage('Error: ' + result.error, 'error');
                return null;
            }
        } catch (error) {
            this.showMessage('Error processing payment: ' + error.message, 'error');
            return null;
        }
    }

    // Stripe payment processing removed - using MTN MoMo only

    // Poll payment status for mobile money
    async pollPaymentStatus(reference) {
        let attempts = 0;
        const maxAttempts = 30;

        const checkStatus = async () => {
            try {
                const response = await fetch(`${this.apiBase}/${reference}/status/`, {
                    headers: {
                        'Authorization': `Token ${this.authToken}`
                    }
                });

                const payment = await response.json();

                if (payment.status === 'successful') {
                    this.showMessage('Payment completed successfully! 🎉', 'success');
                    // Redirect or update UI
                    window.location.href = '/payment-success';
                } else if (payment.status === 'failed') {
                    this.showMessage('Payment failed. Please try again.', 'error');
                } else if (payment.status === 'cancelled') {
                    this.showMessage('Payment was cancelled.', 'error');
                } else if (attempts < maxAttempts) {
                    attempts++;
                    setTimeout(checkStatus, 10000); // Check every 10 seconds
                } else {
                    this.showMessage('Payment is taking longer than expected. Please contact support.', 'error');
                }
            } catch (error) {
                console.error('Error checking payment status:', error);
            }
        };

        // Start checking after 5 seconds
        setTimeout(checkStatus, 5000);
    }

    // Show message to user
    showMessage(message, type) {
        // You can customize this based on your UI framework
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type}`;
        messageDiv.textContent = message;

        const container = document.getElementById('messages') || document.body;
        container.appendChild(messageDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// Usage Example:
/*
// Initialize payment methods
const paymentManager = new PaymentMethodsManager('/api/payments', 'your-auth-token');

// Load and render payment methods
document.addEventListener('DOMContentLoaded', async () => {
    await paymentManager.init();
});

// Handle mobile money payment
function handleMoMoPayment() {
    const phoneNumber = document.getElementById('phone-input').value;
    const amount = 150.00;
    paymentManager.processMoMoPayment(phoneNumber, amount);
}

// Stripe payment handler removed - using MTN MoMo only
*/

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PaymentMethodsManager;
}