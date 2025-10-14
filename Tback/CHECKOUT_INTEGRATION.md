# 🛒 Checkout Payment Integration Guide

This guide shows how to integrate the payment system into your checkout process, including Stripe for international card payments.

## 🎯 Available Payment Methods

Your checkout now supports these payment options:

### 📱 **Mobile Money** (Ghana)
- **MTN Mobile Money** - Instant payments via phone
- **Vodafone Cash** - Available when activated
- **AirtelTigo Money** - Available when activated
- **Currency**: GHS (Ghana Cedis)
- **Processing**: Instant

### 💳 **Credit/Debit Cards** (International)
- **Stripe** - Visa, Mastercard, American Express
- **Currencies**: GHS, USD, EUR
- **Processing**: Instant
- **Security**: PCI compliant

### 🏦 **Bank Transfer** (Large Groups)
- **Manual processing** for large group bookings
- **Currencies**: GHS, USD
- **Processing**: 1-2 business days

## 🔗 API Endpoints

### 1. Get Payment Methods
```http
GET /api/payments/checkout/methods/
```

**Response:**
```json
{
  "payment_methods": [
    {
      "id": "mobile_money",
      "name": "Mobile Money",
      "description": "MTN, Vodafone, AirtelTigo",
      "icon": "📱",
      "processing_time": "Instant",
      "currencies": ["GHS"],
      "providers": [
        {
          "id": 4,
          "name": "MTN Mobile Money",
          "code": "mtn_momo"
        }
      ]
    },
    {
      "id": "card",
      "name": "Credit/Debit Card",
      "description": "Visa, Mastercard, American Express",
      "icon": "💳",
      "processing_time": "Instant",
      "currencies": ["GHS", "USD", "EUR"],
      "providers": [
        {
          "id": 3,
          "name": "Stripe",
          "code": "stripe"
        }
      ]
    },
    {
      "id": "bank_transfer",
      "name": "Bank Transfer",
      "description": "For large groups (optional)",
      "icon": "🏦",
      "processing_time": "1-2 days",
      "currencies": ["GHS", "USD"],
      "providers": []
    }
  ],
  "default_currency": "GHS",
  "supported_currencies": ["GHS", "USD", "EUR"]
}
```

### 2. Create Checkout Payment
```http
POST /api/payments/checkout/create/
Authorization: Token your-auth-token
Content-Type: application/json
```

**Request Body:**
```json
{
  "amount": 150.00,
  "currency": "GHS",
  "payment_method": "momo",
  "provider_code": "mtn_momo",
  "phone_number": "+233244123456",
  "booking_id": 123,
  "description": "Travel booking payment"
}
```

**Response (MTN MoMo):**
```json
{
  "success": true,
  "payment": {
    "payment_id": "uuid-here",
    "reference": "PAY12345678",
    "amount": "150.00",
    "currency": "GHS",
    "status": "processing",
    "payment_method": "momo",
    "created_at": "2024-01-01T12:00:00Z"
  },
  "message": "Payment request sent to customer phone"
}
```

**Response (Stripe):**
```json
{
  "success": true,
  "payment": {
    "payment_id": "uuid-here",
    "reference": "PAY12345678",
    "amount": "50.00",
    "currency": "USD",
    "status": "processing",
    "payment_method": "card"
  },
  "stripe": {
    "client_secret": "pi_1234567890_secret_...",
    "publishable_key": "pk_test_..."
  }
}
```

## 🖥️ Frontend Integration

### 1. **Fetch Payment Methods**
```javascript
// Get available payment methods
const getPaymentMethods = async () => {
  const response = await fetch('/api/payments/checkout/methods/');
  const data = await response.json();
  return data.payment_methods;
};
```

### 2. **Mobile Money Payment**
```javascript
// Create MTN MoMo payment
const createMoMoPayment = async (paymentData) => {
  const response = await fetch('/api/payments/checkout/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${authToken}`
    },
    body: JSON.stringify({
      amount: paymentData.amount,
      currency: 'GHS',
      payment_method: 'momo',
      provider_code: 'mtn_momo',
      phone_number: paymentData.phoneNumber,
      booking_id: paymentData.bookingId,
      description: 'Travel booking payment'
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    // Show success message to user
    // Payment request sent to phone
    showMessage('Payment request sent to your phone. Please check your mobile money app.');
    
    // Poll for payment status
    pollPaymentStatus(result.payment.reference);
  } else {
    showError(result.error);
  }
};
```

### 3. **Stripe Card Payment**
```javascript
// Initialize Stripe
const stripe = Stripe('pk_test_your_publishable_key');

// Create Stripe payment
const createStripePayment = async (paymentData) => {
  // 1. Create payment intent
  const response = await fetch('/api/payments/checkout/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${authToken}`
    },
    body: JSON.stringify({
      amount: paymentData.amount,
      currency: paymentData.currency,
      payment_method: 'card',
      provider_code: 'stripe',
      booking_id: paymentData.bookingId,
      description: 'Travel booking payment'
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    // 2. Confirm payment with Stripe Elements
    const {error} = await stripe.confirmPayment({
      elements,
      clientSecret: result.stripe.client_secret,
      confirmParams: {
        return_url: `${window.location.origin}/payment-success`
      }
    });
    
    if (error) {
      showError(error.message);
    }
  } else {
    showError(result.error);
  }
};
```

### 4. **Payment Status Polling**
```javascript
// Poll payment status for mobile money
const pollPaymentStatus = async (paymentReference) => {
  const maxAttempts = 30; // 5 minutes
  let attempts = 0;
  
  const checkStatus = async () => {
    try {
      const response = await fetch(`/api/payments/${paymentReference}/status/`, {
        headers: {
          'Authorization': `Token ${authToken}`
        }
      });
      
      const payment = await response.json();
      
      if (payment.status === 'successful') {
        showSuccess('Payment completed successfully!');
        redirectToSuccess();
      } else if (payment.status === 'failed') {
        showError('Payment failed. Please try again.');
      } else if (payment.status === 'cancelled') {
        showError('Payment was cancelled.');
      } else if (attempts < maxAttempts) {
        // Continue polling
        attempts++;
        setTimeout(checkStatus, 10000); // Check every 10 seconds
      } else {
        showError('Payment is taking longer than expected. Please contact support.');
      }
    } catch (error) {
      console.error('Error checking payment status:', error);
    }
  };
  
  // Start polling after 5 seconds
  setTimeout(checkStatus, 5000);
};
```

## 🎨 Checkout UI Components

### **Payment Method Selection**
```html
<div class="payment-methods">
  <h3>Choose your preferred payment option</h3>
  
  <!-- Mobile Money -->
  <div class="payment-option" data-method="mobile_money">
    <div class="payment-icon">📱</div>
    <div class="payment-info">
      <h4>Mobile Money</h4>
      <p>MTN, Vodafone, AirtelTigo</p>
      <span class="processing-time">Instant</span>
    </div>
  </div>
  
  <!-- Credit/Debit Cards -->
  <div class="payment-option" data-method="card">
    <div class="payment-icon">💳</div>
    <div class="payment-info">
      <h4>Credit/Debit Card</h4>
      <p>Visa, Mastercard, American Express</p>
      <span class="processing-time">Instant</span>
    </div>
  </div>
  
  <!-- Bank Transfer -->
  <div class="payment-option" data-method="bank_transfer">
    <div class="payment-icon">🏦</div>
    <div class="payment-info">
      <h4>Bank Transfer</h4>
      <p>For large groups (optional)</p>
      <span class="processing-time">1-2 days</span>
    </div>
  </div>
</div>
```

### **Mobile Money Form**
```html
<div id="momo-form" class="payment-form">
  <h4>🇬🇭 MTN Mobile Money</h4>
  <div class="form-group">
    <label>Phone Number</label>
    <input type="tel" id="momo-phone" placeholder="+233244123456" required>
    <small>Enter your MTN Mobile Money number</small>
  </div>
  <button onclick="processMoMoPayment()">Pay GHS 150.00</button>
</div>
```

### **Stripe Card Form**
```html
<div id="stripe-form" class="payment-form">
  <h4>💳 Credit/Debit Card</h4>
  <div id="stripe-elements">
    <!-- Stripe Elements will be mounted here -->
  </div>
  <button onclick="processStripePayment()">Pay $50.00</button>
</div>
```

## 🔄 Payment Flow

### **Mobile Money Flow**
1. User selects Mobile Money
2. Enters phone number
3. Clicks "Pay" button
4. API creates payment and sends MTN request
5. User receives prompt on phone
6. User approves payment in MTN app
7. System receives callback and updates status
8. User sees success message

### **Stripe Card Flow**
1. User selects Credit/Debit Card
2. Enters card details in Stripe Elements
3. Clicks "Pay" button
4. API creates Stripe Payment Intent
5. Frontend confirms payment with Stripe
6. User completes 3D Secure if required
7. Payment processed instantly
8. User redirected to success page

## 🛡️ Security Features

- **Authentication required** for all payment operations
- **HTTPS only** for card payments
- **PCI compliance** through Stripe
- **Phone number validation** for mobile money
- **Amount validation** and currency checks
- **Provider verification** before processing

## 📱 Mobile Optimization

- **Responsive design** for all screen sizes
- **Touch-friendly** payment method selection
- **Mobile number input** with proper keyboard
- **Loading states** during payment processing
- **Clear error messages** and success feedback

## 🚀 Ready to Use!

Your checkout now supports:
- ✅ **MTN Mobile Money** for Ghana customers
- ✅ **Stripe** for international card payments
- ✅ **Bank Transfer** for large group bookings
- ✅ **Multi-currency** support (GHS, USD, EUR)
- ✅ **Real-time status** updates
- ✅ **Secure processing** with proper validation

The payment system is production-ready and can handle your travel booking payments efficiently! 🎉