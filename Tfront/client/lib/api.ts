/**
 * API client for Django backend integration
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

  async request<T>(
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
}

export const apiClient = new ApiClient(API_BASE_URL);

// Destinations API types
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface DestinationHighlight {
  highlight: string;
}

export interface DestinationInclude {
  item: string;
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
  highlights: DestinationHighlight[];
  includes: DestinationInclude[];
  pricing_tiers?: PricingTier[];
  price_category: string;
  is_featured: boolean;
}

export interface DestinationStats {
  total_destinations: number;
  categories_count: number;
  featured_destinations: number;
}

// Destinations API functions
// Tickets API types
export interface TicketCategory {
  id: number;
  name: string;
  slug: string;
  category_type: string;
  description: string;
  icon: string;
  order: number;
}

export interface Venue {
  id: number;
  name: string;
  slug: string;
  address: string;
  city: string;
  region: string;
  country: string;
  latitude?: number;
  longitude?: number;
  capacity?: number;
  description: string;
  image?: string;
  contact_phone?: string;
  contact_email?: string;
  website?: string;
}

export interface EventTicket {
  id: number;
  title: string;
  slug: string;
  category: TicketCategory;
  venue?: Venue;
  ticket_type: string;
  short_description: string;
  price: string;
  discount_price?: string;
  effective_price: string;
  discount_percentage: number;
  currency: string;
  available_quantity: number;
  total_quantity: number;
  event_date: string;
  event_end_date?: string;
  image?: string;
  status: string;
  is_featured: boolean;
  is_available: boolean;
  is_sold_out: boolean;
  rating: string;
  reviews_count: number;
  sales_count: number;
}

// Tickets API functions
export const ticketsApi = {
  async getTickets(params?: {
    search?: string;
    category?: number;
    venue?: number;
    min_price?: number;
    max_price?: number;
    start_date?: string;
    end_date?: string;
    available_only?: boolean;
    ordering?: string;
  }): Promise<EventTicket[]> {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append('search', params.search);
    if (params?.category) searchParams.append('category', params.category.toString());
    if (params?.venue) searchParams.append('venue', params.venue.toString());
    if (params?.min_price) searchParams.append('min_price', params.min_price.toString());
    if (params?.max_price) searchParams.append('max_price', params.max_price.toString());
    if (params?.start_date) searchParams.append('start_date', params.start_date);
    if (params?.end_date) searchParams.append('end_date', params.end_date);
    if (params?.available_only) searchParams.append('available_only', 'true');
    if (params?.ordering) searchParams.append('ordering', params.ordering);

    const url = `/tickets/${searchParams.toString() ? '?' + searchParams.toString() : ''}`;
    return apiClient.request<EventTicket[]>(url);
  },

  async getTicket(slug: string): Promise<EventTicket> {
    return apiClient.request<EventTicket>(`/tickets/${slug}/`);
  },

  async getCategories(): Promise<TicketCategory[]> {
    return apiClient.request<TicketCategory[]>('/tickets/categories/');
  },

  async getVenues(): Promise<Venue[]> {
    return apiClient.request<Venue[]>('/tickets/venues/');
  },

  async getFeaturedTickets(): Promise<EventTicket[]> {
    return apiClient.request<EventTicket[]>('/tickets/featured/');
  },

  async getUpcomingTickets(): Promise<EventTicket[]> {
    return apiClient.request<EventTicket[]>('/tickets/upcoming/');
  },

  async getPopularTickets(): Promise<EventTicket[]> {
    return apiClient.request<EventTicket[]>('/tickets/popular/');
  }
};

export const destinationsApi = {
  async getCategories(): Promise<Category[]> {
    return apiClient.request<Category[]>('/categories/');
  },

  async getDestinations(params?: {
    search?: string;
    category?: number;
    price_category?: string;
    duration_category?: string;
    ordering?: string;
  }): Promise<Destination[]> {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append('search', params.search);
    if (params?.category) searchParams.append('category', params.category.toString());
    if (params?.price_category) searchParams.append('price_category', params.price_category);
    if (params?.duration_category) searchParams.append('duration_category', params.duration_category);
    if (params?.ordering) searchParams.append('ordering', params.ordering);

    const url = `/destinations/${searchParams.toString() ? '?' + searchParams.toString() : ''}`;
    return apiClient.request<Destination[]>(url);
  },

  async getDestination(slug: string): Promise<Destination> {
    return apiClient.request<Destination>(`/destinations/${slug}/`);
  },

  async getStats(): Promise<DestinationStats> {
    return apiClient.request<DestinationStats>('/stats/');
  }
};