# 🔐 Authentication Integration Guide

## Overview
Users must be logged in before they can purchase tickets. This guide shows how to implement this on the frontend.

## Authentication Flow

### 1. **Public Access (No Login Required)**
```javascript
// These endpoints work without authentication
GET /api/tickets/                    // Browse all tickets
GET /api/tickets/categories/         // Get categories
GET /api/tickets/venues/            // Get venues
GET /api/tickets/featured/          // Featured tickets
GET /api/tickets/<slug>/            // Ticket details
```

### 2. **Protected Endpoints (Login Required)**
```javascript
// These endpoints require authentication token
POST /api/tickets/purchase/direct/   // Create ticket purchase
GET  /api/tickets/purchases/user/    // User's purchases
POST /api/stripe/payment-intents/    // Create payment
GET  /api/stripe/payment-intents/    // List payments
POST /api/tickets/reviews/create/    // Create review
GET  /api/tickets/stats/user/        // User stats
```

## Frontend Implementation

### 1. **Login/Register**
```javascript
// Login
const loginUser = async (email, password) => {
  const response = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }
  throw new Error('Login failed');
};

// Register
const registerUser = async (userData) => {
  const response = await fetch('/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }
  throw new Error('Registration failed');
};
```

### 2. **Authenticated Requests**
```javascript
// Helper function for authenticated requests
const authenticatedFetch = async (url, options = {}) => {
  const token = localStorage.getItem('authToken');
  
  if (!token) {
    throw new Error('No authentication token');
  }
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`,
    ...options.headers
  };
  
  return fetch(url, { ...options, headers });
};

// Purchase ticket (requires authentication)
const purchaseTicket = async (ticketData) => {
  const response = await authenticatedFetch('/api/tickets/purchase/direct/', {
    method: 'POST',
    body: JSON.stringify(ticketData)
  });
  
  if (response.ok) {
    return response.json();
  }
  throw new Error('Purchase failed');
};
```

### 3. **Authentication Check**
```javascript
// Check if user is logged in
const isAuthenticated = () => {
  const token = localStorage.getItem('authToken');
  return !!token;
};

// Get current user
const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

// Logout
const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
  // Redirect to home or login page
};
```

### 4. **React Component Example**
```jsx
import React, { useState, useEffect } from 'react';

const TicketPurchase = ({ ticket }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  
  useEffect(() => {
    setIsLoggedIn(isAuthenticated());
  }, []);
  
  const handlePurchaseClick = () => {
    if (!isLoggedIn) {
      setShowLogin(true);
      return;
    }
    
    // Proceed with purchase
    purchaseTicket({
      ticket_id: ticket.id,
      quantity: 1,
      customer_name: getCurrentUser()?.first_name + ' ' + getCurrentUser()?.last_name,
      customer_email: getCurrentUser()?.email
    });
  };
  
  return (
    <div className="ticket-card">
      <h3>{ticket.title}</h3>
      <p>Price: GH₵{ticket.effective_price}</p>
      
      {isLoggedIn ? (
        <button onClick={handlePurchaseClick} className="btn-primary">
          Buy Ticket
        </button>
      ) : (
        <button onClick={() => setShowLogin(true)} className="btn-primary">
          Login to Buy Ticket
        </button>
      )}
      
      {showLogin && <LoginModal onClose={() => setShowLogin(false)} />}
    </div>
  );
};
```

### 5. **Route Protection**
```jsx
// Protected route component
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" />;
  }
  return children;
};

// Usage in router
<Routes>
  <Route path="/tickets" element={<TicketList />} />
  <Route path="/tickets/:slug" element={<TicketDetail />} />
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />
  
  {/* Protected routes */}
  <Route path="/my-tickets" element={
    <ProtectedRoute>
      <MyTickets />
    </ProtectedRoute>
  } />
  <Route path="/profile" element={
    <ProtectedRoute>
      <Profile />
    </ProtectedRoute>
  } />
</Routes>
```

## User Experience Flow

### 1. **Browse Tickets (Public)**
- Users can view all tickets without logging in
- See ticket details, prices, venues, categories
- Filter and search tickets

### 2. **Purchase Flow (Requires Login)**
```
User clicks "Buy Ticket"
  ↓
Is user logged in?
  ↓ NO
Show login/register modal
  ↓
User logs in/registers
  ↓
Redirect back to purchase
  ↓ YES
Show purchase form
  ↓
Process payment
  ↓
Show confirmation & ticket codes
```

### 3. **User Dashboard (Authenticated)**
- View purchase history
- See upcoming events
- Manage profile
- View ticket codes

## Error Handling

```javascript
// Handle authentication errors
const handleAuthError = (error) => {
  if (error.status === 401) {
    // Token expired or invalid
    logout();
    showLoginModal();
  } else if (error.status === 403) {
    // Permission denied
    showErrorMessage('Access denied');
  }
};

// Wrapper for API calls
const apiCall = async (url, options) => {
  try {
    const response = await authenticatedFetch(url, options);
    if (!response.ok) {
      handleAuthError(response);
    }
    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};
```

## Testing Authentication

Run the authentication test:
```bash
cd Tback
python test_authentication_requirements.py
```

Expected results:
- ✅ Public endpoints work without authentication
- ✅ Purchase endpoints require authentication (401)
- ✅ Login works and returns token
- ✅ Authenticated requests work with token

## Summary

🔐 **Authentication is now properly implemented:**
- ✅ Users must login before purchasing tickets
- ✅ Public browsing works without authentication
- ✅ Token-based authentication system
- ✅ Proper error handling for unauthorized access
- ✅ User session management

The system is ready for frontend integration with proper authentication flow!