import { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { validateAndRedirectAsync, getPathType, getValidDestinations } from '../utils/idValidation';

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
  const [isValidating, setIsValidating] = useState(true);
  const [isValid, setIsValid] = useState(false);

  // Determine if this is a destination or ticket path
  const pathType = getPathType(location.pathname);

  useEffect(() => {
    const validateAsync = async () => {
      try {
        setIsValidating(true);
        
        // Preload destinations if this is a destination path
        if (pathType === 'destination') {
          await getValidDestinations();
        }
        
        // Perform validation
        const validationResult = await validateAndRedirectAsync(id, location.pathname, navigate);
        setIsValid(validationResult);
      } catch (error) {
        console.error('Validation error:', error);
        // On error, redirect to default
        const defaultPath = pathType === 'destination' ? '/booking/1' : '/ticket-booking/1';
        navigate(defaultPath, { replace: true });
        setIsValid(false);
      } finally {
        setIsValidating(false);
      }
    };

    validateAsync();
  }, [id, location.pathname, navigate, pathType]);
  
  // Show loading while validating
  if (isValidating) {
    const itemType = pathType === 'destination' ? 'destination' : 'ticket';
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-ghana-gold mx-auto mb-4"></div>
          <p className="text-gray-600">Validating {itemType}...</p>
        </div>
      </div>
    );
  }

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