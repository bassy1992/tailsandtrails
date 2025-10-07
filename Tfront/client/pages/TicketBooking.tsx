import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { 
  ArrowLeft, Calendar, MapPin, Users, Clock, Star, 
  Plus, Minus, Info, Music, Ticket, Loader2
} from "lucide-react";

interface TicketCategory {
  id: number;
  name: string;
  slug: string;
  category_type: string;
  description: string;
  icon: string;
  order: number;
}

interface Venue {
  id: number;
  name: string;
  slug: string;
  address: string;
  city: string;
  region: string;
  country: string;
  latitude?: number;
  longitude?: number;
  capacity?: number;
  description: string;
  image?: string;
  contact_phone?: string;
  contact_email?: string;
  website?: string;
}

interface EventTicket {
  id: number;
  title: string;
  slug: string;
  category: TicketCategory;
  venue?: Venue;
  ticket_type: string;
  description: string;
  short_description: string;
  price: string;
  discount_price?: string;
  effective_price: string;
  discount_percentage: number;
  currency: string;
  total_quantity: number;
  available_quantity: number;
  min_purchase?: number;
  max_purchase?: number;
  event_date: string;
  event_end_date?: string;
  sale_start_date: string;
  sale_end_date: string;
  image?: string;
  gallery_images?: string[];
  features?: string[];
  terms_conditions?: string;
  cancellation_policy?: string;
  tags?: string[];
  status: string;
  is_featured: boolean;
  is_refundable: boolean;
  requires_approval: boolean;
  is_available: boolean;
  is_sold_out: boolean;
  views_count?: number;
  sales_count?: number;
  rating?: string;
  reviews_count?: number;
  created_at?: string;
}

interface TicketType {
  id: string;
  name: string;
  price: number;
  description: string;
  benefits: string[];
  available: number;
}

export default function TicketBooking() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [event, setEvent] = useState<EventTicket | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTicketType, setSelectedTicketType] = useState<string>("regular");
  const [quantity, setQuantity] = useState<number>(1);
  const [customerInfo, setCustomerInfo] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: ""
  });
  const [paymentMethod, setPaymentMethod] = useState<string>("");

  // Fetch event data from API
  useEffect(() => {
    const fetchEvent = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        console.log('Fetching ticket details for ID:', id);
        
        // Try to get ticket details by ID from the list endpoint first
        let response = await fetch(`http://localhost:8000/api/tickets/?id=${id}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch ticket');
        }
        
        const tickets = await response.json();
        if (tickets.length === 0) {
          throw new Error('Ticket not found');
        }
        
        // Get the first ticket from the response
        const ticket = tickets[0];
        
        // Now fetch the full details using the slug if available, otherwise use the basic data
        if (ticket.slug) {
          try {
            const detailResponse = await fetch(`http://localhost:8000/api/tickets/${ticket.slug}/`);
            if (detailResponse.ok) {
              const detailData = await detailResponse.json();
              // Ensure we have all required fields with defaults
              const completeTicket = {
                ...detailData,
                features: detailData.features || [],
                terms_conditions: detailData.terms_conditions || '',
                cancellation_policy: detailData.cancellation_policy || '',
                tags: detailData.tags || [],
                min_purchase: detailData.min_purchase || 1,
                max_purchase: detailData.max_purchase || 10,
                gallery_images: detailData.gallery_images || [],
                views_count: detailData.views_count || 0,
                sales_count: detailData.sales_count || 0,
                rating: detailData.rating || '0.00',
                reviews_count: detailData.reviews_count || 0
              };
              setEvent(completeTicket);
            } else {
              // Fall back to the basic ticket data with defaults
              const basicTicketWithDefaults = {
                ...ticket,
                features: [],
                terms_conditions: '',
                cancellation_policy: '',
                tags: [],
                min_purchase: 1,
                max_purchase: 10,
                gallery_images: [],
                views_count: 0,
                sales_count: 0,
                rating: '0.00',
                reviews_count: 0
              };
              setEvent(basicTicketWithDefaults);
            }
          } catch (detailError) {
            console.warn('Could not fetch detailed ticket info, using basic data:', detailError);
            const basicTicketWithDefaults = {
              ...ticket,
              features: [],
              terms_conditions: '',
              cancellation_policy: '',
              tags: [],
              min_purchase: 1,
              max_purchase: 10,
              gallery_images: [],
              views_count: 0,
              sales_count: 0,
              rating: '0.00',
              reviews_count: 0
            };
            setEvent(basicTicketWithDefaults);
          }
        } else {
          const basicTicketWithDefaults = {
            ...ticket,
            features: [],
            terms_conditions: '',
            cancellation_policy: '',
            tags: [],
            min_purchase: 1,
            max_purchase: 10,
            gallery_images: [],
            views_count: 0,
            sales_count: 0,
            rating: '0.00',
            reviews_count: 0
          };
          setEvent(basicTicketWithDefaults);
        }
        
        setError(null);
      } catch (err) {
        console.error('Error fetching ticket:', err);
        setError(err instanceof Error ? err.message : 'Failed to load ticket');
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [id]);

  // Generate ticket types based on the event data
  const generateTicketTypes = (event: EventTicket): TicketType[] => {
    const basePrice = parseFloat(event.effective_price || event.price || '0');
    const discountPrice = event.discount_price ? parseFloat(event.discount_price) : null;
    const features = event.features || [];
    
    const ticketTypes: TicketType[] = [
      {
        id: "regular",
        name: "General Admission",
        price: basePrice,
        description: event.short_description || "Standard ticket access",
        benefits: features.length > 0 ? features : [
          "Entry to event",
          "Standard seating/standing area",
          "Access to main facilities"
        ],
        available: Math.floor(event.available_quantity * 0.8) // 80% for regular
      }
    ];

    // Add VIP option if the event is featured or has higher price
    if (event.is_featured || basePrice > 100) {
      ticketTypes.push({
        id: "vip",
        name: "VIP Experience",
        price: Math.round(basePrice * 1.8), // 80% markup for VIP
        description: "Premium experience with exclusive benefits",
        benefits: [
          "VIP seating area",
          "Priority entry",
          "Complimentary refreshments",
          "Exclusive merchandise",
          "Meet & greet opportunity"
        ],
        available: Math.floor(event.available_quantity * 0.15) // 15% for VIP
      });
    }

    // Add premium option for high-value events
    if (basePrice > 200) {
      ticketTypes.push({
        id: "premium",
        name: "Premium Package",
        price: Math.round(basePrice * 2.5), // 150% markup for premium
        description: "Ultimate experience with all premium benefits",
        benefits: [
          "Front row seating",
          "Backstage access",
          "Professional photos",
          "Premium dining",
          "Exclusive merchandise",
          "Private meet & greet"
        ],
        available: Math.floor(event.available_quantity * 0.05) // 5% for premium
      });
    }

    return ticketTypes;
  };

  const currentTicketTypes = event ? generateTicketTypes(event) : [];
  const selectedTicket = currentTicketTypes.find(t => t.id === selectedTicketType);
  const totalPrice = selectedTicket ? selectedTicket.price * quantity : 0;

  const handleProceedToPayment = () => {
    if (!paymentMethod || !customerInfo.firstName || !customerInfo.email || !customerInfo.phone) {
      alert("Please fill in all required fields and select a payment method");
      return;
    }

    if (!event || !selectedTicket) {
      alert("Event or ticket type not found");
      return;
    }

    // Create ticket purchase data in the format expected by TicketCheckout
    const ticketPurchaseData = {
      type: 'ticket',
      ticketId: event.id,
      ticketTitle: event.title,
      venue: event.venue?.name || 'TBA',
      eventDate: event.event_date,
      quantity: quantity,
      unitPrice: selectedTicket.price,
      totalAmount: totalPrice,
      customerInfo: {
        name: `${customerInfo.firstName} ${customerInfo.lastName}`.trim(),
        email: customerInfo.email,
        phone: customerInfo.phone
      }
    };

    // Store ticket purchase data in localStorage for the checkout process
    localStorage.setItem('pendingTicketPurchase', JSON.stringify(ticketPurchaseData));

    // Navigate to ticket-specific checkout
    navigate('/ticket-checkout');
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-ghana-green mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Loading Event Details...</h2>
            <p className="text-gray-600">Please wait while we fetch the event information</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error || !event) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <Ticket className="h-16 w-16 text-red-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {error ? 'Error Loading Event' : 'Event Not Found'}
            </h2>
            <p className="text-gray-600 mb-6">
              {error || "The event you're looking for doesn't exist."}
            </p>
            <div className="space-x-4">
              <Button onClick={() => window.location.reload()} variant="outline">
                Try Again
              </Button>
              <Button onClick={() => navigate("/tickets")} className="bg-ghana-green hover:bg-ghana-green/90">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Events
              </Button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Header */}
      <div className="bg-gray-50 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate(-1)}
                className="p-2"
              >
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Buy Tickets</h1>
                <p className="text-gray-600">Secure your spot at this amazing event</p>
              </div>
            </div>
            <Badge className="bg-ghana-green text-white px-4 py-2">
              Step 1 of 2
            </Badge>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Event Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Music className="h-5 w-5 text-ghana-green" />
                  <span>Event Details</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex space-x-4">
                  <img 
                    src={event.image || "https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg?auto=compress&cs=tinysrgb&w=600"} 
                    alt={event.title}
                    className="w-24 h-24 object-cover rounded-lg"
                  />
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-1">{event.title}</h3>
                    <p className="text-gray-600 mb-2">{event.venue?.name || 'Venue TBA'}</p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm">
                      <div className="flex items-center space-x-1">
                        <Calendar className="h-4 w-4 text-gray-500" />
                        <span>{new Date(event.event_date).toLocaleDateString('en-GB')}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="h-4 w-4 text-gray-500" />
                        <span>{new Date(event.event_date).toLocaleTimeString('en-GB', {
                          hour: '2-digit',
                          minute: '2-digit'
                        })}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="h-4 w-4 text-gray-500" />
                        <span>{event.venue ? `${event.venue.name}, ${event.venue.city}` : 'Venue TBA'}</span>
                      </div>
                    </div>
                    
                    {/* Additional event info */}
                    <div className="mt-2 flex flex-wrap gap-2">
                      <Badge variant="outline" className="text-xs">
                        {event.category.name}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        {event.ticket_type}
                      </Badge>
                      {event.is_featured && (
                        <Badge className="text-xs bg-red-500 text-white">
                          Featured
                        </Badge>
                      )}
                      {(event.discount_percentage || 0) > 0 && (
                        <Badge className="text-xs bg-green-500 text-white">
                          {event.discount_percentage}% OFF
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Ticket Types */}
            <Card>
              <CardHeader>
                <CardTitle>Select Ticket Type</CardTitle>
                <CardDescription>Choose your preferred ticket option</CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup value={selectedTicketType} onValueChange={setSelectedTicketType} className="space-y-4">
                  {currentTicketTypes.map((ticket) => (
                    <div key={ticket.id} className="flex items-start space-x-3 p-4 border rounded-lg">
                      <RadioGroupItem value={ticket.id} id={ticket.id} className="mt-1" />
                      <Label htmlFor={ticket.id} className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="font-semibold">{ticket.name}</h4>
                              <span className="text-xl font-bold text-ghana-green">
                                {event.currency}{ticket.price}
                              </span>
                            </div>
                            <p className="text-gray-600 text-sm mb-2">{ticket.description}</p>
                            <div className="space-y-1">
                              {ticket.benefits.map((benefit, index) => (
                                <div key={index} className="flex items-center space-x-2 text-sm text-gray-600">
                                  <span className="w-1 h-1 bg-ghana-green rounded-full"></span>
                                  <span>{benefit}</span>
                                </div>
                              ))}
                            </div>
                            <p className="text-xs text-gray-500 mt-2">
                              {ticket.available} tickets available
                            </p>
                          </div>
                        </div>
                      </Label>
                    </div>
                  ))}
                </RadioGroup>
              </CardContent>
            </Card>

            {/* Quantity Selection */}
            <Card>
              <CardHeader>
                <CardTitle>Number of Tickets</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-4">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(Math.max(event.min_purchase || 1, quantity - 1))}
                    disabled={quantity <= (event.min_purchase || 1)}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <span className="text-xl font-semibold w-12 text-center">{quantity}</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(Math.min(event.max_purchase || 10, quantity + 1))}
                    disabled={quantity >= (event.max_purchase || 10)}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                  <span className="text-sm text-gray-600">
                    Min: {event.min_purchase || 1}, Max: {event.max_purchase || 10} tickets per purchase
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Customer Information */}
            <Card>
              <CardHeader>
                <CardTitle>Customer Information</CardTitle>
                <CardDescription>Please provide your details for ticket delivery</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="firstName">First Name *</Label>
                    <Input
                      id="firstName"
                      value={customerInfo.firstName}
                      onChange={(e) => setCustomerInfo({...customerInfo, firstName: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="lastName">Last Name *</Label>
                    <Input
                      id="lastName"
                      value={customerInfo.lastName}
                      onChange={(e) => setCustomerInfo({...customerInfo, lastName: e.target.value})}
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <Label htmlFor="email">Email Address *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={customerInfo.email}
                    onChange={(e) => setCustomerInfo({...customerInfo, email: e.target.value})}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="phone">Phone Number *</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={customerInfo.phone}
                    onChange={(e) => setCustomerInfo({...customerInfo, phone: e.target.value})}
                    required
                  />
                </div>
              </CardContent>
            </Card>

            {/* Payment Method */}
            <Card>
              <CardHeader>
                <CardTitle>Payment Method</CardTitle>
              </CardHeader>
              <CardContent>
                <RadioGroup value={paymentMethod} onValueChange={setPaymentMethod} className="space-y-3">
                  <div className="flex items-center space-x-3 p-3 border rounded-lg">
                    <RadioGroupItem value="mobile-money" id="mobile-money" />
                    <Label htmlFor="mobile-money" className="flex-1 cursor-pointer">
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="font-medium">Mobile Money</p>
                          <p className="text-sm text-gray-600">MTN, Vodafone, AirtelTigo</p>
                        </div>
                        <Badge variant="outline" className="text-green-600">Instant</Badge>
                      </div>
                    </Label>
                  </div>
                  
                  <div className="flex items-center space-x-3 p-3 border rounded-lg">
                    <RadioGroupItem value="paystack" id="paystack" />
                    <Label htmlFor="paystack" className="flex-1 cursor-pointer">
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="font-medium">Card Payment</p>
                          <p className="text-sm text-gray-600">Visa, Mastercard, Verve</p>
                        </div>
                        <Badge variant="outline" className="text-blue-600">Secure</Badge>
                      </div>
                    </Label>
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>
          </div>

          {/* Summary Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {selectedTicket && (
                  <>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm">{selectedTicket.name}</span>
                        <span className="text-sm font-medium">GH₵{selectedTicket.price}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm">Quantity</span>
                        <span className="text-sm font-medium">× {quantity}</span>
                      </div>
                      {(event.discount_percentage || 0) > 0 && (
                        <div className="flex justify-between text-green-600">
                          <span className="text-sm">Discount ({event.discount_percentage}%)</span>
                          <span className="text-sm font-medium">
                            -GH₵{((parseFloat(event.price || '0') - parseFloat(event.effective_price || '0')) * quantity).toFixed(2)}
                          </span>
                        </div>
                      )}
                    </div>
                    
                    <Separator />
                    
                    <div className="flex justify-between items-center text-lg font-bold">
                      <span>Total</span>
                      <span className="text-ghana-green">GH₵{totalPrice.toLocaleString()}</span>
                    </div>

                    <Button 
                      onClick={handleProceedToPayment}
                      disabled={!paymentMethod || !selectedTicket}
                      className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                    >
                      Proceed to Payment
                    </Button>

                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                      <div className="flex items-start space-x-2">
                        <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                        <div className="text-xs text-blue-800">
                          <p className="font-medium">Ticket Policy</p>
                          <p>
                            {event.is_refundable 
                              ? "Refundable tickets - cancellation allowed up to 24 hours before event." 
                              : "Tickets are non-refundable."
                            } Free name changes up to 24 hours before event.
                          </p>
                          {event.terms_conditions && event.terms_conditions.trim() && (
                            <p className="mt-1">{event.terms_conditions}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
