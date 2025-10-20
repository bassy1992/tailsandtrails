import React from 'react';
import { useIsMobile } from '@/hooks/use-mobile';
import { cn } from '@/lib/utils';

interface MobileOptimizedProps {
  children: React.ReactNode;
  className?: string;
  mobileClassName?: string;
  desktopClassName?: string;
}

export function MobileOptimized({ 
  children, 
  className, 
  mobileClassName, 
  desktopClassName 
}: MobileOptimizedProps) {
  const isMobile = useIsMobile();
  
  return (
    <div className={cn(
      className,
      isMobile ? mobileClassName : desktopClassName
    )}>
      {children}
    </div>
  );
}

interface ResponsiveGridProps {
  children: React.ReactNode;
  cols?: {
    mobile?: number;
    tablet?: number;
    desktop?: number;
  };
  gap?: {
    mobile?: number;
    tablet?: number;
    desktop?: number;
  };
  className?: string;
}

export function ResponsiveGrid({ 
  children, 
  cols = { mobile: 1, tablet: 2, desktop: 3 },
  gap = { mobile: 4, tablet: 6, desktop: 8 },
  className 
}: ResponsiveGridProps) {
  const gridCols = `grid-cols-${cols.mobile} sm:grid-cols-${cols.tablet} lg:grid-cols-${cols.desktop}`;
  const gridGap = `gap-${gap.mobile} sm:gap-${gap.tablet} lg:gap-${gap.desktop}`;
  
  return (
    <div className={cn('grid', gridCols, gridGap, className)}>
      {children}
    </div>
  );
}

interface MobileCardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
  hover?: boolean;
}

export function MobileCard({ 
  children, 
  className, 
  padding = 'md',
  hover = true 
}: MobileCardProps) {
  const paddingClasses = {
    sm: 'p-3 sm:p-4',
    md: 'p-4 sm:p-6',
    lg: 'p-6 sm:p-8'
  };
  
  return (
    <div className={cn(
      'bg-white rounded-lg shadow-md',
      paddingClasses[padding],
      hover && 'hover:shadow-lg transition-shadow duration-200',
      className
    )}>
      {children}
    </div>
  );
}

interface TouchButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
}

export function TouchButton({ 
  children, 
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  className,
  ...props 
}: TouchButtonProps) {
  const baseClasses = 'touch-target font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variantClasses = {
    primary: 'bg-ghana-green text-white hover:bg-ghana-green/90 focus:ring-ghana-green',
    secondary: 'bg-ghana-gold text-black hover:bg-ghana-gold/90 focus:ring-ghana-gold',
    outline: 'border-2 border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white focus:ring-ghana-green',
    ghost: 'text-ghana-green hover:bg-ghana-green/10 focus:ring-ghana-green'
  };
  
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };
  
  return (
    <button 
      className={cn(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        fullWidth && 'w-full',
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

interface ResponsiveImageProps {
  src: string;
  alt: string;
  className?: string;
  aspectRatio?: 'square' | 'video' | 'wide' | 'tall';
  loading?: 'lazy' | 'eager';
}

export function ResponsiveImage({ 
  src, 
  alt, 
  className,
  aspectRatio = 'video',
  loading = 'lazy'
}: ResponsiveImageProps) {
  const aspectClasses = {
    square: 'aspect-square',
    video: 'aspect-video',
    wide: 'aspect-[21/9]',
    tall: 'aspect-[3/4]'
  };
  
  return (
    <div className={cn('overflow-hidden rounded-lg', aspectClasses[aspectRatio], className)}>
      <img 
        src={src} 
        alt={alt}
        loading={loading}
        className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
      />
    </div>
  );
}

interface MobileSectionProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
  background?: 'white' | 'gray' | 'transparent';
}

export function MobileSection({ 
  children, 
  className,
  padding = 'md',
  background = 'transparent'
}: MobileSectionProps) {
  const paddingClasses = {
    sm: 'py-8 sm:py-12',
    md: 'py-12 sm:py-16 lg:py-20',
    lg: 'py-16 sm:py-20 lg:py-24'
  };
  
  const backgroundClasses = {
    white: 'bg-white',
    gray: 'bg-gray-50',
    transparent: 'bg-transparent'
  };
  
  return (
    <section className={cn(
      paddingClasses[padding],
      backgroundClasses[background],
      className
    )}>
      <div className="mobile-container">
        {children}
      </div>
    </section>
  );
}

interface MobileTextProps {
  children: React.ReactNode;
  variant?: 'h1' | 'h2' | 'h3' | 'body' | 'caption';
  className?: string;
  align?: 'left' | 'center' | 'right';
}

export function MobileText({ 
  children, 
  variant = 'body',
  className,
  align = 'left'
}: MobileTextProps) {
  const variantClasses = {
    h1: 'mobile-heading',
    h2: 'mobile-subheading',
    h3: 'text-xl sm:text-2xl font-semibold text-gray-800',
    body: 'mobile-text',
    caption: 'text-sm sm:text-base text-gray-500'
  };
  
  const alignClasses = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right'
  };
  
  const Component = variant.startsWith('h') ? variant as keyof JSX.IntrinsicElements : 'p';
  
  return (
    <Component className={cn(
      variantClasses[variant],
      alignClasses[align],
      className
    )}>
      {children}
    </Component>
  );
}

// Hook for responsive breakpoints
export function useResponsiveBreakpoint() {
  const isMobile = useIsMobile();
  
  return {
    isMobile,
    isTablet: !isMobile && window.innerWidth < 1024,
    isDesktop: window.innerWidth >= 1024,
    breakpoint: isMobile ? 'mobile' : window.innerWidth < 1024 ? 'tablet' : 'desktop'
  };
}