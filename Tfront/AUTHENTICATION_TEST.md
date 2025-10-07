# 🔐 Frontend Authentication Test Guide

## Testing the Authentication-First Implementation

### 1. **Start the Servers**

**Backend (Django):**
```bash
cd Tback
python manage.py runserver
```

**Frontend (React):**
```bash
cd Tfront
npm run dev
# or
pnpm dev
```

### 2. **Test Authentication Flow**

#### **Step 1: Try to Access Tickets Without Login**
1. Open browser to `http://localhost:3000`
2. Click on "Tickets" in navigation
3. **Expected Result**: Should redirect to `/login` page with message "Please log in to access this page"

#### **Step 2: Create Account or Login**
1. On login page, click "Sign Up" if you don't have an account
2. Fill in registration form:
   - Email: `test@example.com`
   - Username: `testuser`
   - First Name: `Test`
   - Last Name: `User`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
3. Click "Sign Up"
4. **Expected Result**: Should redirect to dashboard with success message

#### **Step 3: Access Tickets After Login**
1. Click on "Tickets" in navigation
2. **Expected Result**: Should load tickets page with real data from API
3. Should see tickets, categories, and venues loaded from backend
4. Should see user avatar/name in top-right corner

#### **Step 4: Test Logout**
1. Click on user avatar in top-right
2. Click "Sign Out"
3. Try to access `/tickets` directly
4. **Expected Result**: Should redirect back to login page

### 3. **Verify API Calls**

Open browser developer tools (F12) and check Network tab:

#### **Before Login:**
- No API calls to `/api/tickets/` should succeed
- Should see 401 Unauthorized responses

#### **After Login:**
- Should see successful API calls with `Authorization: Token <token>` headers
- `/api/tickets/` should return 200 with ticket data
- `/api/tickets/categories/` should return 200 with categories

### 4. **Test Different Scenarios**

#### **Scenario A: Direct URL Access**
1. Logout if logged in
2. Try to visit `http://localhost:3000/tickets` directly
3. **Expected**: Redirect to login page

#### **Scenario B: Token Expiration**
1. Login successfully
2. In browser dev tools, go to Application > Local Storage
3. Delete the `auth_token` key
4. Try to access tickets page
5. **Expected**: Should redirect to login with "session expired" message

#### **Scenario C: Invalid Token**
1. Login successfully
2. In browser dev tools, change `auth_token` value to something invalid
3. Try to access tickets page
4. **Expected**: Should redirect to login and clear invalid token

### 5. **Expected User Experience**

#### **For New Users:**
```
Visit site → Click Tickets → Redirect to Login → 
Sign Up → Success → Access all ticket features
```

#### **For Returning Users:**
```
Visit site → Already logged in → Click Tickets → 
Immediate access to ticket features
```

#### **For Logged Out Users:**
```
Visit site → Click Tickets → Redirect to Login → 
Login → Return to tickets page
```

### 6. **Troubleshooting**

#### **If tickets don't load after login:**
1. Check browser console for errors
2. Verify backend is running on port 8000
3. Check Network tab for API call responses
4. Ensure token is being sent in Authorization header

#### **If login doesn't work:**
1. Check if user exists in Django admin
2. Verify password is correct
3. Check backend logs for authentication errors

#### **If redirects don't work:**
1. Check React Router configuration
2. Verify ProtectedRoute component is working
3. Check AuthContext state management

### 7. **Success Criteria**

✅ **Authentication Wall Working:**
- Cannot access tickets without login
- Proper redirect to login page
- Clear error messages

✅ **Login Flow Working:**
- Can create new account
- Can login with existing account
- Token stored and used for API calls

✅ **Ticket Features Working:**
- Tickets load after authentication
- Categories and venues load
- All ticket functionality accessible

✅ **Session Management Working:**
- Logout clears session
- Invalid tokens handled gracefully
- Session persists across page refreshes

### 8. **API Endpoints Status**

After successful implementation:

**🔐 Protected (Require Authentication):**
- `GET /api/tickets/` - List tickets
- `GET /api/tickets/categories/` - List categories  
- `GET /api/tickets/venues/` - List venues
- `POST /api/tickets/purchase/direct/` - Purchase tickets
- All other ticket-related endpoints

**🌐 Public (No Authentication Required):**
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration

This ensures complete authentication control over your ticket system! 🎉