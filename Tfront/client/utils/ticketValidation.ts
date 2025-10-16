/**
 * Comprehensive Ticket ID Validation and Redirect Handling
 * GitHub Issue: 60110
 */

export interface TicketValidationResult {
  isValid: boolean;
  ticketId?: number;
  redirectPath?: string;
  errorMessage?: string;
  suggestedTickets?: number[];
}

export interface ValidTicket {
  id: number;
  title: string;
  slug?: string;
  status: 'active' | 'inactive';
}

/**
 * Current valid tickets in the system
 * This should be updated when new tickets are added
 */
const VALID_TICKETS: ValidTicket[] = [
  { id: 1, title: 'Ghana Music Festival 2024', status: 'active' },
  { id: 2, title: 'Black Stars vs Nigeria - AFCON Qualifier', status: 'active' }
];

/**
 * Get all valid ticket IDs
 */
export const getValidTicketIds = (): number[] => {
  return VALID_TICKETS.filter(ticket => ticket.status === 'active').map(ticket => ticket.id);
};

/**
 * Get default ticket ID (first active ticket)
 */
export const getDefaultTicketId = (): number => {
  const validIds = getValidTicketIds();
  return validIds.length > 0 ? validIds[0] : 1;
};

/**
 * Validate ticket ID and provide comprehensive feedback
 */
export const validateTicketId = (ticketId: string | number | undefined): TicketValidationResult => {
  // Handle undefined or null
  if (ticketId === undefined || ticketId === null) {
    return {
      isValid: false,
      errorMessage: 'No ticket ID provided',
      redirectPath: `/booking/${getDefaultTicketId()}`,
      suggestedTickets: getValidTicketIds()
    };
  }

  // Convert to number
  const numericId = typeof ticketId === 'string' ? parseInt(ticketId, 10) : ticketId;

  // Handle invalid number conversion
  if (isNaN(numericId) || numericId <= 0) {
    return {
      isValid: false,
      errorMessage: `Invalid ticket ID format: ${ticketId}`,
      redirectPath: `/booking/${getDefaultTicketId()}`,
      suggestedTickets: getValidTicketIds()
    };
  }

  // Check if ticket exists and is active
  const validIds = getValidTicketIds();
  if (validIds.includes(numericId)) {
    return {
      isValid: true,
      ticketId: numericId
    };
  }

  // Invalid ticket ID - provide helpful redirect
  return {
    isValid: false,
    errorMessage: `Ticket ID ${numericId} not found`,
    redirectPath: `/booking/${getDefaultTicketId()}`,
    suggestedTickets: validIds
  };
};

/**
 * Get redirect path for different route types
 */
export const getRedirectPath = (currentPath: string, validTicketId: number): string => {
  if (currentPath.includes('/booking/')) {
    return `/booking/${validTicketId}`;
  } else if (currentPath.includes('/ticket-booking/')) {
    return `/ticket-booking/${validTicketId}`;
  } else if (currentPath.includes('/tickets/')) {
    return `/tickets`;
  }
  return `/booking/${validTicketId}`;
};

/**
 * Comprehensive ticket ID validation with logging
 */
export const validateAndRedirect = (
  ticketId: string | number | undefined,
  currentPath: string,
  navigate: (path: string, options?: any) => void
): boolean => {
  const validation = validateTicketId(ticketId);

  if (!validation.isValid) {
    console.warn(`🔄 Ticket ID Validation Failed:`, {
      providedId: ticketId,
      error: validation.errorMessage,
      suggestedTickets: validation.suggestedTickets,
      currentPath
    });

    // Determine redirect path
    const redirectPath = validation.redirectPath || getRedirectPath(currentPath, getDefaultTicketId());
    
    console.log(`🔄 Redirecting to: ${redirectPath}`);
    
    // Perform redirect
    navigate(redirectPath, { replace: true });
    
    return false; // Validation failed, redirect performed
  }

  console.log(`✅ Ticket ID ${validation.ticketId} validated successfully`);
  return true; // Validation passed
};

/**
 * Check if API call should be made for this ticket ID
 */
export const shouldMakeApiCall = (ticketId: string | number | undefined): boolean => {
  const validation = validateTicketId(ticketId);
  return validation.isValid;
};

/**
 * Get error message for invalid ticket ID
 */
export const getTicketErrorMessage = (ticketId: string | number | undefined): string => {
  const validation = validateTicketId(ticketId);
  if (validation.isValid) {
    return '';
  }
  
  const suggestedIds = validation.suggestedTickets?.join(', ') || 'none available';
  return `${validation.errorMessage}. Available tickets: ${suggestedIds}`;
};

/**
 * Update valid tickets list (for dynamic updates)
 */
export const updateValidTickets = (tickets: ValidTicket[]): void => {
  VALID_TICKETS.length = 0;
  VALID_TICKETS.push(...tickets);
  console.log(`📋 Updated valid tickets:`, VALID_TICKETS.map(t => `${t.id}: ${t.title}`));
};