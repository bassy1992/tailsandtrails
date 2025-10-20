import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { MapPin, Phone, Mail, Facebook, Instagram, Twitter, User, Settings, LogOut, Calendar, Menu, X } from "lucide-react";
import { ReactNode, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useIsMobile } from "@/hooks/use-mobile";

interface LayoutProps {
  children: ReactNode;
}

function AuthSection() {
  const { user, isAuthenticated, logout } = useAuth();

  if (isAuthenticated && user) {
    const getInitials = (name: string) => {
      return name.split(' ').map(n => n[0]).join('').toUpperCase();
    };

    return (
      <DropdownMenu>
        <DropdownMenuTrigger className="flex items-center space-x-2 hover:bg-gray-50 rounded-lg p-2 transition-colors">
          <Avatar className="w-8 h-8">
            <AvatarImage src={user.avatar} />
            <AvatarFallback className="bg-ghana-green text-white text-sm">
              {getInitials(user.name)}
            </AvatarFallback>
          </Avatar>
          <span className="text-gray-700 font-medium">{user.name.split(' ')[0]}</span>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-56">
          <DropdownMenuLabel className="flex flex-col space-y-1">
            <p className="text-sm font-medium">{user.name}</p>
            <p className="text-xs text-gray-500">{user.email}</p>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem asChild>
            <Link to="/dashboard" className="flex items-center space-x-2 cursor-pointer">
              <User className="w-4 h-4" />
              <span>Dashboard</span>
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link to="/dashboard" className="flex items-center space-x-2 cursor-pointer">
              <Calendar className="w-4 h-4" />
              <span>My Bookings</span>
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link to="/dashboard" className="flex items-center space-x-2 cursor-pointer">
              <Settings className="w-4 h-4" />
              <span>Profile Settings</span>
            </Link>
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            onClick={logout}
            className="flex items-center space-x-2 cursor-pointer text-red-600 focus:text-red-600"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    );
  }

  return (
    <>
      <Link to="/login">
        <Button variant="ghost" className="text-ghana-green hover:bg-ghana-green hover:text-white">
          Login
        </Button>
      </Link>
      <Link to="/signup">
        <Button className="bg-ghana-green hover:bg-ghana-green/90 text-white">
          Sign Up
        </Button>
      </Link>
    </>
  );
}

function MobileNavigation() {
  const [isOpen, setIsOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();

  const navigationLinks = [
    { to: "/", label: "Home" },
    { to: "/destinations", label: "Destinations" },
    { to: "/gallery", label: "Gallery" },
    { to: "/tickets", label: "Events" },
    { to: "/about", label: "About" },
    { to: "/contact", label: "Contact" },
  ];

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="sm" className="md:hidden">
          <Menu className="h-6 w-6" />
          <span className="sr-only">Open menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[300px] sm:w-[400px]">
        <SheetHeader>
          <SheetTitle className="text-left">
            <Link to="/" className="flex items-center space-x-2" onClick={() => setIsOpen(false)}>
              <img
                src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fbfa2b897e15b4475b41dbeceafc18e1c?format=webp&width=200"
                alt="Tales and Trails Ghana Logo"
                className="h-8 w-auto"
              />
              <span className="text-lg font-bold text-ghana-green">Tales and Trails</span>
            </Link>
          </SheetTitle>
        </SheetHeader>
        
        <div className="flex flex-col space-y-4 mt-8">
          {/* Navigation Links */}
          <div className="space-y-3">
            {navigationLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="block px-3 py-2 text-lg font-medium text-gray-700 hover:text-ghana-green hover:bg-gray-50 rounded-md transition-colors"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="border-t pt-4">
            {isAuthenticated && user ? (
              <div className="space-y-3">
                <div className="flex items-center space-x-3 px-3 py-2">
                  <Avatar className="w-10 h-10">
                    <AvatarImage src={user.avatar} />
                    <AvatarFallback className="bg-ghana-green text-white">
                      {user.name.split(' ').map(n => n[0]).join('').toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium text-gray-900">{user.name}</p>
                    <p className="text-sm text-gray-500">{user.email}</p>
                  </div>
                </div>
                
                <Link
                  to="/dashboard"
                  className="flex items-center space-x-3 px-3 py-2 text-gray-700 hover:text-ghana-green hover:bg-gray-50 rounded-md transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  <User className="w-5 h-5" />
                  <span>Dashboard</span>
                </Link>
                
                <Link
                  to="/dashboard"
                  className="flex items-center space-x-3 px-3 py-2 text-gray-700 hover:text-ghana-green hover:bg-gray-50 rounded-md transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  <Calendar className="w-5 h-5" />
                  <span>My Bookings</span>
                </Link>
                
                <button
                  onClick={() => {
                    logout();
                    setIsOpen(false);
                  }}
                  className="flex items-center space-x-3 px-3 py-2 w-full text-left text-red-600 hover:bg-red-50 rounded-md transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                <Link to="/login" onClick={() => setIsOpen(false)}>
                  <Button variant="outline" className="w-full">
                    Login
                  </Button>
                </Link>
                <Link to="/signup" onClick={() => setIsOpen(false)}>
                  <Button className="w-full bg-ghana-green hover:bg-ghana-green/90">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}

export default function Layout({ children }: LayoutProps) {
  const isMobile = useIsMobile();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2 sm:space-x-3">
              <img
                src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fbfa2b897e15b4475b41dbeceafc18e1c?format=webp&width=200"
                alt="Tales and Trails Ghana Logo"
                className="h-8 sm:h-10 w-auto"
              />
              <span className={`font-bold text-ghana-green ${isMobile ? 'text-lg sm:text-xl' : 'text-2xl'}`}>
                {isMobile ? 'Tales & Trails' : 'Tales and Trails Ghana'}
              </span>
            </Link>

            {/* Desktop Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <Link to="/" className="text-gray-700 hover:text-ghana-green transition-colors font-medium">
                Home
              </Link>
              <Link to="/destinations" className="text-gray-700 hover:text-ghana-green transition-colors font-medium">
                Destinations
              </Link>
              <Link to="/gallery" className="text-gray-700 hover:text-ghana-green transition-colors font-medium">
                Gallery
              </Link>
              <Link to="/tickets" className="text-gray-700 hover:text-ghana-green transition-colors font-medium">
                Events
              </Link>
              <Link to="/about" className="text-gray-700 hover:text-ghana-green transition-colors font-medium">
                About
              </Link>
              <Link to="/contact" className="text-gray-700 hover:text-ghana-green transition-colors font-medium">
                Contact
              </Link>
            </div>

            {/* Desktop Auth Section */}
            <div className="hidden md:flex items-center space-x-4">
              <AuthSection />
            </div>

            {/* Mobile Navigation */}
            <MobileNavigation />
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-ghana-green text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            {/* Company Info */}
            <div className="space-y-4 sm:col-span-2 lg:col-span-1">
              <div className="flex items-center space-x-2 sm:space-x-3">
                <img
                  src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fbfa2b897e15b4475b41dbeceafc18e1c?format=webp&width=200"
                  alt="Tales and Trails Ghana Logo"
                  className="h-6 sm:h-8 w-auto"
                />
                <span className="text-lg sm:text-xl font-bold">Tales and Trails Ghana</span>
              </div>
              <p className="text-gray-300 text-sm sm:text-base">
                Discover the beauty and culture of Ghana with Tales and Trails Ghana - your gateway to authentic experiences and exciting events.
              </p>
              <div className="flex space-x-4">
                <Facebook className="h-5 w-5 hover:text-ghana-gold cursor-pointer transition-colors" />
                <Instagram className="h-5 w-5 hover:text-ghana-gold cursor-pointer transition-colors" />
                <Twitter className="h-5 w-5 hover:text-ghana-gold cursor-pointer transition-colors" />
              </div>
            </div>

            {/* Quick Links */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Quick Links</h3>
              <div className="space-y-2">
                <Link to="/destinations" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Destinations
                </Link>
                <Link to="/gallery" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Media Gallery
                </Link>
                <Link to="/tickets" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Events
                </Link>
                <Link to="/about" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  About Us
                </Link>
                <Link to="/contact" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Contact
                </Link>
              </div>
            </div>

            {/* Popular Destinations */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Popular Destinations</h3>
              <div className="space-y-2">
                <Link to="/destinations/cape-coast" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Cape Coast Castle
                </Link>
                <Link to="/destinations/aburi" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Aburi Gardens
                </Link>
                <Link to="/destinations/manhyia" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Manhyia Palace
                </Link>
                <Link to="/destinations/kakum" className="block text-gray-300 hover:text-ghana-gold transition-colors text-sm sm:text-base">
                  Kakum National Park
                </Link>
              </div>
            </div>

            {/* Contact Info */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Contact Us</h3>
              <div className="space-y-3">
                <a href="tel:+233241227481" className="flex items-center space-x-2 text-gray-300 hover:text-ghana-gold transition-colors">
                  <Phone className="h-4 w-4 flex-shrink-0" />
                  <span className="text-sm sm:text-base">+233 24 122 7481</span>
                </a>
                <a href="mailto:Talesandtrailsghana@gmail.com" className="flex items-center space-x-2 text-gray-300 hover:text-ghana-gold transition-colors">
                  <Mail className="h-4 w-4 flex-shrink-0" />
                  <span className="text-sm sm:text-base break-all">Talesandtrailsghana@gmail.com</span>
                </a>
                <div className="flex items-start space-x-2">
                  <MapPin className="h-4 w-4 mt-1 flex-shrink-0" />
                  <span className="text-gray-300 text-sm sm:text-base">
                    Aviation Highway<br />
                    Accra Spintex Road<br />
                    Accra, Ghana
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-6 sm:mt-8 pt-6 sm:pt-8 text-center">
            <p className="text-gray-300 text-xs sm:text-sm">
              © 2024 Tales and Trails Ghana. All rights reserved.
            </p>
            <div className="flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-4 mt-2">
              <Link to="/privacy" className="text-gray-300 hover:text-ghana-gold transition-colors text-xs sm:text-sm">
                Privacy Policy
              </Link>
              <span className="hidden sm:inline text-gray-500">|</span>
              <Link to="/terms" className="text-gray-300 hover:text-ghana-gold transition-colors text-xs sm:text-sm">
                Terms of Service
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
