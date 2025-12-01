import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Construction, ArrowLeft } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

export default function Placeholder() {
  const location = useLocation();
  const path = location.pathname;
  
  const getPageTitle = () => {
    switch (path) {
      case '/tours': return 'Tour Packages';
      case '/about': return 'About Us';
      case '/contact': return 'Contact Us';
      case '/login': return 'Login';
      case '/signup': return 'Sign Up';
      case '/dashboard': return 'User Dashboard';
      case '/admin': return 'Admin Dashboard';
      default: 
        if (path.startsWith('/tour/')) return 'Tour Details';
        if (path.startsWith('/destinations/')) return 'Destination Details';
        return 'Page';
    }
  };

  const getPageDescription = () => {
    switch (path) {
      case '/tours': return 'Browse all available tour packages with detailed information and booking options.';
      case '/about': return 'Learn more about Tales and Trails Ghana, our mission, and our commitment to authentic travel experiences.';
      case '/contact': return 'Get in touch with our team for custom tours, support, or general inquiries.';
      case '/login': return 'Sign in to your account to manage bookings and access exclusive features.';
      case '/signup': return 'Create an account to start booking tours and accessing personalized recommendations.';
      case '/dashboard': return 'Manage your profile, view bookings, payment history, and access support.';
      case '/admin': return 'Administrative panel for managing tours, bookings, customers, and payments.';
      default: 
        if (path.startsWith('/tour/')) return 'Detailed information about this tour package including itinerary, pricing, and booking options.';
        if (path.startsWith('/destinations/')) return 'Comprehensive guide to this destination with available tours and local information.';
        return 'This page is under construction and will be available soon.';
    }
  };

  return (
    <Layout>
      <div className="min-h-[60vh] flex items-center justify-center py-16">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Card className="border-2 border-dashed border-gray-300">
            <CardHeader className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center">
                <Construction className="h-8 w-8 text-ghana-green" />
              </div>
              <CardTitle className="text-3xl text-ghana-green">
                {getPageTitle()}
              </CardTitle>
              <CardDescription className="text-lg leading-relaxed">
                {getPageDescription()}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="bg-ghana-gold/10 p-4 rounded-lg">
                <p className="text-sm text-gray-700">
                  <strong>Coming Soon:</strong> This page is currently being developed. 
                  In the meantime, you can explore our homepage and destinations to discover 
                  amazing tour packages across Ghana.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/">
                  <Button className="bg-ghana-green hover:bg-ghana-green/90">
                    Go to Homepage
                  </Button>
                </Link>
                <Link to="/destinations">
                  <Button variant="outline" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                    Browse Destinations
                  </Button>
                </Link>
                <Button 
                  variant="ghost" 
                  onClick={() => window.history.back()}
                  className="text-gray-600 hover:text-ghana-green"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Go Back
                </Button>
              </div>

              <div className="text-sm text-gray-500">
                Have questions or need a custom tour? <Link to="/contact" className="text-ghana-green hover:underline">Contact us</Link> and we'll help you plan the perfect Ghana experience.
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
