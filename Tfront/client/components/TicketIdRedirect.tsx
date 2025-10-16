import { useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { validateAndRedirect } from '../utils/ticketValidation';

interface TicketIdRedirectProps {
  children: React.ReactNode;
}

/**
 * Component that validates ticket IDs and redirects invalid ones
 */
export default function TicketIdRedirect({ children }: TicketIdRedirectProps) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();

  // Comprehensive ticket ID validation and redirect
  const isValid = validateAndRedirect(id, location.pathname, navigate);
  
  // If validation failed, redirect is in progress - don't render children
  if (!isValid) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-ghana-gold mx-auto mb-4"></div>
          <p className="text-gray-600">Redirecting to available ticket...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}