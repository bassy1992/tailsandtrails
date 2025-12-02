/**
 * Shared code between client and server
 * API types and utilities for Django backend integration
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// User types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  date_of_birth?: string;
  created_at: string;
}

// Auth API types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  date_of_birth?: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  token: string;
}

export interface ApiError {
  message?: string;
  [key: string]: any;
}

// Destination types
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface PricingTier {
  id: number;
  min_people: number;
  max_people: number;
  total_price: string;
  price_per_person: string;
}

export interface Destination {
  id: number;
  name: string;
  slug: string;
  location: string;
  description: string;
  image: string;
  price: string;
  duration: string;
  duration_display: string;
  max_group_size: number;
  start_date?: string;
  end_date?: string;
  rating: string;
  reviews_count: number;
  category: Category;
  highlights: Array<{ highlight: string }>;
  includes: Array<{ item: string }>;
  images?: Array<{ image_url: string; alt_text: string; is_primary: boolean }>;
  pricing_tiers?: PricingTier[];
  addon_options?: any[];
  experience_addons?: any[];
  price_category: string;
  is_featured: boolean;
}

export interface Review {
  id: number;
  rating: number;
  title: string;
  comment: string;
  user_name: string;
  is_verified: boolean;
  created_at: string;
}

export interface Stats {
  total_destinations: number;
  categories_count: number;
  featured_destinations: number;
}

// Payment types
export interface PaymentListItem {
  payment_id: string;
  reference: string;
  amount: string;
  currency: string;
  payment_method: string;
  payment_method_display: string;
  status: string;
  status_display: string;
  created_at: string;
  processed_at: string | null;
}

export interface BookingDetails {
  type?: 'destination' | 'ticket';
  destination?: {
    name: string;
    location: string;
    duration: string;
    image_url?: string;
  };
  ticket?: {
    id: number;
    title: string;
    quantity: number;
    price_per_ticket: number;
  };
  travelers?: {
    adults: number;
    children: number;
  };
  selected_date?: string;
  selected_options?: {
    accommodation?: {
      name: string;
      price: number;
    };
    transport?: {
      name: string;
      price: number;
    };
    meals?: {
      name: string;
      price: number;
    };
  };
  pricing?: {
    base_total: number;
    options_total: number;
    final_total: number;
  };
  user_info?: {
    name: string;
    email: string;
    phone: string;
  };
}

export interface PaymentDetail {
  payment_id: string;
  reference: string;
  user: string | null;
  booking: number | null;
  amount: string;
  currency: string;
  payment_method: string;
  payment_method_display: string;
  provider: {
    id: number;
    name: string;
    code: string;
    is_active: boolean;
  } | null;
  phone_number: string;
  status: string;
  status_display: string;
  external_reference: string;
  description: string;
  created_at: string;
  updated_at: string;
  processed_at: string | null;
  metadata?: {
    booking_details?: BookingDetails;
  };
}

// API utility functions
class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('auth_token');
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Token ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw error;
    }

    return response.json();
  }

  // Auth endpoints
  async login(data: LoginRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async register(data: RegisterRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async logout(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/auth/logout/', {
      method: 'POST',
    });
  }

  async getProfile(): Promise<User> {
    return this.request<User>('/auth/profile/');
  }

  async updateProfile(data: Partial<User>): Promise<{ message: string; user: User }> {
    return this.request<{ message: string; user: User }>('/auth/profile/update/', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Destination endpoints
  async getCategories(): Promise<Category[]> {
    return this.request<Category[]>('/categories/');
  }

  async getDestinations(params?: {
    search?: string;
    category?: number;
    duration?: string;
    price_category?: string;
    ordering?: string;
  }): Promise<Destination[]> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) queryParams.append(key, String(value));
      });
    }
    const query = queryParams.toString();
    return this.request<Destination[]>(`/destinations/${query ? `?${query}` : ''}`);
  }

  async getDestination(slug: string): Promise<Destination> {
    return this.request<Destination>(`/destinations/${slug}/`);
  }

  async getDestinationReviews(destinationId: number): Promise<Review[]> {
    return this.request<Review[]>(`/destinations/${destinationId}/reviews/`);
  }

  async getStats(): Promise<Stats> {
    return this.request<Stats>('/stats/');
  }

  // Payment endpoints
  async getPaymentStatus(reference: string): Promise<PaymentDetail> {
    return this.request<PaymentDetail>(`/payments/status/${reference}/`);
  }

  async getUserPayments(): Promise<PaymentListItem[]> {
    return this.request<PaymentListItem[]>('/payments/');
  }

  async getPaymentDetail(reference: string): Promise<PaymentDetail> {
    return this.request<PaymentDetail>(`/payments/${reference}/`);
  }

  async createCheckoutPayment(data: {
    amount: number;
    currency: string;
    payment_method: string;
    provider_code: string;
    phone_number?: string;
    description?: string;
    booking_details?: any;
  }): Promise<{ success: boolean; payment: PaymentDetail; message?: string; error?: string }> {
    return this.request<{ success: boolean; payment: PaymentDetail; message?: string; error?: string }>(
      '/payments/checkout/',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }
}

export const apiClient = new ApiClient(API_BASE_URL);

/**
 * Example response type for /api/demo
 */
export interface DemoResponse {
  message: string;
}
