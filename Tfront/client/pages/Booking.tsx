import { useState, useEffect } from "react";
import { useParams, useLocation, Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
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
  MapPin, Calendar, Users, ArrowLeft, CreditCard, Smartphone, 
  Building2, Check, Star, Clock, Hotel, Car, Utensils, Shield,
  Plus, Minus, ChevronDown, ChevronUp, Info
} from "lucide-react";
import { apiClient, destinationsApi } from "@/lib/api";

interface BookingState {
  tourId: string;
  tourName: string;
  duration: string;
  basePrice: number;
  selectedDate: string;
  startDate?: string;
  endDate?: string;
  travelers: {
    adults: number;
    children: number;
  };
}

interface AddOnOption {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  selected: boolean;
  options?: {
    id: string;
    name: string;
    price: number;
  }[];
}

export default function Booking() {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [searchParams] = useSearchParams();
  
  const [loadingFromDatabase, setLoadingFromDatabase] = useState(false);
  const [loadedFromPayment, setLoadedFromPayment] = useState(false);
  const [loadingTourData, setLoadingTourData] = useState(false);
  const [tourData, setTourData] = useState<any>(null);
  
  // Get booking data from navigation state or use defaults
  const [bookingData, setBookingData] = useState<BookingState>(() => {
    if (location.state) {
      return location.state as BookingState;
    }
    return {
      tourId: id || "1",
      tourName: "Loading...",
      duration: "3 Days", 
      basePrice: 0,
      selectedDate: new Date().toISOString().split('T')[0],
      travelers: { adults: 1, children: 0 }
    };
  });

  const [addOns, setAddOns] = useState<AddOnOption[]>([
    // Accommodation
    {
      id: "accommodation",
      name: "Accommodation Upgrade",
      description: "Choose your preferred accommodation level",
      price: 0,
      category: "accommodation",
      selected: false,
      options: [
        { id: "standard", name: "Standard Hotel (included)", price: 0 },
        { id: "premium", name: "Premium Hotel", price: 500 },
        { id: "luxury", name: "Luxury Resort", price: 1200 }
      ]
    },
    // Transport
    {
      id: "transport",
      name: "Transport Options",
      description: "Upgrade your transportation",
      price: 0,
      category: "transport",
      selected: false,
      options: [
        { id: "shared", name: "Shared Bus (included)", price: 0 },
        { id: "private", name: "Private Van", price: 800 },
        { id: "airport", name: "Airport Pickup & Drop", price: 400 }
      ]
    },
    // Meals
    {
      id: "meals",
      name: "Meal Options",
      description: "Customize your dining experience",
      price: 0,
      category: "meals", 
      selected: false,
      options: [
        { id: "standard", name: "Standard Meals (included)", price: 0 },
        { id: "vegetarian", name: "Vegetarian / Vegan Option", price: 0 },
        { id: "luxury", name: "Luxury Dining Package", price: 300 }
      ]
    },
    // Medical & Insurance
    {
      id: "medical",
      name: "Medical & Insurance",
      description: "Additional health and safety coverage",
      price: 0,
      category: "medical",
      selected: false,
      options: [
        { id: "basic", name: "Basic First Aid (included)", price: 0 },
        { id: "insurance", name: "Travel Insurance", price: 200 },
        { id: "support", name: "On-call Medical Support", price: 500 }
      ]
    },
    // Experiences
    {
      id: "cultural",
      name: "Cultural Experience",
      description: "Drumming, cooking, local market tour",
      price: 250,
      category: "experience",
      selected: false
    },
    {
      id: "adventure",
      name: "Adventure Add-on", 
      description: "Kakum Canopy Walk, Beach Trip",
      price: 400,
      category: "experience",
      selected: false
    }
  ]);

  const [selectedOptions, setSelectedOptions] = useState<{ [key: string]: string }>({
    accommodation: "standard",
    transport: "shared", 
    meals: "standard",
    medical: "basic"
  });

  const [paymentMethod, setPaymentMethod] = useState<string>("");
  const [paymentMethods, setPaymentMethods] = useState<any[]>([]);
  const [showBreakdown, setShowBreakdown] = useState(true);

  // Load tour data from API to get pricing tiers
  useEffect(() => {
    const loadTourData = async () => {
      // Skip if we have a payment reference (will be loaded by other useEffect)
      const paymentRef = searchParams.get('payment') || searchParams.get('ref');
      if (paymentRef) {
        return;
      }

      if (!id) {
        return;
      }

      try {
        setLoadingTourData(true);
        console.log('Loading tour data from API for:', id);
        
        const tour = await destinationsApi.getDestination(id);
        setTourData(tour); // Store full tour data including pricing tiers
        
        // Load add-ons from tour data
        if (tour.addon_options || tour.experience_addons) {
          const loadedAddOns: AddOnOption[] = [];
          
          // Group addon_options by category
          const addonsByCategory: { [key: string]: any[] } = {};
          tour.addon_options?.forEach((addon: any) => {
            const categoryName = addon.category.name;
            if (!addonsByCategory[categoryName]) {
              addonsByCategory[categoryName] = [];
            }
            addonsByCategory[categoryName].push(addon);
          });
          
          // Convert to AddOnOption format
          Object.entries(addonsByCategory).forEach(([categoryName, addons]) => {
            const category = addons[0].category;
            loadedAddOns.push({
              id: categoryName,
              name: category.display_name,
              description: category.description,
              price: 0,
              category: categoryName,
              selected: false,
              options: addons.map((addon: any) => ({
                id: addon.id.toString(),
                name: addon.name,
                price: parseFloat(addon.price)
              }))
            });
          });
          
          // Add experience add-ons
          tour.experience_addons?.forEach((exp: any) => {
            loadedAddOns.push({
              id: exp.id.toString(),
              name: exp.name,
              description: exp.description,
              price: parseFloat(exp.price),
              category: "experience",
              selected: false
            });
          });
          
          if (loadedAddOns.length > 0) {
            setAddOns(loadedAddOns);
            console.log('Loaded add-ons from database:', loadedAddOns);
          }
        }
        
        // Only update booking data if we don't have navigation state
        if (location.state) {
          console.log('Using navigation state, but storing tour data for pricing tiers');
          return;
        }
        
        // Calculate default selected date
        let defaultDate = new Date().toISOString().split('T')[0];
        if (tour.start_date) {
          const startDate = new Date(tour.start_date);
          const today = new Date();
          const effectiveDate = startDate > today ? startDate : today;
          defaultDate = effectiveDate.toISOString().split('T')[0];
        }
        
        setBookingData({
          tourId: tour.id.toString(),
          tourName: tour.name,
          duration: tour.duration_display,
          basePrice: parseFloat(tour.price),
          selectedDate: defaultDate,
          startDate: tour.start_date,
          endDate: tour.end_date,
          travelers: { adults: 1, children: 0 }
        });
        
        console.log('Loaded tour data:', tour.name, 'Pricing tiers:', tour.pricing_tiers);
      } catch (error) {
        console.error('Error loading tour data:', error);
      } finally {
        setLoadingTourData(false);
      }
    };
    
    loadTourData();
  }, [id, location.state, searchParams]);

  // Load booking from database if payment reference is provided
  useEffect(() => {
    const loadBookingFromDatabase = async () => {
      const paymentRef = searchParams.get('payment') || searchParams.get('ref');
      
      if (!paymentRef) {
        return; // No payment reference, use default/state data
      }

      try {
        setLoadingFromDatabase(true);
        console.log('Loading booking from payment:', paymentRef);
        
        const payment = await apiClient.getPaymentStatus(paymentRef);
        
        if (payment.metadata?.booking_details) {
          const details = payment.metadata.booking_details;
          console.log('Loaded booking details:', details);
          
          // Update booking data from database
          setBookingData({
            tourId: id || "1",
            tourName: details.destination?.name || "Tour Package",
            duration: details.destination?.duration || "3 Days / 2 Nights",
            basePrice: details.pricing?.base_total ? 
              details.pricing.base_total / (details.travelers?.adults || 1) : 
              1500,
            selectedDate: details.selected_date || new Date().toISOString().split('T')[0],
            travelers: {
              adults: details.travelers?.adults || 2,
              children: details.travelers?.children || 0
            }
          });
          
          // Update selected options if available
          if (details.selected_options) {
            const newSelectedOptions: { [key: string]: string } = {};
            
            if (details.selected_options.accommodation) {
              // Map accommodation name to option id
              const accName = details.selected_options.accommodation.name.toLowerCase();
              if (accName.includes('luxury')) newSelectedOptions.accommodation = 'luxury';
              else if (accName.includes('premium')) newSelectedOptions.accommodation = 'premium';
              else newSelectedOptions.accommodation = 'standard';
            }
            
            if (details.selected_options.transport) {
              const transName = details.selected_options.transport.name.toLowerCase();
              if (transName.includes('private')) newSelectedOptions.transport = 'private';
              else if (transName.includes('airport')) newSelectedOptions.transport = 'airport';
              else newSelectedOptions.transport = 'shared';
            }
            
            if (details.selected_options.meals) {
              const mealName = details.selected_options.meals.name.toLowerCase();
              if (mealName.includes('luxury')) newSelectedOptions.meals = 'luxury-meals';
              else if (mealName.includes('vegetarian') || mealName.includes('vegan')) newSelectedOptions.meals = 'vegetarian';
              else newSelectedOptions.meals = 'standard';
            }
            
            setSelectedOptions(prev => ({ ...prev, ...newSelectedOptions }));
          }
          
          setLoadedFromPayment(true);
        }
      } catch (error) {
        console.error('Error loading booking from database:', error);
      } finally {
        setLoadingFromDatabase(false);
      }
    };
    
    loadBookingFromDatabase();
  }, [searchParams, id]);

  // Load payment methods from API
  useEffect(() => {
    const loadPaymentMethods = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/payments/checkout/methods/');
        const data = await response.json();
        setPaymentMethods(data.payment_methods || []);
      } catch (error) {
        console.error('Error loading payment methods:', error);
        // Fallback to default methods if API fails
        setPaymentMethods([
          {
            id: 'mobile_money',
            name: 'Mobile Money',
            description: 'MTN, Vodafone, AirtelTigo',
            icon: '📱',
            processing_time: 'Instant',
            providers: [{ name: 'MTN Mobile Money' }]
          }
        ]);
      }
    };
    
    loadPaymentMethods();
  }, []);

  // Helper function to get price for group size using pricing tiers
  const getPriceForGroup = (numPeople: number): number => {
    if (!tourData?.pricing_tiers || tourData.pricing_tiers.length === 0) {
      // No pricing tiers, use base price * number of people
      return bookingData.basePrice * numPeople;
    }
    
    // Find matching pricing tier
    const tier = tourData.pricing_tiers.find((t: any) => 
      numPeople >= t.min_people && numPeople <= t.max_people
    );
    
    if (tier) {
      return parseFloat(tier.total_price);
    }
    
    // Fallback to base price * number of people
    return bookingData.basePrice * numPeople;
  };

  // Calculate total price
  const calculateTotal = () => {
    const baseTotal = getPriceForGroup(bookingData.travelers.adults);
    
    let addOnTotal = 0;
    
    // Calculate option upgrades
    Object.entries(selectedOptions).forEach(([category, optionId]) => {
      const addOn = addOns.find(a => a.id === category);
      if (addOn?.options) {
        const option = addOn.options.find(o => o.id === optionId);
        if (option && option.price > 0) {
          addOnTotal += option.price * bookingData.travelers.adults;
        }
      }
    });

    // Calculate experience add-ons
    addOns.forEach(addOn => {
      if (addOn.category === "experience" && addOn.selected) {
        addOnTotal += addOn.price;
      }
    });

    return { baseTotal, addOnTotal, total: baseTotal + addOnTotal };
  };

  const totals = calculateTotal();

  const handleOptionChange = (category: string, optionId: string) => {
    setSelectedOptions(prev => ({
      ...prev,
      [category]: optionId
    }));
  };

  const handleAddOnToggle = (id: string) => {
    setAddOns(prev => prev.map(addOn => 
      addOn.id === id ? { ...addOn, selected: !addOn.selected } : addOn
    ));
  };

  const handleTravelersChange = (type: 'adults' | 'children', increment: boolean) => {
    const maxGroupSize = tourData?.max_group_size || 10; // Default to 10 if not set
    
    setBookingData(prev => {
      const newValue = prev.travelers[type] + (increment ? 1 : -1);
      const totalTravelers = type === 'adults' 
        ? newValue + prev.travelers.children 
        : prev.travelers.adults + newValue;
      
      // Don't allow exceeding max group size
      if (totalTravelers > maxGroupSize) {
        return prev;
      }
      
      return {
        ...prev,
        travelers: {
          ...prev.travelers,
          [type]: Math.max(0, newValue)
        }
      };
    });
  };

  const handleProceedToPayment = () => {
    if (!paymentMethod) {
      alert("Please select a payment method");
      return;
    }

    if (!isAuthenticated) {
      alert("Please log in to complete your booking");
      navigate("/login", { state: { returnUrl: location.pathname } });
      return;
    }

    const paymentData = {
      tourName: bookingData.tourName,
      total: totals.total,
      bookingReference: `GH${Date.now().toString().slice(-6)}`,
      paymentMethod: paymentMethod,
      userInfo: {
        id: user?.id,
        name: user?.name,
        email: user?.email,
        phone: user?.phone
      },
      bookingDetails: {
        bookingData,
        selectedOptions,
        addOns: addOns.filter(a => a.selected)
      }
    };

    // Navigate to appropriate payment method
    if (paymentMethod === "mobile_money") {
      navigate("/momo-checkout", { state: paymentData });
    } else if (paymentMethod === "card") {
      // Card payments removed - show message
      alert("Card payments are no longer supported. Please use MTN Mobile Money.");
      return;
    } else if (paymentMethod === "bank_transfer") {
      // Show bank transfer information
      alert("Bank transfer details will be provided via email. Please contact support for large group bookings.");
    } else {
      // Other payment methods
      alert(`Payment method ${paymentMethod} will be available soon. Please try Mobile Money or Card payment.`);
    }
  };

  if (loadingFromDatabase || loadingTourData) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ghana-green mx-auto mb-4"></div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {loadingTourData ? 'Loading Tour Details' : 'Loading Booking Details'}
            </h2>
            <p className="text-gray-600">
              {loadingTourData ? 'Fetching tour information from database...' : 'Fetching your booking information from database...'}
            </p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!bookingData) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Invalid Booking</h2>
            <p className="text-gray-600 mb-6">No booking data found.</p>
            <Link to="/destinations">
              <Button className="bg-ghana-green hover:bg-ghana-green/90">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Destinations
              </Button>
            </Link>
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
                <h1 className="text-2xl font-bold text-gray-900">Complete Your Booking</h1>
                <p className="text-gray-600">Review and customize your tour package</p>
              </div>
            </div>
            <Badge className="bg-ghana-green text-white px-4 py-2">
              Step 2 of 3
            </Badge>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* 🔹 Login Prompt for Unauthenticated Users */}
            {!isAuthenticated && (
              <Card className="border-amber-200 bg-amber-50">
                <CardContent className="pt-6">
                  <div className="flex items-center space-x-3">
                    <Info className="h-5 w-5 text-amber-600" />
                    <div className="flex-1">
                      <p className="text-amber-800 font-medium">Sign in to complete your booking</p>
                      <p className="text-amber-700 text-sm">You'll need an account to proceed with payment and receive booking confirmations.</p>
                    </div>
                    <div className="flex space-x-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => navigate("/login", { state: { returnUrl: location.pathname } })}
                        className="border-amber-300 text-amber-700 hover:bg-amber-100"
                      >
                        Sign In
                      </Button>
                      <Button 
                        size="sm"
                        onClick={() => navigate("/register", { state: { returnUrl: location.pathname } })}
                        className="bg-ghana-green hover:bg-ghana-green/90"
                      >
                        Create Account
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* 🔹 1. User Information */}
            {isAuthenticated && user && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Users className="h-5 w-5 text-ghana-green" />
                    <span>Booking For</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div className="w-12 h-12 bg-ghana-green text-white rounded-full flex items-center justify-center font-semibold">
                      {user.first_name.charAt(0)}{user.last_name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{user.name}</h3>
                      <p className="text-gray-600">{user.email}</p>
                      {user.phone && <p className="text-gray-600">{user.phone}</p>}
                    </div>
                    <Badge variant="outline" className="ml-auto border-ghana-green text-ghana-green">
                      Member since {new Date(user.memberSince).getFullYear()}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* 🔹 2. Booking Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-ghana-green" />
                  <span>Booking Summary</span>
                  {loadedFromPayment && (
                    <Badge variant="outline" className="ml-2 border-blue-500 text-blue-600">
                      Loaded from Database
                    </Badge>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {bookingData.tourName}
                      </h3>
                      <p className="text-gray-600">{bookingData.duration}</p>
                    </div>
                    <Badge variant="outline" className="border-ghana-green text-ghana-green">
                      Heritage Tour
                    </Badge>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-gray-50 p-4 rounded-lg">
                    <div>
                      <Label className="text-sm text-gray-600">Dates</Label>
                      <p className="font-medium">
                        {bookingData.startDate && bookingData.endDate ? (
                          <>
                            {new Date(bookingData.startDate).toLocaleDateString('en-GB', {
                              day: 'numeric',
                              month: 'short',
                              year: 'numeric'
                            })} – {new Date(bookingData.endDate).toLocaleDateString('en-GB', {
                              day: 'numeric',
                              month: 'short',
                              year: 'numeric'
                            })}
                          </>
                        ) : (
                          <>
                            {new Date(bookingData.selectedDate).toLocaleDateString('en-GB', {
                              day: 'numeric',
                              month: 'short',
                              year: 'numeric'
                            })}
                          </>
                        )}
                      </p>
                    </div>
                    
                    <div>
                      <Label className="text-sm text-gray-600">
                        Travelers
                        {tourData?.max_group_size && (
                          <span className="text-xs text-gray-500 ml-2">(Max {tourData.max_group_size})</span>
                        )}
                      </Label>
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleTravelersChange('adults', false)}
                          disabled={bookingData.travelers.adults <= 1}
                        >
                          <Minus className="h-3 w-3" />
                        </Button>
                        <span className="font-medium">{bookingData.travelers.adults} {bookingData.travelers.adults === 1 ? 'Adult' : 'Adults'}</span>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleTravelersChange('adults', true)}
                          disabled={bookingData.travelers.adults >= (tourData?.max_group_size || 10)}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                    
                    <div>
                      <Label className="text-sm text-gray-600">Base Price</Label>
                      <p className="font-medium text-lg">GH₵{bookingData.basePrice.toLocaleString()} per person</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 🔹 3. Select/Add-On Options */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Star className="h-5 w-5 text-ghana-green" />
                  <span>Customize Your Experience</span>
                </CardTitle>
                <CardDescription>
                  Select upgrades and add-ons to enhance your tour
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                
                {/* Show database add-ons if available */}
                {tourData?.addon_options && tourData.addon_options.length > 0 && (
                  <div className="space-y-4">
                    <p className="text-sm text-gray-600">Available add-ons for this tour:</p>
                    {addOns.filter(a => a.options).map((addOn) => {
                      // If only one option, show it directly without expansion
                      const singleOption = addOn.options?.length === 1 ? addOn.options[0] : null;
                      
                      return (
                        <div key={addOn.id} className="space-y-3">
                          <div className="flex items-center space-x-3 p-3 border rounded-lg">
                            <Checkbox
                              id={`addon-${addOn.id}`}
                              checked={addOn.selected}
                              onCheckedChange={() => handleAddOnToggle(addOn.id)}
                            />
                            <Label htmlFor={`addon-${addOn.id}`} className="flex-1 cursor-pointer">
                              <div className="flex justify-between items-center">
                                <div>
                                  <p className="font-medium">
                                    {singleOption ? singleOption.name : addOn.name}
                                  </p>
                                  {!singleOption && (
                                    <p className="text-sm text-gray-600">{addOn.description}</p>
                                  )}
                                </div>
                                {singleOption && singleOption.price > 0 && (
                                  <span className="text-ghana-green font-medium">
                                    +GH₵{singleOption.price.toLocaleString()}
                                  </span>
                                )}
                              </div>
                            </Label>
                          </div>
                          
                          {/* Show options when selected (only if multiple options) */}
                          {addOn.selected && !singleOption && addOn.options && addOn.options.length > 1 && (
                            <div className="ml-8 space-y-2">
                              <p className="text-sm font-medium text-gray-700">Choose option:</p>
                              <RadioGroup 
                                value={selectedOptions[addOn.id] || addOn.options[0]?.id}
                                onValueChange={(value) => handleOptionChange(addOn.id, value)}
                                className="space-y-2"
                              >
                                {addOn.options.map((option) => (
                                  <div key={option.id} className="flex items-center space-x-2 p-2 border rounded">
                                    <RadioGroupItem value={option.id} id={`${addOn.id}-${option.id}`} />
                                    <Label htmlFor={`${addOn.id}-${option.id}`} className="flex-1 cursor-pointer">
                                      <div className="flex justify-between items-center">
                                        <p className="text-sm">{option.name}</p>
                                        <span className="text-sm text-ghana-green">
                                          {option.price === 0 ? 'Included' : `+GH₵${option.price.toLocaleString()}`}
                                        </span>
                                      </div>
                                    </Label>
                                  </div>
                                ))}
                              </RadioGroup>
                            </div>
                          )}
                        </div>
                      );
                    })}
                    
                    {/* Experience add-ons */}
                    {addOns.filter(a => a.category === "experience").length > 0 && (
                      <div className="space-y-3">
                        <h4 className="font-semibold">Additional Experiences</h4>
                        {addOns.filter(a => a.category === "experience").map((addOn) => (
                          <div key={addOn.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                            <Checkbox
                              id={addOn.id}
                              checked={addOn.selected}
                              onCheckedChange={() => handleAddOnToggle(addOn.id)}
                            />
                            <Label htmlFor={addOn.id} className="flex-1 cursor-pointer">
                              <div className="flex justify-between items-center">
                                <div>
                                  <p className="font-medium">{addOn.name}</p>
                                  <p className="text-sm text-gray-600">{addOn.description}</p>
                                </div>
                                <span className="text-ghana-green font-medium">+GH₵{addOn.price.toLocaleString()}</span>
                              </div>
                            </Label>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
                
                {/* Fallback to hardcoded add-ons if none from database */}
                {(!tourData?.addon_options || tourData.addon_options.length === 0) && (
                  <>
                {/* A. Accommodation */}
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Hotel className="h-5 w-5 text-ghana-green" />
                    <h4 className="font-semibold">Accommodation Options</h4>
                  </div>
                  <RadioGroup 
                    value={selectedOptions.accommodation} 
                    onValueChange={(value) => handleOptionChange('accommodation', value)}
                    className="space-y-2"
                  >
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="standard" id="standard" />
                      <Label htmlFor="standard" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Standard Hotel</p>
                            <p className="text-sm text-gray-600">Included in base package</p>
                          </div>
                          <span className="text-ghana-green font-medium">Included</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="premium" id="premium" />
                      <Label htmlFor="premium" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Premium Hotel</p>
                            <p className="text-sm text-gray-600">4-star accommodation with pool & spa</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵500 per person</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="luxury" id="luxury" />
                      <Label htmlFor="luxury" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Luxury Resort</p>
                            <p className="text-sm text-gray-600">5-star beachfront resort with premium amenities</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵1,200 per person</span>
                        </div>
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                <Separator />

                {/* B. Transport */}
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Car className="h-5 w-5 text-ghana-green" />
                    <h4 className="font-semibold">Transport Options</h4>
                  </div>
                  <RadioGroup 
                    value={selectedOptions.transport} 
                    onValueChange={(value) => handleOptionChange('transport', value)}
                    className="space-y-2"
                  >
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="shared" id="shared" />
                      <Label htmlFor="shared" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Shared Bus</p>
                            <p className="text-sm text-gray-600">Comfortable group transportation</p>
                          </div>
                          <span className="text-ghana-green font-medium">Included</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="private" id="private" />
                      <Label htmlFor="private" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Private Van</p>
                            <p className="text-sm text-gray-600">Exclusive vehicle for your group</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵800</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="airport" id="airport" />
                      <Label htmlFor="airport" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Airport Pickup & Drop</p>
                            <p className="text-sm text-gray-600">Convenient airport transfers</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵400</span>
                        </div>
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                <Separator />

                {/* C. Meals */}
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Utensils className="h-5 w-5 text-ghana-green" />
                    <h4 className="font-semibold">Meal Options</h4>
                  </div>
                  <RadioGroup 
                    value={selectedOptions.meals} 
                    onValueChange={(value) => handleOptionChange('meals', value)}
                    className="space-y-2"
                  >
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="standard" id="meals-standard" />
                      <Label htmlFor="meals-standard" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Standard Meals</p>
                            <p className="text-sm text-gray-600">Local cuisine and international options</p>
                          </div>
                          <span className="text-ghana-green font-medium">Included</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="vegetarian" id="vegetarian" />
                      <Label htmlFor="vegetarian" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Vegetarian / Vegan Option</p>
                            <p className="text-sm text-gray-600">Plant-based meals throughout the tour</p>
                          </div>
                          <span className="text-ghana-green font-medium">No extra charge</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="luxury-meals" id="luxury-meals" />
                      <Label htmlFor="luxury-meals" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Luxury Dining Package</p>
                            <p className="text-sm text-gray-600">Fine dining and premium restaurants</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵300</span>
                        </div>
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                <Separator />

                {/* D. Medical & Insurance */}
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Shield className="h-5 w-5 text-ghana-green" />
                    <h4 className="font-semibold">Medical & Insurance</h4>
                  </div>
                  <RadioGroup 
                    value={selectedOptions.medical} 
                    onValueChange={(value) => handleOptionChange('medical', value)}
                    className="space-y-2"
                  >
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="basic" id="basic-medical" />
                      <Label htmlFor="basic-medical" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Basic First Aid</p>
                            <p className="text-sm text-gray-600">Standard first aid coverage</p>
                          </div>
                          <span className="text-ghana-green font-medium">Included</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="insurance" id="travel-insurance" />
                      <Label htmlFor="travel-insurance" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Travel Insurance</p>
                            <p className="text-sm text-gray-600">Comprehensive coverage for emergencies</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵200</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-2 p-3 border rounded-lg">
                      <RadioGroupItem value="support" id="medical-support" />
                      <Label htmlFor="medical-support" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">On-call Medical Support</p>
                            <p className="text-sm text-gray-600">24/7 medical assistance available</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵500</span>
                        </div>
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                <Separator />

                {/* E. Extras / Experiences */}
                <div className="space-y-3">
                  <h4 className="font-semibold">Additional Experiences</h4>
                  
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3 p-3 border rounded-lg">
                      <Checkbox
                        id="cultural"
                        checked={addOns.find(a => a.id === "cultural")?.selected}
                        onCheckedChange={() => handleAddOnToggle("cultural")}
                      />
                      <Label htmlFor="cultural" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Cultural Experience</p>
                            <p className="text-sm text-gray-600">Traditional drumming, cooking class, local market tour</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵250</span>
                        </div>
                      </Label>
                    </div>
                    
                    <div className="flex items-center space-x-3 p-3 border rounded-lg">
                      <Checkbox
                        id="adventure"
                        checked={addOns.find(a => a.id === "adventure")?.selected}
                        onCheckedChange={() => handleAddOnToggle("adventure")}
                      />
                      <Label htmlFor="adventure" className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">Adventure Add-on</p>
                            <p className="text-sm text-gray-600">Kakum Canopy Walk, Beach Trip, Nature Photography</p>
                          </div>
                          <span className="text-ghana-green font-medium">+GH₵400</span>
                        </div>
                      </Label>
                    </div>
                  </div>
                </div>
                  </>
                )}
              </CardContent>
            </Card>

            {/* 🔹 4. Payment Methods */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <CreditCard className="h-5 w-5 text-ghana-green" />
                  <span>Payment Method</span>
                </CardTitle>
                <CardDescription>Choose your preferred payment option</CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup value={paymentMethod} onValueChange={setPaymentMethod} className="space-y-3">
                  {paymentMethods.map((method) => {
                    // Only show methods with providers or bank transfer
                    if (method.providers?.length === 0 && method.id !== 'bank_transfer') {
                      return null;
                    }

                    const getIcon = (methodId: string) => {
                      switch (methodId) {
                        case 'mobile_money':
                          return <Smartphone className="h-5 w-5 text-ghana-green" />;
                        case 'card':
                          return <CreditCard className="h-5 w-5 text-ghana-green" />;
                        case 'bank_transfer':
                          return <Building2 className="h-5 w-5 text-ghana-green" />;
                        default:
                          return <CreditCard className="h-5 w-5 text-ghana-green" />;
                      }
                    };

                    const getBadgeColor = (processingTime: string) => {
                      if (processingTime.toLowerCase().includes('instant')) {
                        return 'text-green-600';
                      } else if (processingTime.toLowerCase().includes('secure')) {
                        return 'text-blue-600';
                      } else {
                        return 'text-gray-600';
                      }
                    };

                    return (
                      <div key={method.id} className="flex items-center space-x-3 p-4 border rounded-lg">
                        <RadioGroupItem value={method.id} id={method.id} />
                        <Label htmlFor={method.id} className="flex-1 cursor-pointer">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              {getIcon(method.id)}
                              <div>
                                <p className="font-medium">{method.name}</p>
                                <p className="text-sm text-gray-600">{method.description}</p>
                              </div>
                            </div>
                            <Badge variant="outline" className={getBadgeColor(method.processing_time)}>
                              {method.processing_time}
                            </Badge>
                          </div>
                        </Label>
                      </div>
                    );
                  })}
                </RadioGroup>
              </CardContent>
            </Card>
          </div>

          {/* 🔹 3. Payment Breakdown (Right Sidebar) */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Payment Summary</CardTitle>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowBreakdown(!showBreakdown)}
                    className="p-1"
                  >
                    {showBreakdown ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                  </Button>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {showBreakdown && (
                  <>
                    {/* Base Package */}
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Base Package ({bookingData.travelers.adults} {bookingData.travelers.adults === 1 ? 'traveler' : 'travelers'})</span>
                        <span>GH₵{totals.baseTotal.toLocaleString()}</span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {bookingData.travelers.adults} {bookingData.travelers.adults === 1 ? 'Adult' : 'Adults'} × GH₵{bookingData.basePrice.toLocaleString()}
                      </div>
                    </div>

                    <Separator />

                    {/* Upgrades */}
                    {Object.entries(selectedOptions).map(([category, optionId]) => {
                      const addOn = addOns.find(a => a.id === category);
                      if (!addOn?.options) return null;
                      
                      const option = addOn.options.find(o => o.id === optionId);
                      if (!option || option.price === 0) return null;
                      
                      const upgradeTotal = option.price * bookingData.travelers.adults;
                      
                      return (
                        <div key={category} className="flex justify-between text-sm">
                          <span>{option.name}</span>
                          <span>GH₵{upgradeTotal.toLocaleString()}</span>
                        </div>
                      );
                    })}

                    {/* Experience Add-ons */}
                    {addOns.filter(a => a.category === "experience" && a.selected).map(addOn => (
                      <div key={addOn.id} className="flex justify-between text-sm">
                        <span>{addOn.name}</span>
                        <span>GH₵{addOn.price.toLocaleString()}</span>
                      </div>
                    ))}

                    <Separator />
                  </>
                )}

                {/* Total */}
                <div className="flex justify-between items-center text-lg font-bold">
                  <span>Total</span>
                  <span className="text-ghana-green">GH₵{totals.total.toLocaleString()}</span>
                </div>

                {/* Proceed Button */}
                <Button 
                  onClick={handleProceedToPayment}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                  disabled={!paymentMethod}
                >
                  Proceed to Payment
                </Button>

                {/* Info */}
                <div className="flex items-start space-x-2 text-xs text-gray-600 bg-blue-50 p-3 rounded-lg">
                  <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-blue-800">Secure Payment</p>
                    <p>Your payment information is encrypted and secure. Free cancellation up to 24 hours before departure.</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
