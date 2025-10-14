import React from 'react';

interface SafeTooltipProviderProps {
  children: React.ReactNode;
}

const SafeTooltipProvider: React.FC<SafeTooltipProviderProps> = ({ children }) => {
  // For now, just return children without TooltipProvider to avoid the React context error
  // We can add TooltipProvider back later when we need tooltips
  return <>{children}</>;
};

export default SafeTooltipProvider;
