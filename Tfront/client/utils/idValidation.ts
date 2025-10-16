

/**
 * Comprehensive ID Validation and Redirect Handling for Tickets and Destinations
 * GitHub Issue: 60110
 */

export interface ValidationResult {
  isValid: boolean;
  id?: number;
  redirectPath?: string;
  errorMessage?: string;
  suggestedIds?: number[];
}

export interface ValidItem {
  id: number;
  title: string;
  slug?: string;
  status: 'active' | 'inactive';
}

// Dynamic destinations cache
let cachedDestinations: ValidItem[] | null = null;
let lastFetchTime = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

/**
 * Current valid tickets in the system
 */
const VALID_TICKETS: ValidItem[] = [
  { id: 1, title: 'Ghana Music Festival 2024', status: 'active' },
  { id: 2, title: 'Black Stars vs Nigeria - AFCON Qualifier', status: 'active' }
];

/**
 * Current valid destinations in the system
 */
const VALID_DESTINATIONS: ValidItem[] = [
  { id: 1, title: 'Kakum National Park Canopy Walk', slug: 'kakum-national-park-canopy-walk', status: 'active' },
  { id: 2, title: 'Cape Coast Castle Tour', slug: 'cape-coast-castle-tour', status: 'active' },
  { id: 3, title: 'Mole National Park Safari', slug: 'mole-national-park-safari', status: 'active' },
  { id: 4, title: 'Labadi Beach Experience', slug: 'labadi-beach-experience', status: 'active' },
  { id: 5, title: 'Kumasi Cultural Heritage Tour', slug: 'kumasi-cultural-heritage-tour', status: 'active' },
  { id: 6, title: 'Volta Region Waterfalls Adventure', slug: 'volta-region-waterfalls-adventure', status: 'active' },
  { id: 7, title: 'Tent Xscape', slug: 'tent-xscape', status: 'active' }
];

/**
 * Get all valid ticket IDs
 */
export const getValidTicketIds = (): number[] => {
  return VALID_TICKETS.filter(ticket => ticket.status === 'active').map(ticket => ticket.id);
};

/**
 * Fetch destinations from API and cache them
 */
const fetchDestinationsFromAPI = async (): Promise<ValidItem[]> => {
  try {
    // Lazy load the API to avoid circular dependencies
    const apiModule = await import('../lib/api');
    const destinations = await apiModule.destinationsApi.getDestinations();
    
    return destinations.map(dest => ({
      id: dest.id,
      title: dest.title,
      slug: dest.slug,
      status: 'active' as const
    }));
  } catch (error) {
    console.warn('Failed to fetch destinations from API, using fallback:', error);
    return VALID_DESTINATIONS;
  }
};

/**
 * Get all valid destination IDs (with API fallback)
 */
export const getValidDestinationIds = async (): Promise<number[]> => {
  const destinations = await getValidDestinations();
  return destinations.filter(dest => dest.status === 'active').map(dest => dest.id);
};

/**
 * Get valid destinations with caching
 */
export const getValidDestinations = async (): Promise<ValidItem[]> => {
  const now = Date.now();
  
  // Return cached data if it's still fresh
  if (cachedDestinations && (now - lastFetchTime) < CACHE_DURATION) {
    return cachedDestinations;
  }
  
  // Fetch fresh data
  try {
    cachedDestinations = await fetchDestinationsFromAPI();
    lastFetchTime = now;
    return cachedDestinations;
  } catch (error) {
    console.warn('Failed to fetch destinations, using hardcoded fallback');
    return VALID_DESTINATIONS;
  }
};

/**
 * Synchronous version for backward compatibility (uses cached data or fallback)
 */
export const getValidDestinationIdsSync = (): number[] => {
  const destinations = cachedDestinations || VALID_DESTINATIONS;
  return destinations.filter(dest => dest.status === 'active').map(dest => dest.id);
};

/**
 * Get default ticket ID (first active ticket)
 */
export const getDefaultTicketId = (): number => {
  const validIds = getValidTicketIds();
  return validIds.length > 0 ? validIds[0] : 1;
};

/**
 * Get default destination ID (first active destination)
 */
export const getDefaultDestinationId = async (): Promise<number> => {
  const validIds = await getValidDestinationIds();
  return validIds.length > 0 ? validIds[0] : 1;
};

/**
 * Synchronous version for backward compatibility
 */
export const getDefaultDestinationIdSync = (): number => {
  const validIds = getValidDestinationIdsSync();
  return validIds.length > 0 ? validIds[0] : 1;
};

/**
 * Determine if the current path is for destinations or tickets
 */
export const getPathType = (currentPath: string): 'destination' | 'ticket' => {
  if (currentPath.includes('/booking/') || currentPath.includes('/destinations/')) {
    return 'destination';
  }
  return 'ticket';
};

/**
 * Validate ID based on path type and provide comprehensive feedback (async version)
 */
export const validateIdAsync = async (id: string | number | undefined, pathType: 'destination' | 'ticket'): Promise<ValidationResult> => {
  console.log(`🚀 validateIdAsync called with ID: "${id}" (${typeof id}), pathType: ${pathType}`);
  
  const isDestination = pathType === 'destination';
  const validIds = isDestination ? await getValidDestinationIds() : getValidTicketIds();
  const defaultId = isDestination ? await getDefaultDestinationId() : getDefaultTicketId();
  const itemType = isDestination ? 'destination' : 'ticket';
  const defaultPath = isDestination ? `/booking/${defaultId}` : `/ticket-booking/${defaultId}`;

  // Handle undefined or null
  if (id === undefined || id === null) {
    return {
      isValid: false,
      errorMessage: `No ${itemType} ID provided`,
      redirectPath: defaultPath,
      suggestedIds: validIds
    };
  }

  // Handle string IDs (could be slugs or numeric strings)
  if (typeof id === 'string') {
    // Try to parse as number first
    const numericId = parseInt(id, 10);
    
    // If it's a valid number, validate as numeric ID
    if (!isNaN(numericId) && numericId > 0) {
      if (validIds.includes(numericId)) {
        console.log(`✅ Valid numeric ID: ${numericId}`);
        return {
          isValid: true,
          id: numericId
        };
      }
    } else {
      // It's likely a slug, validate against slug list
      if (isDestination) {
        const destinations = await getValidDestinations();
        const destinationBySlug = destinations.find(dest => 
          dest.slug === id && dest.status === 'active'
        );
        if (destinationBySlug) {
          console.log(`✅ Valid slug "${id}" -> ID ${destinationBySlug.id}`);
          return {
            isValid: true,
            id: destinationBySlug.id
          };
        }
      }
      // For tickets, we don't have slug support yet, so treat as invalid
    }
  } else {
    // Handle numeric ID
    if (validIds.includes(id)) {
      return {
        isValid: true,
        id: id
      };
    }
  }

  // Invalid ID - provide helpful redirect
  return {
    isValid: false,
    errorMessage: `${itemType.charAt(0).toUpperCase() + itemType.slice(1)} ID ${id} not found`,
    redirectPath: defaultPath,
    suggestedIds: validIds
  };
};

/**
 * Synchronous validate ID (for backward compatibility, uses cached data)
 */
export const validateId = (id: string | number | undefined, pathType: 'destination' | 'ticket'): ValidationResult => {
  console.log(`🚀 validateId called with ID: "${id}" (${typeof id}), pathType: ${pathType}`);
  
  const isDestination = pathType === 'destination';
  const validIds = isDestination ? getValidDestinationIdsSync() : getValidTicketIds();
  const defaultId = isDestination ? getDefaultDestinationIdSync() : getDefaultTicketId();
  const itemType = isDestination ? 'destination' : 'ticket';
  const defaultPath = isDestination ? `/booking/${defaultId}` : `/ticket-booking/${defaultId}`;

  // Handle undefined or null
  if (id === undefined || id === null) {
    return {
      isValid: false,
      errorMessage: `No ${itemType} ID provided`,
      redirectPath: defaultPath,
      suggestedIds: validIds
    };
  }

  // Handle string IDs (could be slugs or numeric strings)
  if (typeof id === 'string') {
    // Try to parse as number first
    const numericId = parseInt(id, 10);
    
    // If it's a valid number, validate as numeric ID
    if (!isNaN(numericId) && numericId > 0) {
      if (validIds.includes(numericId)) {
        console.log(`✅ Valid numeric ID: ${numericId}`);
        return {
          isValid: true,
          id: numericId
        };
      }
    } else {
      // It's likely a slug, validate against slug list
      if (isDestination) {
        const destinations = cachedDestinations || VALID_DESTINATIONS;
        const destinationBySlug = destinations.find(dest => 
          dest.slug === id && dest.status === 'active'
        );
        if (destinationBySlug) {
          console.log(`✅ Valid slug "${id}" -> ID ${destinationBySlug.id}`);
          return {
            isValid: true,
            id: destinationBySlug.id
          };
        }
      }
      // For tickets, we don't have slug support yet, so treat as invalid
    }
  } else {
    // Handle numeric ID
    if (validIds.includes(id)) {
      return {
        isValid: true,
        id: id
      };
    }
  }

  // Invalid ID - provide helpful redirect
  return {
    isValid: false,
    errorMessage: `${itemType.charAt(0).toUpperCase() + itemType.slice(1)} ID ${id} not found`,
    redirectPath: defaultPath,
    suggestedIds: validIds
  };
};

/**
 * Legacy function for backward compatibility
 */
export const validateTicketId = (ticketId: string | number | undefined): ValidationResult => {
  return validateId(ticketId, 'ticket');
};

/**
 * Get redirect path for different route types
 */
export const getRedirectPath = (currentPath: string, validId: number): string => {
  const pathType = getPathType(currentPath);
  
  if (currentPath.includes('/booking/')) {
    return `/booking/${validId}`;
  } else if (currentPath.includes('/ticket-booking/')) {
    return `/ticket-booking/${validId}`;
  } else if (currentPath.includes('/tickets/')) {
    return `/tickets`;
  } else if (currentPath.includes('/destinations/')) {
    return `/destinations/${validId}`;
  }
  
  // Default based on path type
  return pathType === 'destination' ? `/booking/${validId}` : `/ticket-booking/${validId}`;
};

/**
 * Comprehensive ID validation with logging for both tickets and destinations (async version)
 */
export const validateAndRedirectAsync = async (
  id: string | number | undefined,
  currentPath: string,
  navigate: (path: string, options?: any) => void
): Promise<boolean> => {
  const pathType = getPathType(currentPath);
  const validation = await validateIdAsync(id, pathType);

  if (!validation.isValid) {
    console.warn(`🔄 ${pathType.charAt(0).toUpperCase() + pathType.slice(1)} ID Validation Failed:`, JSON.stringify({
      providedId: id,
      error: validation.errorMessage,
      suggestedIds: validation.suggestedIds,
      currentPath,
      pathType
    }, null, 2));

    // Determine redirect path
    const defaultId = pathType === 'destination' ? await getDefaultDestinationId() : getDefaultTicketId();
    const redirectPath = validation.redirectPath || getRedirectPath(currentPath, defaultId);
    
    console.log(`🔄 Redirecting to: ${redirectPath}`);
    
    // Perform redirect
    navigate(redirectPath, { replace: true });
    
    return false; // Validation failed, redirect performed
  }

  console.log(`✅ ${pathType.charAt(0).toUpperCase() + pathType.slice(1)} ID ${validation.id} validated successfully`);
  return true; // Validation passed
};

/**
 * Synchronous version for backward compatibility (uses cached data)
 */
export const validateAndRedirect = (
  id: string | number | undefined,
  currentPath: string,
  navigate: (path: string, options?: any) => void
): boolean => {
  const pathType = getPathType(currentPath);
  const validation = validateId(id, pathType);

  if (!validation.isValid) {
    console.warn(`🔄 ${pathType.charAt(0).toUpperCase() + pathType.slice(1)} ID Validation Failed:`, JSON.stringify({
      providedId: id,
      error: validation.errorMessage,
      suggestedIds: validation.suggestedIds,
      currentPath,
      pathType
    }, null, 2));

    // Determine redirect path
    const defaultId = pathType === 'destination' ? getDefaultDestinationIdSync() : getDefaultTicketId();
    const redirectPath = validation.redirectPath || getRedirectPath(currentPath, defaultId);
    
    console.log(`🔄 Redirecting to: ${redirectPath}`);
    
    // Perform redirect
    navigate(redirectPath, { replace: true });
    
    return false; // Validation failed, redirect performed
  }

  console.log(`✅ ${pathType.charAt(0).toUpperCase() + pathType.slice(1)} ID ${validation.id} validated successfully`);
  return true; // Validation passed
};

/**
 * Check if API call should be made for this ID
 */
export const shouldMakeApiCall = (id: string | number | undefined, pathType: 'destination' | 'ticket'): boolean => {
  const validation = validateId(id, pathType);
  return validation.isValid;
};

/**
 * Legacy function for backward compatibility
 */
export const shouldMakeApiCallForTicket = (ticketId: string | number | undefined): boolean => {
  return shouldMakeApiCall(ticketId, 'ticket');
};

/**
 * Get error message for invalid ID
 */
export const getErrorMessage = (id: string | number | undefined, pathType: 'destination' | 'ticket'): string => {
  const validation = validateId(id, pathType);
  if (validation.isValid) {
    return '';
  }
  
  const itemType = pathType === 'destination' ? 'destinations' : 'tickets';
  const suggestedIds = validation.suggestedIds?.join(', ') || 'none available';
  return `${validation.errorMessage}. Available ${itemType}: ${suggestedIds}`;
};

/**
 * Legacy function for backward compatibility
 */
export const getTicketErrorMessage = (ticketId: string | number | undefined): string => {
  return getErrorMessage(ticketId, 'ticket');
};

/**
 * Update valid tickets list (for dynamic updates)
 */
export const updateValidTickets = (tickets: ValidItem[]): void => {
  VALID_TICKETS.length = 0;
  VALID_TICKETS.push(...tickets);
  console.log(`📋 Updated valid tickets:`, VALID_TICKETS.map(t => `${t.id}: ${t.title}`));
};

/**
 * Update valid destinations list (for dynamic updates)
 */
export const updateValidDestinations = (destinations: ValidItem[]): void => {
  VALID_DESTINATIONS.length = 0;
  VALID_DESTINATIONS.push(...destinations);
  console.log(`📋 Updated valid destinations:`, VALID_DESTINATIONS.map(d => `${d.id}: ${d.title}`));
};