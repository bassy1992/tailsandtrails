import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

/**
 * Component to handle redirects for invalid ticket IDs
 */
export default function TicketRedirect() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    const validTicketIds = ['1', '2'];
    
    if (id && !validTicketIds.includes(id)) {
      console.log(`Redirecting invalid ticket ID ${id} to ticket 2`);
      navigate('/ticket-booking/2', { replace: true });
    } else if (!id) {
      // No ID provided, redirect to tickets list
      navigate('/tickets', { replace: true });
    }
  }, [id, navigate]);

  return null; // This component doesn't render anything
}