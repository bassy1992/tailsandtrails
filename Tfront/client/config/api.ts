// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
};

// Helper function to build API URLs
export const buildApiUrl = (endpoint: string): string => {
  // Remove leading slash if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  
  // If endpoint already includes the full API URL, return as is
  if (cleanEndpoint.startsWith('http')) {
    return cleanEndpoint;
  }
  
  // Build the full URL
  return `${API_CONFIG.API_URL}/${cleanEndpoint}`;
};

// Common headers for API requests
export const getApiHeaders = (includeAuth = false): HeadersInit => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  if (includeAuth) {
    const token = localStorage.getItem('authToken');
    if (token) {
      headers['Authorization'] = `Token ${token}`;
    }
  }

  return headers;
};

// API fetch wrapper with proper error handling
export const apiRequest = async (
  endpoint: string,
  options: RequestInit = {},
  includeAuth = false
): Promise<Response> => {
  const url = buildApiUrl(endpoint);
  const headers = {
    ...getApiHeaders(includeAuth),
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  return response;
};