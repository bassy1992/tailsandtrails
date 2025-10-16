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
  max_people: number | null;
  price_per_person: string;
  group_size_display: string;
  is_active: boolean;
}

export interface PricingResponse {
  destination_id: number;
  destination_name: string;
  group_size: number;
  price_per_person: string;
  total_price: string;
  base_price: string;
  has_tiered_pricing: boolean;
  pricing_tiers: PricingTier[];
}

export interface Destination {
  id: number;
  name: string;
  slug: string;
  location: string;
  description: string;
  image: string;
  image_url: string;
  price: string;
  duration: string;
  duration_display: string;
  max_group_size: number;
  rating: string;
  reviews_count: number;
  category: Category;
  highlights: DestinationHighlight[];
  includes: DestinationInclude[];
  pricing_tiers: PricingTier[];
  has_tiered_pricing: boolean;
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

  async getDestinationPricing(destinationId: number, groupSize: number): Promise<PricingResponse> {
    return apiClient.request<PricingResponse>(`/destinations/${destinationId}/pricing/?group_size=${groupSize}`);
  },

  async getStats(): Promise<DestinationStats> {
    return apiClient.request<DestinationStats>('/stats/');
  }
};

// Gallery API types
export interface GalleryCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  gallery_count: number;
  video_count: number;
}

export interface GalleryImage {
  id: number;
  image_url: string;
  thumbnail_url: string;
  caption: string;
  camera_info?: string;
  is_main: boolean;
  order: number;
  created_at: string;
}

export interface ImageGallery {
  id: number;
  title: string;
  slug: string;
  description: string;
  location: string;
  category?: GalleryCategory;
  category_name?: string;
  destination_name?: string;
  photographer?: string;
  date_taken?: string;
  is_featured: boolean;
  images?: GalleryImage[];
  main_image_url: string;
  image_count: number;
  created_at: string;
}

export interface GalleryVideo {
  id: number;
  title: string;
  slug: string;
  description: string;
  video_url: string;
  thumbnail_url: string;
  duration: string;
  resolution?: string;
  location: string;
  category: GalleryCategory;
  destination_name?: string;
  videographer?: string;
  date_recorded?: string;
  equipment_info?: string;
  views: number;
  formatted_views: string;
  is_featured: boolean;
  tags: Array<{id: number; name: string; slug: string}>;
  created_at: string;
}

export interface GalleryStats {
  total_galleries: number;
  total_images: number;
  total_videos: number;
  featured_galleries: number;
  featured_videos: number;
  categories: number;
  total_views: number;
}

export interface GalleryMixedFeed {
  results: Array<(ImageGallery | GalleryVideo) & {type: 'gallery' | 'video'}>;
  total_galleries: number;
  total_videos: number;
  category: string;
}

// Gallery API functions
export const galleryApi = {
  async getCategories(): Promise<GalleryCategory[]> {
    return apiClient.request<GalleryCategory[]>('/gallery/categories/');
  },

  async getGalleries(params?: {
    category?: string;
    featured?: boolean;
    search?: string;
    ordering?: string;
  }): Promise<ImageGallery[]> {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.append('category', params.category);
    if (params?.featured) searchParams.append('featured', 'true');
    if (params?.search) searchParams.append('search', params.search);
    if (params?.ordering) searchParams.append('ordering', params.ordering);

    const url = `/gallery/galleries/${searchParams.toString() ? '?' + searchParams.toString() : ''}`;
    return apiClient.request<ImageGallery[]>(url);
  },

  async getGallery(slug: string): Promise<ImageGallery> {
    const url = `/gallery/galleries/${slug}/`;
    return apiClient.request<ImageGallery>(url);
  },

  // Legacy method for backward compatibility - now returns galleries as images
  async getImages(params?: {
    category?: string;
    featured?: boolean;
    search?: string;
    ordering?: string;
  }): Promise<ImageGallery[]> {
    return this.getGalleries(params);
  },

  async getImage(slug: string): Promise<ImageGallery> {
    return this.getGallery(slug);
  },

  async getVideos(params?: {
    category?: string;
    featured?: boolean;
    search?: string;
    ordering?: string;
  }): Promise<GalleryVideo[]> {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.append('category', params.category);
    if (params?.featured) searchParams.append('featured', 'true');
    if (params?.search) searchParams.append('search', params.search);
    if (params?.ordering) searchParams.append('ordering', params.ordering);

    const url = `/gallery/videos/${searchParams.toString() ? '?' + searchParams.toString() : ''}`;
    return apiClient.request<GalleryVideo[]>(url);
  },

  async getVideo(slug: string): Promise<GalleryVideo> {
    return apiClient.request<GalleryVideo>(`/gallery/videos/${slug}/`);
  },

  async getMixedFeed(params?: {
    category?: string;
    featured?: boolean;
    limit?: number;
  }): Promise<GalleryMixedFeed> {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.append('category', params.category);
    if (params?.featured) searchParams.append('featured', 'true');
    if (params?.limit) searchParams.append('limit', params.limit.toString());

    const url = `/gallery/feed/${searchParams.toString() ? '?' + searchParams.toString() : ''}`;
    return apiClient.request<GalleryMixedFeed>(url);
  },

  async getStats(): Promise<GalleryStats> {
    return apiClient.request<GalleryStats>('/gallery/stats/');
  }
};