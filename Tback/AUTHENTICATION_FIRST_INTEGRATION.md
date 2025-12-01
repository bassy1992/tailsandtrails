# 🔐 Authentication-First Integration Guide

## Overview
**ALL ticket features now require authentication.** Users must login before they can access any ticket-related functionality, including browsing tickets.

## Updated Authentication Flow

### 🚫 **No Public Access to Tickets**
All these endpoints now return **401 Unauthorized** without authentication:
```javascript
GET /api/tickets/                    // ❌ Requires login
GET /api/tickets/categories/         // ❌ Requires login  
GET /api/tickets/venues/            // ❌ Requires login
GET /api/tickets/featured/          // ❌ Requires login
GET /api/tickets/<slug>/            // ❌ Requires login
POST /api/tickets/purchase/direct/   // ❌ Requires login
```

### ✅ **Only Public Endpoints**
```javascript
POST /api/auth/login/               // ✅ Public access
POST /api/auth/register/            // ✅ Public access
```

## Frontend Implementation

### 1. **App Entry Point - Authentication Check**
```jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on app start
    const token = localStorage.getItem('authToken');
    if (token) {
      // Verify token is still valid
      verifyToken(token).then(valid => {
        setIsAuthenticated(valid);
        setIsLoading(false);
      });
    } else {
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        {isAuthenticated ? (
          // Authenticated routes - full app access
          <>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tickets" element={<TicketList />} />
            <Route path="/tickets/:slug" element={<TicketDetail />} />
            <Route path="/my-tickets" element={<MyTickets />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        ) : (
          // Unauthenticated routes - only auth pages
          <>
            <Route path="/login" element={<Login onLogin={setIsAuthenticated} />} />
            <Route path="/register" element={<Register onRegister={setIsAuthenticated} />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        )}
      </Routes>
    </Router>
  );
};

export default App;
```

### 2. **Login Component**
```jsx
import React, { useState } from 'react';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        onLogin(true);
      } else {
        const errorData = await response.json();
        setError(errorData.non_field_errors?.[0] || 'Login failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to access tickets
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            You must be logged in to view and purchase tickets
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          <div>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email address"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <div>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
          
          <div className="text-center">
            <a href="/register" className="text-indigo-600 hover:text-indigo-500">
              Don't have an account? Sign up
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
```

### 3. **Protected API Calls**
```javascript
// All API calls now require authentication
const authenticatedFetch = async (url, options = {}) => {
  const token = localStorage.getItem('authToken');
  
  if (!token) {
    // Redirect to login if no token
    window.location.href = '/login';
    throw new Error('No authentication token');
  }
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`,
    ...options.headers
  };
  
  const response = await fetch(url, { ...options, headers });
  
  if (response.status === 401) {
    // Token expired or invalid
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    window.location.href = '/login';
    throw new Error('Authentication expired');
  }
  
  return response;
};

// Example: Load tickets (requires authentication)
const loadTickets = async () => {
  try {
    const response = await authenticatedFetch('/api/tickets/');
    if (response.ok) {
      return response.json();
    }
    throw new Error('Failed to load tickets');
  } catch (error) {
    console.error('Error loading tickets:', error);
    throw error;
  }
};
```

### 4. **Navigation with Logout**
```jsx
const Navigation = ({ onLogout }) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  
  const handleLogout = async () => {
    try {
      await authenticatedFetch('/api/auth/logout/', { method: 'POST' });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      onLogout(false);
    }
  };
  
  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold">Ticket System</h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <span>Welcome, {user.first_name}!</span>
            <button
              onClick={handleLogout}
              className="text-gray-500 hover:text-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};
```

### 5. **Route Protection Middleware**
```jsx
// Higher-order component for route protection
const withAuth = (Component) => {
  return (props) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    
    useEffect(() => {
      const token = localStorage.getItem('authToken');
      if (token) {
        setIsAuthenticated(true);
      }
      setIsLoading(false);
    }, []);
    
    if (isLoading) {
      return <div>Loading...</div>;
    }
    
    if (!isAuthenticated) {
      return <Navigate to="/login" />;
    }
    
    return <Component {...props} />;
  };
};

// Usage
const ProtectedTicketList = withAuth(TicketList);
```

## User Experience Flow

### 1. **First Visit**
```
User visits any URL
  ↓
Check authentication
  ↓ NOT LOGGED IN
Redirect to /login
  ↓
Show login form with message:
"You must be logged in to view and purchase tickets"
```

### 2. **After Login**
```
User logs in successfully
  ↓
Store token in localStorage
  ↓
Redirect to dashboard/tickets
  ↓
All ticket features now accessible
```

### 3. **Session Management**
```
API call returns 401
  ↓
Clear stored token
  ↓
Redirect to login
  ↓
Show "Session expired" message
```

## Testing the Implementation

Run the authentication test to verify:
```bash
cd Tback
python test_authentication_requirements.py
```

Expected results:
- ✅ All ticket endpoints return 401 without authentication
- ✅ Only login/register endpoints are public
- ✅ Authenticated requests work properly

## Frontend URL Structure

### **Before Authentication:**
- `/login` - Login form
- `/register` - Registration form
- All other routes redirect to `/login`

### **After Authentication:**
- `/` - Dashboard/Home
- `/tickets` - Browse tickets
- `/tickets/:slug` - Ticket details
- `/my-tickets` - User's purchases
- `/profile` - User profile

## Summary

🔐 **Complete Authentication Wall:**
- ✅ No ticket browsing without login
- ✅ No public access to any ticket data
- ✅ Login required for ALL ticket features
- ✅ Clean separation between auth and app states
- ✅ Proper session management and token handling

Users must now create an account and login before they can access any ticket functionality. This provides maximum security and user tracking for your ticket system.