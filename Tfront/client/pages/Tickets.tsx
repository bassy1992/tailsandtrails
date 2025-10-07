import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Calendar, MapPin, Clock, Users, Star, Music, Mic2, 
  Search, Filter, Ticket, Zap, Heart, Share2, Loader2
} from "lucide-react";
import { Link } from "react-router-dom";
import { ticketsApi, EventTicket, TicketCategory } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

// Types are now imported from api.ts

export default function Tickets() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedMonth, setSelectedMonth] = useState("all");
  const [tickets, setTickets] = useState<EventTicket[]>([]);
  const [categories, setCategories] = useState<TicketCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  // Fetch tickets and categories from API (public access for browsing)
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        console.log('Fetching tickets from public API...');
        
        // Fetch tickets using direct fetch (public access)
        const [ticketsResponse, categoriesResponse] = await Promise.all([
          fetch('http://localhost:8000/api/tickets/', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }),
          fetch('http://localhost:8000/api/tickets/categories/', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }).catch(() => null) // Don't fail if categories fail
        ]);
        
        if (!ticketsResponse.ok) {
          throw new Error(`Failed to fetch tickets: ${ticketsResponse.status}`);
        }
        
        const ticketsData = await ticketsResponse.json();
        console.log('Tickets data received:', ticketsData);
        
        let categoriesData = [];
        if (categoriesResponse && categoriesResponse.ok) {
          categoriesData = await categoriesResponse.json();
          console.log('Categories data received:', categoriesData);
        }
        
        setTickets(ticketsData);
        setCategories(categoriesData);
        
        console.log('Successfully loaded tickets and categories');
        
      } catch (err) {
        console.error('Error fetching data:', err);
        const errorMessage = err instanceof Error ? err.message : 'Failed to load tickets';
        console.log('Using mock data due to API error:', errorMessage);
        
        // Use mock data as fallback instead of showing error
        setTickets([]);
        setCategories([]);
        setError(null); // Don't show error, just use mock data
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // Remove dependency on isAuthenticated

  // Mock events data for fallback - in real app, this would come from an API
  const mockEvents: EventTicket[] = [
    {
      id: 1,
      name: "Raphohic Festival 2024",
      artist: "Various Artists",
      venue: "National Theatre, Accra",
      date: "2024-12-23",
      time: "6:00 PM",
      category: "Festival",
      price: 150,
      currency: "GH₵",
      image: "https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg?auto=compress&cs=tinysrgb&w=600",
      rating: 4.8,
      attendees: 5000,
      description: "Ghana's biggest hip-hop festival featuring the best local and international rap artists.",
      availableTickets: 1200,
      totalTickets: 5000,
      tags: ["Hip-Hop", "Festival", "Outdoor"],
      isHot: true,
      isSoldOut: false
    },
    {
      id: 2,
      name: "Bhim Concert 2024",
      artist: "Stonebwoy",
      venue: "Accra Sports Stadium",
      date: "2024-12-31",
      time: "8:00 PM",
      category: "Concert",
      price: 120,
      currency: "GH₵",
      image: "https://images.pexels.com/photos/1105666/pexels-photo-1105666.jpeg?auto=compress&cs=tinysrgb&w=600",
      rating: 4.9,
      attendees: 20000,
      description: "New Year's Eve concert with Stonebwoy and special guests. Ring in 2025 with the Bhim Nation!",
      availableTickets: 3500,
      totalTickets: 20000,
      tags: ["Dancehall", "Reggae", "New Year"],
      isHot: true,
      isSoldOut: false
    },
    {
      id: 3,
      name: "Ghana Meets Naija",
      artist: "Sarkodie x Burna Boy",
      venue: "Fantasy Dome, Trade Fair",
      date: "2025-01-15",
      time: "7:00 PM",
      category: "Concert",
      price: 200,
      currency: "GH₵",
      image: "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
      rating: 4.7,
      attendees: 8000,
      description: "Epic collaboration concert featuring Ghana's Sarkodie and Nigeria's Burna Boy.",
      availableTickets: 2000,
      totalTickets: 8000,
      tags: ["Afrobeats", "Hip-Hop", "Collaboration"],
      isHot: true,
      isSoldOut: false
    },
    {
      id: 4,
      name: "Ashaiman to the World",
      artist: "Shatta Wale",
      venue: "Saka Saka Park, Ashaiman",
      date: "2025-02-14",
      time: "6:00 PM",
      category: "Concert",
      price: 80,
      currency: "GH₵",
      image: "https://images.pexels.com/photos/2747449/pexels-photo-2747449.jpeg?auto=compress&cs=tinysrgb&w=600",
      rating: 4.6,
      attendees: 15000,
      description: "Shatta Wale's annual homecoming concert celebrating Ashaiman and the SM fanbase.",
      availableTickets: 5000,
      totalTickets: 15000,
      tags: ["Dancehall", "Reggae", "Community"],
      isHot: false,
      isSoldOut: false
    },
    {
      id: 5,
      name: "Highlife Legends Night",
      artist: "Amakye Dede, Nana Ampadu",
      venue: "National Theatre, Accra",
      date: "2025-03-21",
      time: "7:30 PM",
      category: "Concert",
      price: 100,
      currency: "GH₵",
      image: "https://images.pexels.com/photos/1677710/pexels-photo-1677710.jpeg?auto=compress&cs=tinysrgb&w=600",
      rating: 4.8,
      attendees: 3000,
      description: "A celebration of Ghana's highlife music heritage with legendary performers.",
      availableTickets: 800,
      totalTickets: 3000,
      tags: ["Highlife", "Traditional", "Legends"],
      isHot: false,
      isSoldOut: false
    },
    {
      id: 6,
      name: "Vodafone Ghana Music Awards",
      artist: "Various Nominees",
      venue: "Grand Arena, AICC",
      date: "2025-04-05",
      time: "8:00 PM",
      category: "Awards",
      price: 250,
      currency: "GH₵",
      image: "https://images.pexels.com/photos/1190297/pexels-photo-1190297.jpeg?auto=compress&cs=tinysrgb&w=600",
      rating: 4.9,
      attendees: 6000,
      description: "Ghana's premier music awards ceremony celebrating the best in Ghanaian music.",
      availableTickets: 0,
      totalTickets: 6000,
      tags: ["Awards", "Gala", "Red Carpet"],
      isHot: false,
      isSoldOut: true
    }
  ];

  // Use real data if available, otherwise fallback to mock data
  const events = tickets.length > 0 ? tickets : mockEvents;
  
  const categoryOptions = ["all", ...categories.map(cat => cat.name)];
  const months = ["all", "December", "January", "February", "March", "April"];

  const filteredEvents = events.filter(event => {
    // Handle both API response format and mock data format
    const title = event.title || event.name || '';
    const venueName = event.venue?.name || event.venue || '';
    const categoryName = event.category?.name || event.category || '';
    const eventDate = event.event_date || event.date || '';
    
    const matchesSearch = title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         venueName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "all" || categoryName === selectedCategory;
    const eventMonth = new Date(eventDate).toLocaleDateString('en-US', { month: 'long' });
    const matchesMonth = selectedMonth === "all" || eventMonth === selectedMonth;
    
    return matchesSearch && matchesCategory && matchesMonth;
  });

  const hotEvents = events.filter(event => event.is_featured || event.isHot);
  const upcomingEvents = events.filter(event => {
    const eventDate = event.event_date || event.date || '';
    return new Date(eventDate) > new Date();
  }).slice(0, 6);

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-ghana-green mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Loading Tickets...</h2>
            <p className="text-gray-600">Please wait while we fetch the latest events</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <Ticket className="h-16 w-16 text-red-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Tickets</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={() => window.location.reload()} className="bg-ghana-green hover:bg-ghana-green/90">
              Try Again
            </Button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Event Tickets
            </h1>
            <p className="text-xl md:text-2xl text-ghana-gold mb-8">
              Your gateway to Ghana's hottest concerts, festivals & events
            </p>
            <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-4">
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  type="text"
                  placeholder="Search events, artists, venues..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 py-3 text-gray-900"
                />
              </div>
              <Button className="bg-ghana-gold hover:bg-ghana-gold/90 text-black font-semibold px-8 py-3">
                <Ticket className="h-5 w-5 mr-2" />
                Find Tickets
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Filters */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 space-y-4 md:space-y-0">
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Filter by:</span>
            </div>
            
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-1 text-sm focus:ring-ghana-green focus:border-ghana-green"
            >
              {categoryOptions.map(category => (
                <option key={category} value={category}>
                  {category === "all" ? "All Categories" : category}
                </option>
              ))}
            </select>
            
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-1 text-sm focus:ring-ghana-green focus:border-ghana-green"
            >
              {months.map(month => (
                <option key={month} value={month}>
                  {month === "all" ? "All Months" : month}
                </option>
              ))}
            </select>
          </div>
          
          <p className="text-sm text-gray-600">
            {filteredEvents.length} events found
          </p>
        </div>

        <Tabs defaultValue="all" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="all">All Events</TabsTrigger>
            <TabsTrigger value="hot">Hot Tickets 🔥</TabsTrigger>
            <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
          </TabsList>

          {/* All Events */}
          <TabsContent value="all" className="mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
            
            {filteredEvents.length === 0 && (
              <div className="text-center py-12">
                <Ticket className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No events found</h3>
                <p className="text-gray-600">Try adjusting your search or filters</p>
              </div>
            )}
          </TabsContent>

          {/* Hot Tickets */}
          <TabsContent value="hot" className="mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {hotEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          </TabsContent>

          {/* Upcoming Events */}
          <TabsContent value="upcoming" className="mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {upcomingEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  );
}

function EventCard({ event }: { event: EventTicket }) {
  const { isAuthenticated } = useAuth();
  // Handle both API response format and mock data format
  const title = event.title || event.name || 'Untitled Event';
  const isSoldOut = event.is_sold_out || event.isSoldOut || false;
  const availableQty = event.available_quantity || event.availableTickets || 0;
  const totalQty = event.total_quantity || event.totalTickets || 1;
  const isFeatured = event.is_featured || event.isHot || false;
  const categoryName = event.category?.name || event.category || 'Event';
  const eventDate = event.event_date || event.date || '';
  const eventTime = event.time || '';
  const venueName = event.venue?.name || event.venue || 'Venue TBA';
  const venueCity = event.venue?.city || '';
  const price = event.effective_price || event.price || '0';
  const originalPrice = event.price || '';
  const discountPrice = event.discount_price || '';
  const discountPercentage = event.discount_percentage || 0;
  const rating = parseFloat(event.rating || '0');
  const reviewsCount = event.reviews_count || 0;
  const salesCount = event.sales_count || event.attendees || 0;
  const ticketType = event.ticket_type || 'single';
  const categoryType = event.category?.category_type || 'event';
  const venueCapacity = event.venue?.capacity;
  const isAvailable = event.is_available !== undefined ? event.is_available : !isSoldOut;

  const getAvailabilityStatus = () => {
    if (isSoldOut) return { text: "Sold Out", color: "bg-red-100 text-red-800" };
    const percentageLeft = (availableQty / totalQty) * 100;
    if (percentageLeft <= 10) return { text: "Few Left", color: "bg-yellow-100 text-yellow-800" };
    if (percentageLeft <= 30) return { text: "Selling Fast", color: "bg-orange-100 text-orange-800" };
    return { text: "Available", color: "bg-green-100 text-green-800" };
  };

  const availability = getAvailabilityStatus();
  
  // Default image if none provided
  const eventImage = event.image || "https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg?auto=compress&cs=tinysrgb&w=600";

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 overflow-hidden">
      <div className="relative">
        <img
          src={eventImage}
          alt={title}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute top-3 left-3 flex flex-wrap gap-2">
          {isFeatured && (
            <Badge className="bg-red-500 text-white">
              <Zap className="h-3 w-3 mr-1" />
              Featured
            </Badge>
          )}
          <Badge className="bg-ghana-green text-white">
            {categoryName}
          </Badge>
        </div>
        <div className="absolute top-3 right-3 flex space-x-2">
          <Button size="sm" variant="secondary" className="bg-white/90 hover:bg-white p-2">
            <Heart className="h-4 w-4" />
          </Button>
          <Button size="sm" variant="secondary" className="bg-white/90 hover:bg-white p-2">
            <Share2 className="h-4 w-4" />
          </Button>
        </div>
        <Badge className={`absolute bottom-3 right-3 ${availability.color}`}>
          {availability.text}
        </Badge>
      </div>
      
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <CardTitle className="text-lg font-bold line-clamp-2 group-hover:text-ghana-green transition-colors">
              {title}
            </CardTitle>
            <CardDescription className="flex items-center space-x-1 mt-1">
              <Music className="h-4 w-4" />
              <span>{event.artist || venueName}</span>
            </CardDescription>
          </div>
          <div className="text-right">
            <div className="flex flex-col">
              {discountPrice && (
                <span className="text-sm text-gray-500 line-through">
                  {event.currency || 'GH₵'}{originalPrice}
                </span>
              )}
              <div className="text-2xl font-bold text-ghana-green">
                {event.currency || 'GH₵'}{price}
              </div>
              {discountPercentage > 0 && (
                <span className="text-xs text-red-600 font-medium">
                  {discountPercentage}% OFF
                </span>
              )}
            </div>
            <div className="flex items-center space-x-1 text-sm text-gray-600 mt-1">
              <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
              <span>{rating.toFixed(1)}</span>
              <span className="text-xs">({reviewsCount})</span>
            </div>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="space-y-3">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Calendar className="h-4 w-4" />
            <span>{new Date(eventDate).toLocaleDateString('en-GB', { 
              weekday: 'short', 
              day: 'numeric', 
              month: 'short',
              year: 'numeric'
            })}</span>
            <Clock className="h-4 w-4 ml-2" />
            <span>
              {eventTime || new Date(eventDate).toLocaleTimeString('en-GB', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </span>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <MapPin className="h-4 w-4" />
            <span className="line-clamp-1">
              {venueCity ? `${venueName}, ${venueCity}` : venueName}
            </span>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Users className="h-4 w-4" />
            <span>{salesCount.toLocaleString()} {event.attendees ? 'expected' : 'sold'}</span>
            {venueCapacity && (
              <span>• {venueCapacity.toLocaleString()} capacity</span>
            )}
          </div>

          <div className="flex flex-wrap gap-1 mt-2">
            <Badge variant="outline" className="text-xs">
              {ticketType}
            </Badge>
            <Badge variant="outline" className="text-xs">
              {categoryType}
            </Badge>
            {isFeatured && (
              <Badge variant="outline" className="text-xs text-red-600 border-red-200">
                Featured
              </Badge>
            )}
            {event.tags && event.tags.slice(0, 2).map((tag, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
        </div>
        
        <div className="mt-6 space-y-2">
          {isSoldOut || !isAvailable ? (
            <Button 
              className="w-full bg-gray-400 cursor-not-allowed"
              disabled
            >
              <Ticket className="h-4 w-4 mr-2" />
              {isSoldOut ? "Sold Out" : "Not Available"}
            </Button>
          ) : isAuthenticated ? (
            <Button 
              className="w-full bg-ghana-green hover:bg-ghana-green/90"
              asChild
            >
              <Link to={`/ticket-booking/${event.id}`}>
                <Ticket className="h-4 w-4 mr-2" />
                Buy Tickets
              </Link>
            </Button>
          ) : (
            <Button 
              className="w-full bg-ghana-blue hover:bg-ghana-blue/90"
              asChild
            >
              <Link to="/login" state={{ returnUrl: `/ticket-booking/${event.id}` }}>
                <Ticket className="h-4 w-4 mr-2" />
                Login to Buy Tickets
              </Link>
            </Button>
          )}
          
          {!isSoldOut && isAvailable && (
            <p className="text-xs text-center text-gray-500">
              {availableQty.toLocaleString()} of {totalQty.toLocaleString()} tickets left
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
