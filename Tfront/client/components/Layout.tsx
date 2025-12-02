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
import { MapPin, Phone, Mail, Facebook, Instagram, Twitter, User, Settings, LogOut, Calendar, Menu, X } from "lucide-react";
import { ReactNode, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

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

export default function Layout({ children }: LayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
              <span className="text-lg sm:text-2xl font-bold text-ghana-green hidden sm:inline">Tales and Trails Ghana</span>
              <span className="text-lg font-bold text-ghana-green sm:hidden">T&T Ghana</span>
            </Link>

            {/* Navigation Links - Desktop */}
            <div className="hidden md:flex items-center space-x-8">
              <Link to="/" className="text-gray-700 hover:text-ghana-green transition-colors">
                Home
              </Link>
              <Link to="/destinations" className="text-gray-700 hover:text-ghana-green transition-colors">
                Destinations
              </Link>
              <Link to="/gallery" className="text-gray-700 hover:text-ghana-green transition-colors">
                Gallery
              </Link>
              <Link to="/tickets" className="text-gray-700 hover:text-ghana-green transition-colors">
                Tickets
              </Link>
              <Link to="/about" className="text-gray-700 hover:text-ghana-green transition-colors">
                About
              </Link>
              <Link to="/contact" className="text-gray-700 hover:text-ghana-green transition-colors">
                Contact
              </Link>
            </div>

            {/* Auth Section - Desktop */}
            <div className="hidden md:flex items-center space-x-4">
              <AuthSection />
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label="Toggle menu"
              >
                {mobileMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </Button>
            </div>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t border-gray-200 py-4 space-y-2">
              <Link 
                to="/" 
                className="block px-4 py-2 text-gray-700 hover:bg-ghana-green hover:text-white rounded transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>
              <Link 
                to="/destinations" 
                className="block px-4 py-2 text-gray-700 hover:bg-ghana-green hover:text-white rounded transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Destinations
              </Link>
              <Link 
                to="/gallery" 
                className="block px-4 py-2 text-gray-700 hover:bg-ghana-green hover:text-white rounded transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Gallery
              </Link>
              <Link 
                to="/tickets" 
                className="block px-4 py-2 text-gray-700 hover:bg-ghana-green hover:text-white rounded transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Tickets
              </Link>
              <Link 
                to="/about" 
                className="block px-4 py-2 text-gray-700 hover:bg-ghana-green hover:text-white rounded transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                About
              </Link>
              <Link 
                to="/contact" 
                className="block px-4 py-2 text-gray-700 hover:bg-ghana-green hover:text-white rounded transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                Contact
              </Link>
              
              {/* Mobile Auth Section */}
              <div className="border-t border-gray-200 pt-4 px-4 space-y-2">
                <AuthSection />
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-ghana-green text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Company Info */}
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <img
                  src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fbfa2b897e15b4475b41dbeceafc18e1c?format=webp&width=200"
                  alt="Tales and Trails Ghana Logo"
                  className="h-8 w-auto"
                />
                <span className="text-xl font-bold">Tales and Trails Ghana</span>
              </div>
              <p className="text-gray-300">
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
                <Link to="/destinations" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Destinations
                </Link>
                <Link to="/gallery" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Media Gallery
                </Link>
                <Link to="/tickets" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Event Tickets
                </Link>
                <Link to="/about" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  About Us
                </Link>
                <Link to="/contact" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Contact
                </Link>
              </div>
            </div>

            {/* Popular Destinations */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Popular Destinations</h3>
              <div className="space-y-2">
                <Link to="/destinations/cape-coast" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Cape Coast Castle
                </Link>
                <Link to="/destinations/aburi" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Aburi Gardens
                </Link>
                <Link to="/destinations/manhyia" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Manhyia Palace
                </Link>
                <Link to="/destinations/kakum" className="block text-gray-300 hover:text-ghana-gold transition-colors">
                  Kakum National Park
                </Link>
              </div>
            </div>

            {/* Contact Info */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Contact Us</h3>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <Phone className="h-4 w-4" />
                  <span className="text-gray-300">+233 24 127 4481</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Phone className="h-4 w-4" />
                  <span className="text-gray-300">+233 54 191 8418</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <span className="text-gray-300">info@talesandtrails.gh</span>
                </div>
                <div className="flex items-start space-x-2">
                  <MapPin className="h-4 w-4 mt-1" />
                  <span className="text-gray-300">
                    Aviation Highway, Spintex<br />
                    Accra, Ghana
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-8 pt-8 text-center">
            <p className="text-gray-300">
              © 2024 Tales and Trails Ghana. All rights reserved. | Privacy Policy | Terms of Service
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
