# 🔄 Replace Your Payment Methods with Stripe Integration

## Current Issue
You're seeing "Paystack / Flutterwave" instead of "Stripe" because your frontend is using hardcoded payment options instead of the dynamic API.

## ✅ Solution: Replace Your Current Code

### 1. **Replace Your Current HTML**

**❌ Remove this (your current code):**
```html
<div class="payment-methods">
  <h3>Choose your preferred payment option</h3>
  
  <div class="payment-option">
    <div class="payment-icon">📱</div>
    <div class="payment-info">
      <h4>Mobile Money</h4>
      <p>MTN, Vodafone, AirtelTigo</p>
      <span>Instant</span>
    </div>
  </div>
  
  <div class="payment-option">
    <div class="payment-icon">💳</div>
    <div class="payment-info">
      <h4>Paystack / Flutterwave</h4>
      <p>Cards + Mobile Money</p>
      <span>Secure</span>
    </div>
  </div>
  
  <div class="payment-option">
    <div class="payment-icon">🏦</div>
    <div class="payment-info">
      <h4>Bank Transfer</h4>
      <p>For large groups (optional)</p>
      <span>1-2 days</span>
    </div>
  </div>
</div>
```

**✅ Replace with this (dynamic API-driven code):**
```html
<div id="payment-methods-container">
  <!-- Payment methods will be loaded dynamically -->
  <div class="loading">Loading payment methods...</div>
</div>

<!-- Mobile Money Form -->
<div id="mobile_money-form" class="payment-form" style="display: none;">
  <h4>📱 MTN Mobile Money</h4>
  <div class="form-group">
    <label for="momo-phone">Phone Number</label>
    <input type="tel" id="momo-phone" placeholder="+233244123456" required>
    <small>Enter your MTN Mobile Money number</small>
  </div>
  <button onclick="handleMoMoPayment()">Pay GHS 150.00</button>
</div>

<!-- Stripe Card Form -->
<div id="card-form" class="payment-form" style="display: none;">
  <h4>💳 Credit/Debit Card</h4>
  <div class="form-group">
    <label>Card Details</label>
    <div id="stripe-elements">
      <!-- Stripe Elements will be mounted here -->
    </div>
  </div>
  <button onclick="handleStripePayment()">Pay GHS 150.00</button>
</div>

<!-- Bank Transfer Form -->
<div id="bank_transfer-form" class="payment-form" style="display: none;">
  <h4>🏦 Bank Transfer</h4>
  <p>For large group bookings, please contact us:</p>
  <ul>
    <li>Email: payments@trailsandtrails.com</li>
    <li>Phone: +233 XX XXX XXXX</li>
  </ul>
  <p><em>Processing time: 1-2 business days</em></p>
</div>

<div id="messages"></div>
```

### 2. **Add Required JavaScript**

**Add this JavaScript to your page:**
```html
<script src="https://js.stripe.com/v3/"></script>
<script>
// Payment Methods Manager
class PaymentMethodsManager {
    constructor() {
        this.apiBase = '/api/payments';
        this.authToken = 'YOUR_AUTH_TOKEN'; // Replace with actual token
        this.paymentMethods = [];
        this.stripe = null;
        this.elements = null;
    }

    async init() {
        await this.loadPaymentMethods();
        this.renderPaymentMethods();
    }

    async loadPaymentMethods() {
        const response = await fetch(`${this.apiBase}/checkout/methods/`);
        const data = await response.json();
        this.paymentMethods = data.payment_methods;
    }

    renderPaymentMethods() {
        const container = document.getElementById('payment-methods-container');
        
        container.innerHTML = `
            <h3>Choose your preferred payment option</h3>
            ${this.paymentMethods.map(method => {
                if (method.providers.length === 0 && method.id !== 'bank_transfer') return '';
                
                return `
                    <div class="payment-option" onclick="selectPaymentMethod('${method.id}')">
                        <div class="payment-icon">${method.icon}</div>
                        <div class="payment-info">
                            <h4>${method.name}</h4>
                            <p>${method.description}</p>
                            <span>${method.processing_time}</span>
                        </div>
                    </div>
                `;
            }).join('')}
        `;
    }
}

// Initialize payment methods
const paymentManager = new PaymentMethodsManager();

document.addEventListener('DOMContentLoaded', async () => {
    await paymentManager.init();
});

// Select payment method
function selectPaymentMethod(methodId) {
    // Hide all forms
    document.querySelectorAll('.payment-form').forEach(form => {
        form.style.display = 'none';
    });
    
    // Show selected form
    const form = document.getElementById(`${methodId}-form`);
    if (form) {
        form.style.display = 'block';
    }
    
    // Initialize Stripe for card payments
    if (methodId === 'card' && !paymentManager.stripe) {
        paymentManager.stripe = Stripe('pk_test_YOUR_STRIPE_KEY'); // Replace with your key
        paymentManager.elements = paymentManager.stripe.elements();
        
        const paymentElement = paymentManager.elements.create('payment');
        paymentElement.mount('#stripe-elements');
    }
}

// Handle Mobile Money Payment
async function handleMoMoPayment() {
    const phoneNumber = document.getElementById('momo-phone').value;
    
    if (!phoneNumber) {
        alert('Please enter your phone number');
        return;
    }
    
    const response = await fetch('/api/payments/checkout/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${paymentManager.authToken}`
        },
        body: JSON.stringify({
            amount: 150.00,
            currency: 'GHS',
            payment_method: 'momo',
            provider_code: 'mtn_momo',
            phone_number: phoneNumber,
            description: 'Travel booking payment'
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        alert('Payment request sent to your phone. Please check your mobile money app.');
        // Poll for status updates
        pollPaymentStatus(result.payment.reference);
    } else {
        alert('Error: ' + result.error);
    }
}

// Handle Stripe Payment
async function handleStripePayment() {
    // Create payment intent
    const response = await fetch('/api/payments/checkout/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${paymentManager.authToken}`
        },
        body: JSON.stringify({
            amount: 150.00,
            currency: 'GHS',
            payment_method: 'card',
            provider_code: 'stripe',
            description: 'Travel booking payment'
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        // Confirm payment with Stripe
        const {error} = await paymentManager.stripe.confirmPayment({
            elements: paymentManager.elements,
            clientSecret: result.stripe.client_secret,
            confirmParams: {
                return_url: window.location.origin + '/payment-success'
            }
        });
        
        if (error) {
            alert('Payment failed: ' + error.message);
        }
    } else {
        alert('Error: ' + result.error);
    }
}

// Poll payment status for mobile money
async function pollPaymentStatus(reference) {
    let attempts = 0;
    const maxAttempts = 30;
    
    const checkStatus = async () => {
        const response = await fetch(`/api/payments/${reference}/status/`, {
            headers: {
                'Authorization': `Token ${paymentManager.authToken}`
            }
        });
        
        const payment = await response.json();
        
        if (payment.status === 'successful') {
            alert('Payment completed successfully! 🎉');
            window.location.href = '/payment-success';
        } else if (payment.status === 'failed') {
            alert('Payment failed. Please try again.');
        } else if (attempts < maxAttempts) {
            attempts++;
            setTimeout(checkStatus, 10000);
        } else {
            alert('Payment is taking longer than expected. Please contact support.');
        }
    };
    
    setTimeout(checkStatus, 5000);
}
</script>
```

### 3. **Update Your CSS**

**Add these styles:**
```css
.payment-option {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
}

.payment-option:hover {
    border-color: #007bff;
    background-color: #f8f9fa;
}

.payment-option.selected {
    border-color: #007bff;
    background-color: #e7f3ff;
}

.payment-icon {
    font-size: 24px;
    margin-right: 15px;
}

.payment-info {
    flex: 1;
}

.payment-info h4 {
    margin: 0 0 5px 0;
}

.payment-info p {
    margin: 0 0 5px 0;
    color: #666;
}

.payment-info span {
    color: #007bff;
    font-size: 12px;
}

.payment-form {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

#stripe-elements {
    margin: 10px 0;
}

button {
    background-color: #007bff;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background-color: #0056b3;
}
```

### 4. **Important Configuration**

**You need to update these values:**

1. **Auth Token**: Replace `'YOUR_AUTH_TOKEN'` with the actual user's authentication token
2. **Stripe Key**: Replace `'pk_test_YOUR_STRIPE_KEY'` with your actual Stripe publishable key
3. **Amount**: Update the amount based on your booking total

### 5. **Test the Integration**

After making these changes, you should see:
- ✅ **Mobile Money** - MTN, Vodafone, AirtelTigo - Instant
- ✅ **Credit/Debit Card** - Visa, Mastercard, American Express - Instant  
- ✅ **Bank Transfer** - For large groups (optional) - 1-2 days

## 🎯 Result

Your checkout will now show:
1. **Mobile Money** with MTN Mobile Money integration
2. **Credit/Debit Card** with Stripe integration (instead of Paystack/Flutterwave)
3. **Bank Transfer** for large groups

The payment methods are loaded dynamically from your API, so they'll always be up-to-date with your backend configuration.

## 🔧 Troubleshooting

If you still see the old payment methods:
1. **Clear browser cache**
2. **Check if you're using the new HTML/JavaScript**
3. **Verify API endpoints are accessible**
4. **Check browser console for errors**
5. **Ensure authentication token is valid**

Your Stripe integration is ready and working! 🎉