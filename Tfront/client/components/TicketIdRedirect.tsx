import { useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { validateAndRedirect, getPathType } from '../utils/idValidation';

interface IdRedirectProps {
  children: React.ReactNode;
}

/**
 * Component that validates IDs and redirects invalid ones for both tickets and destinations
 */
export default function IdRedirect({ children }: IdRedirectProps) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();

  // Determine if this is a destination or ticket path
  const pathType = getPathType(location.pathname);
  
  // Comprehensive ID validation and redirect
  const isValid = validateAndRedirect(id, location.pathname, navigate);
  
  // If validation failed, redirect is in progress - don't render children
  if (!isValid) {
    const itemType = pathType === 'destination' ? 'destination' : 'ticket';
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-ghana-gold mx-auto mb-4"></div>
          <p className="text-gray-600">Redirecting to available {itemType}...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}

// Export with legacy name for backward compatibility
export { IdRedirect as TicketIdRedirect };