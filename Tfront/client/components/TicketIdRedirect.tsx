import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface TicketIdRedirectProps {
  children: React.ReactNode;
}

/**
 * Component that validates ticket IDs and redirects invalid ones
 */
export default function TicketIdRedirect({ children }: TicketIdRedirectProps) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    // List of valid ticket IDs that exist in the database
    const validTicketIds = ['1', '2'];
    
    if (id && !validTicketIds.includes(id)) {
      console.log(`Invalid ticket ID ${id} detected, redirecting to ticket 2`);
      
      // Determine the current path to redirect appropriately
      const currentPath = window.location.pathname;
      
      if (currentPath.includes('/booking/')) {
        navigate('/booking/2', { replace: true });
      } else if (currentPath.includes('/ticket-booking/')) {
        navigate('/ticket-booking/2', { replace: true });
      } else {
        // Default redirect to tickets page
        navigate('/tickets', { replace: true });
      }
      
      return;
    }
  }, [id, navigate]);

  return <>{children}</>;
}