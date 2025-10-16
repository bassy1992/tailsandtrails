import { useState, useEffect } from "react";
import { useParams, useLocation, Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import Layout from "@/components/Layout";
import AddOnSelector from "@/components/AddOnSelector";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Separator } from "@/components/ui/separator";
import { 
  MapPin, Calendar, Users, ArrowLeft, CreditCard, Smartphone, 
  Building2, Check, Star, Clock, Hotel, Car, Utensils, Shield,
  Plus, Minus, ChevronDown, ChevronUp, Info, DollarSign
} from "lucide-react";

interface BookingState {
  tourId: string;
  tourName: string;
  duration: string;
  basePrice: number;
  selectedDate: string;
  travelers: {
    adults: number;
    children: number;
  };
}

interface AddOnSelection {
  addon_id: number;
  option_id?: number;
  quantity: number;
  unit_price: number;
  total_price: number;
  name: string;
}

export default function Booking() {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  
  // Get booking data from navigation state or use defaults
  const [bookingData, setBookingData] = useState<BookingState>(() => {
    if (location.state) {
      return location.state as BookingState;
    }
    return {
      tourId: id || "1",
      tourName: "Cape Coast Castle Heritage Tour",
      duration: "3 Days / 2 Nights", 
      basePrice: 1500,
      selectedDate: "2025-09-20",
      travelers: { adults: 2, children: 1 }
    };
  });

  const [selectedAddOns, setSelectedAddOns] = useState<AddOnSelection[]>([]);
  const [addonTotal, setAddonTotal] = useState<number>(0);
  const [paymentMethod, setPaymentMethod] = useState<string>("");
  const [paymentMethods, setPaymentMethods] = useState<any[]>([]);
  const [showBreakdown, setShowBreakdown] = useState(true);

  // Load payment methods from API
  useEffect(() => {
    const loadPaymentMethods = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/checkout/methods/`);
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

  // Calculate total price
  const calculateTotal = () => {
    const baseTotal = bookingData.basePrice * bookingData.travelers.adults;
    return { baseTotal, addOnTotal: addonTotal, total: baseTotal + addonTotal };
  };

  const totals = calculateTotal();

  // Handle add-on selection changes
  const handleAddOnSelectionChange = (addons: AddOnSelection[], total: number) => {
    setSelectedAddOns(addons);
    setAddonTotal(total);
  };

  const handleTravelersChange = (type: 'adults' | 'children', increment: boolean) => {
    setBookingData(prev => ({
      ...prev,
      travelers: {
        ...prev.travelers,
        [type]: Math.max(0, prev.travelers[type] + (increment ? 1 : -1))
      }
    }));
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
        selectedAddOns,
        addonTotal,
        baseTotal: totals.baseTotal
      }
    };

    // Navigate to appropriate payment method
    if (paymentMethod === "mobile_money") {
      navigate("/momo-checkout", { state: paymentData });
    } else if (paymentMethod === "card") {
      navigate("/paystack-checkout", { state: paymentData });
    } else if (paymentMethod === "bank_transfer") {
      alert("Bank transfer details will be provided via email. Please contact support for large group bookings.");
    } else {
      alert(`Payment method ${paymentMethod} will be available soon. Please try Mobile Money or Card payment.`);
    }
  };

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
            
            {/* Login Prompt for Unauthenticated Users */}
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

            {/* User Information */}
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
                      {user.first_name?.charAt(0)}{user.last_name?.charAt(0)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{user.name}</h3>
                      <p className="text-gray-600">{user.email}</p>
                      {user.phone && <p className="text-gray-600">{user.phone}</p>}
                    </div>
                    <Badge variant="outline" className="ml-auto border-ghana-green text-ghana-green">
                      Member since {new Date(user.memberSince || Date.now()).getFullYear()}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Booking Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-ghana-green" />
                  <span>Booking Summary</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {/* Tour Info Header */}
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-1">
                        {bookingData.tourName}
                      </h3>
                      <p className="text-gray-600 text-sm">{bookingData.duration}</p>
                    </div>
                    <Badge variant="outline" className="border-ghana-green text-ghana-green">
                      Heritage Tour
                    </Badge>
                  </div>
                  
                  {/* Booking Details Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Dates Section */}
                    <div className="space-y-2">
                      <Label className="text-sm font-medium text-gray-700 flex items-center">
                        <Calendar className="h-4 w-4 mr-2 text-ghana-green" />
                        Dates
                      </Label>
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="font-medium text-gray-900">
                          {new Date(bookingData.selectedDate).toLocaleDateString('en-GB', {
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric'
                          })} – {new Date(new Date(bookingData.selectedDate).getTime() + 2 * 24 * 60 * 60 * 1000).toLocaleDateString('en-GB', {
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric'
                          })}
                        </p>
                      </div>
                    </div>

                    {/* Base Price Section */}
                    <div className="space-y-2">
                      <Label className="text-sm font-medium text-gray-700 flex items-center">
                        <DollarSign className="h-4 w-4 mr-2 text-ghana-green" />
                        Base Price
                      </Label>
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="font-semibold text-lg text-ghana-green">
                          GH₵{bookingData.basePrice.toLocaleString()}
                        </p>
                        <p className="text-sm text-gray-600">per person</p>
                      </div>
                    </div>
                  </div>

                  {/* Travelers Section */}
                  <div className="space-y-3">
                    <Label className="text-sm font-medium text-gray-700 flex items-center">
                      <Users className="h-4 w-4 mr-2 text-ghana-green" />
                      Travelers
                    </Label>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Adults */}
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">Adults</p>
                          <p className="text-sm text-gray-600">Age 18+</p>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleTravelersChange('adults', false)}
                            disabled={bookingData.travelers.adults <= 1}
                          >
                            <Minus className="h-4 w-4" />
                          </Button>
                          <span className="font-semibold w-8 text-center">{bookingData.travelers.adults}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleTravelersChange('adults', true)}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>

                      {/* Children */}
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">Children</p>
                          <p className="text-sm text-gray-600">Age 2-17</p>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleTravelersChange('children', false)}
                            disabled={bookingData.travelers.children <= 0}
                          >
                            <Minus className="h-4 w-4" />
                          </Button>
                          <span className="font-semibold w-8 text-center">{bookingData.travelers.children}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleTravelersChange('children', true)}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Dynamic Add-On Options */}
            <AddOnSelector
              ticketId={parseInt(bookingData.tourId)}
              travelers={bookingData.travelers.adults}
              onSelectionChange={handleAddOnSelectionChange}
            />

            {/* Payment Methods */}
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
                      <div key={method.id} className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value={method.id} id={method.id} />
                        <Label htmlFor={method.id} className="flex-1 cursor-pointer">
                          <div className="flex justify-between items-center">
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

          {/* Summary Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Booking Summary</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowBreakdown(!showBreakdown)}
                  >
                    {showBreakdown ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Tour Details */}
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">{bookingData.tourName}</h3>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>{bookingData.duration}</p>
                    <p>{bookingData.travelers.adults} Adults, {bookingData.travelers.children} Children</p>
                    <p>{new Date(bookingData.selectedDate).toLocaleDateString('en-GB')}</p>
                  </div>
                </div>

                <Separator />

                {/* Price Breakdown */}
                {showBreakdown && (
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-900">Price Breakdown</h4>
                    
                    {/* Base Price */}
                    <div className="flex justify-between text-sm">
                      <span>Base Price ({bookingData.travelers.adults} adults)</span>
                      <span>GH₵{totals.baseTotal.toLocaleString()}</span>
                    </div>

                    {/* Add-ons */}
                    {selectedAddOns.length > 0 && (
                      <>
                        <div className="space-y-1">
                          <p className="text-sm font-medium text-gray-700">Add-ons:</p>
                          {selectedAddOns.map((addon, index) => (
                            <div key={index} className="flex justify-between text-sm text-gray-600">
                              <span className="truncate mr-2">{addon.name}</span>
                              <span>+GH₵{addon.total_price.toLocaleString()}</span>
                            </div>
                          ))}
                        </div>
                      </>
                    )}

                    <Separator />
                  </div>
                )}

                {/* Total */}
                <div className="flex justify-between items-center text-lg font-bold">
                  <span>Total</span>
                  <span className="text-ghana-green">GH₵{totals.total.toLocaleString()}</span>
                </div>

                {/* Proceed Button */}
                <Button 
                  onClick={handleProceedToPayment}
                  disabled={!paymentMethod}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                  size="lg"
                >
                  Proceed to Payment
                </Button>

                {/* Security Notice */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div className="flex items-start space-x-2">
                    <Shield className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-blue-800">
                      <p className="font-medium">Secure Booking</p>
                      <p>Your payment information is encrypted and secure. You can cancel or modify your booking up to 24 hours before the tour date.</p>
                    </div>
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