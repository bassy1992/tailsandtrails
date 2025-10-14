import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient, User as ApiUser, RegisterRequest } from '@/lib/api';
import { useToast } from './ToastContext';

interface User {
  id: number;
  name: string;
  email: string;
  phone?: string;
  avatar?: string;
  memberSince: string;
  username: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string, returnUrl?: string) => Promise<boolean>;
  register: (data: RegisterRequest) => Promise<boolean>;
  logout: () => Promise<void>;
  loading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Helper function to transform API user to frontend user format
const transformUser = (apiUser: ApiUser): User => ({
  id: apiUser.id,
  name: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email,
  phone: apiUser.phone_number,
  memberSince: apiUser.created_at,
  username: apiUser.username,
  first_name: apiUser.first_name,
  last_name: apiUser.last_name,
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { showSuccess, showError, showInfo } = useToast();

  useEffect(() => {
    // Check for existing session on mount
    const initAuth = async () => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          apiClient.setToken(token);
          const apiUser = await apiClient.getProfile();
          const userData = transformUser(apiUser);
          setUser(userData);
          // Don't show welcome message on page refresh, only on actual login
        } catch (error) {
          // Token is invalid, clear it
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user');
          apiClient.setToken(null);
          showError('Your session has expired. Please log in again.');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, [showError]);

  const login = async (email: string, password: string, returnUrl?: string): Promise<boolean> => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.login({ email, password });
      const userData = transformUser(response.user);
      
      // Store token and user data
      apiClient.setToken(response.token);
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Show success message and redirect
      showSuccess(`Welcome back, ${userData.first_name}!`);
      navigate(returnUrl || '/dashboard');
      return true;
    } catch (error: any) {
      console.error('Login error:', error);
      
      // Handle specific error messages from Django
      let errorMessage = 'Login failed. Please try again.';
      
      if (error.email) {
        errorMessage = Array.isArray(error.email) ? error.email[0] : error.email;
      } else if (error.password) {
        errorMessage = Array.isArray(error.password) ? error.password[0] : error.password;
      } else if (error.non_field_errors) {
        errorMessage = Array.isArray(error.non_field_errors) ? error.non_field_errors[0] : error.non_field_errors;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setError(errorMessage);
      showError(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: RegisterRequest): Promise<boolean> => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.register(data);
      const userData = transformUser(response.user);
      
      // Store token and user data
      apiClient.setToken(response.token);
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Show success message and redirect to dashboard
      showSuccess(`Welcome to Tales and Trails Ghana, ${userData.first_name}!`);
      navigate('/dashboard');
      return true;
    } catch (error: any) {
      console.error('Registration error:', error);
      
      // Handle specific error messages from Django
      let errorMessage = 'Registration failed. Please try again.';
      
      if (error.email) {
        errorMessage = Array.isArray(error.email) ? error.email[0] : error.email;
      } else if (error.username) {
        errorMessage = Array.isArray(error.username) ? error.username[0] : error.username;
      } else if (error.password) {
        errorMessage = Array.isArray(error.password) ? error.password[0] : error.password;
      } else if (error.non_field_errors) {
        errorMessage = Array.isArray(error.non_field_errors) ? error.non_field_errors[0] : error.non_field_errors;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setError(errorMessage);
      showError(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await apiClient.logout();
      showInfo('You have been signed out successfully');
    } catch (error) {
      console.error('Logout error:', error);
      showInfo('You have been signed out');
    } finally {
      // Clear local state regardless of API call success
      setUser(null);
      apiClient.setToken(null);
      localStorage.removeItem('user');
      navigate('/');
    }
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    loading,
    error
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
