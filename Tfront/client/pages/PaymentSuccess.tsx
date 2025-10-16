import { useEffect, useState } from "react";
import { useLocation, useNavigate, useSearchParams, Link } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  CheckCircle, Download, Calendar, MapPin, Users, Phone, 
  Mail, Share2, Star, Smartphone, CreditCard, Clock,
  Receipt, Home, MessageCircle
} from "lucide-react";

interface PaymentSuccessData {
  // Tour data
  tourName?: string;
  bookingReference?: string;
  bookingDetails?: any;

  // Ticket data
  eventName?: string;
  artist?: string;
  venue?: string;
  date?: string;
  time?: string;
  ticketType?: string;
  quantity?: number;
  unitPrice?: number;
  ticketReference?: string;
  customerInfo?: any;
  eventDetails?: any;

  // Common fields
  total: number;
  paymentMethod: string;
  paymentDetails: {
    method: string;
    provider?: string;
    phone?: string;
    transactionId: string;
    timestamp: string;
  };
}

export default function PaymentSuccess() {
  console.log('🚀 PaymentSuccess component is being rendered!');
  
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  // Try to get payment data from location state first, then from URL params
  const paymentData = location.state as PaymentSuccessData || (() => {
    const reference = searchParams.get('reference');
    const amount = searchParams.get('amount');
    const method = searchParams.get('method');
    
    if (reference && amount) {
      return {
        total: parseFloat(amount),
        paymentDetails: {
          method: method || 'Unknown',
          transactionId: reference,
          timestamp: new Date().toISOString()
        }
      } as PaymentSuccessData;
    }
    return null;
  })();
  const [isDownloading, setIsDownloading] = useState(false);
  const [enhancedPaymentData, setEnhancedPaymentData] = useState<PaymentSuccessData | null>(null);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);

  // Debug: Log the payment data to see what we're receiving
  useEffect(() => {
    console.log('🎉 PaymentSuccess component mounted!');
    console.log('PaymentSuccess - Location:', location);
    console.log('PaymentSuccess - Search params:', Object.fromEntries(searchParams.entries()));
    console.log('PaymentSuccess - Received payment data:', paymentData);
    if (paymentData?.bookingDetails) {
      console.log('PaymentSuccess - Booking details:', paymentData.bookingDetails);
    }
    // Also check for nested booking details in different locations
    if (paymentData?.booking_details) {
      console.log('PaymentSuccess - booking_details (snake_case):', paymentData.booking_details);
    }
  }, [paymentData]);

  // Fetch complete payment details if booking details are missing
  useEffect(() => {
    const fetchCompletePaymentData = async () => {
      // Check if we have booking details, if not, try to fetch from backend
      const hasBookingDetails = getBookingDetails() !== null;
      
      if (!hasBookingDetails && paymentData?.paymentDetails?.transactionId) {
        console.log('PaymentSuccess - Booking details missing, fetching from backend...');
        setIsLoadingDetails(true);
        
        try {
          const token = localStorage.getItem('auth_token');
          if (!token) {
            console.error('PaymentSuccess - No auth token found');
            return;
          }
          
          const response = await fetch(
            `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/payment/${paymentData.paymentDetails.transactionId}/`,
            {
              headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
              }
            }
          );
          
          if (response.ok) {
            const completeData = await response.json();
            console.log('PaymentSuccess - Fetched complete payment data:', completeData);
            
            // Merge the fetched data with existing payment data
            const mergedData = {
              ...paymentData,
              ...completeData,
              // Preserve any existing payment details
              paymentDetails: {
                ...completeData.paymentDetails,
                ...paymentData.paymentDetails
              }
            };
            
            setEnhancedPaymentData(mergedData);
          } else {
            console.error('PaymentSuccess - Failed to fetch payment details:', response.status);
          }
        } catch (error) {
          console.error('PaymentSuccess - Error fetching payment details:', error);
        } finally {
          setIsLoadingDetails(false);
        }
      }
    };
    
    if (paymentData) {
      fetchCompletePaymentData();
    }
  }, [paymentData]);

  // Helper function to get booking details from various possible locations
  const getBookingDetails = () => {
    // Use enhanced data if available, otherwise fall back to original
    const dataSource = enhancedPaymentData || paymentData;
    
    // Try different possible locations for booking details
    return dataSource?.bookingDetails || 
           dataSource?.booking_details || 
           dataSource?.bookingData ||
           null;
  };

  // Helper function to get tour/event name
  const getEventName = () => {
    const dataSource = enhancedPaymentData || paymentData;
    const bookingDetails = getBookingDetails();
    
    return dataSource?.eventName || 
           dataSource?.tourName || 
           bookingDetails?.bookingData?.tourName ||
           bookingDetails?.tourName ||
           'Booking';
  };

  // Helper function to get travelers info
  const getTravelersInfo = () => {
    const bookingDetails = getBookingDetails();
    const travelers = bookingDetails?.bookingData?.travelers;
    
    if (!travelers) return null;
    
    let info = `${travelers.adults} Adult${travelers.adults > 1 ? 's' : ''}`;
    if (travelers.children > 0) {
      info += `, ${travelers.children} Child${travelers.children > 1 ? 'ren' : ''}`;
    }
    return info;
  };

  // Helper function to get current data source
  const getCurrentPaymentData = () => {
    return enhancedPaymentData || paymentData;
  };

  useEffect(() => {
    console.log('PaymentSuccess mounted with data:', paymentData);
    
    if (!paymentData) {
      console.log('No payment data found, checking localStorage and URL params...');
      
      // Try to get payment data from localStorage as backup
      const storedPaymentData = localStorage.getItem('completedPaymentData');
      if (storedPaymentData) {
        try {
          const parsedData = JSON.parse(storedPaymentData);
          console.log('Found payment data in localStorage:', parsedData);
          
          // Set the payment data and don't redirect
          setEnhancedPaymentData(parsedData);
          localStorage.removeItem('completedPaymentData'); // Clean up
          return;
        } catch (e) {
          console.error('Error parsing stored payment data:', e);
        }
      }
      
      // Check URL parameters as final fallback
      const reference = searchParams.get('reference');
      const amount = searchParams.get('amount');
      
      if (reference && amount) {
        console.log('Found payment info in URL params, creating minimal success data');
        const minimalPaymentData = {
          total: parseFloat(amount),
          paymentDetails: {
            method: searchParams.get('method') || 'Payment',
            transactionId: reference,
            timestamp: new Date().toISOString(),
            status: 'completed'
          },
          tourName: 'Booking Completed',
          bookingReference: reference
        };
        
        setEnhancedPaymentData(minimalPaymentData);
        return;
      }
      
      console.log('No payment data available anywhere, showing success message and redirecting');
      // Show a generic success message for 3 seconds, then redirect
      setTimeout(() => {
        navigate('/tickets', { 
          state: { 
            message: 'Payment completed successfully! Check your email for confirmation.' 
          } 
        });
      }, 3000);
      return;
    }
  }, [paymentData, navigate, searchParams]);

  const generateBookingReference = () => {
    return `GH${Date.now().toString().slice(-6)}`;
  };

  const currentData = getCurrentPaymentData();
  const bookingRef = currentData?.ticketReference || currentData?.bookingReference || generateBookingReference();
  const isTicket = !!currentData?.eventName;

  const handleDownloadReceipt = async () => {
    setIsDownloading(true);
    // Simulate download
    setTimeout(() => {
      setIsDownloading(false);
      // In real app, this would generate and download a PDF
      alert('Receipt downloaded successfully!');
    }, 2000);
  };

  const handleShare = () => {
    const currentData = getCurrentPaymentData();
    const isTicket = !!currentData?.eventName;
    const title = isTicket ? 'Tales and Trails Ghana - Event Ticket Confirmation' : 'Tales and Trails Ghana - Booking Confirmation';
    const text = isTicket
      ? `I just got tickets for ${currentData?.eventName} by ${currentData?.artist}! Ticket reference: ${bookingRef}`
      : `I just booked an amazing tour: ${getEventName()}. Booking reference: ${bookingRef}`;

    if (navigator.share) {
      navigator.share({
        title,
        text,
        url: window.location.href,
      });
    } else {
      // Fallback for browsers that don't support Web Share API
      navigator.clipboard.writeText(text);
      alert(isTicket ? 'Ticket details copied to clipboard!' : 'Booking details copied to clipboard!');
    }
  };

  // Show a generic success page if no payment data is available
  if (!paymentData && !enhancedPaymentData) {
    return (
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 flex items-center justify-center">
          <div className="max-w-md mx-auto text-center p-8">
            <div className="w-20 h-20 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="h-12 w-12 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-green-900 mb-4">Payment Successful!</h1>
            <p className="text-green-700 mb-6">
              Your payment has been processed successfully. You should receive a confirmation email shortly.
            </p>
            <div className="space-y-3">
              <Button 
                onClick={() => navigate('/dashboard')} 
                className="w-full bg-ghana-green hover:bg-ghana-green/90"
              >
                View My Bookings
              </Button>
              <Button 
                variant="outline"
                onClick={() => navigate('/tickets')} 
                className="w-full"
              >
                Browse More Events
              </Button>
            </div>
            <p className="text-sm text-gray-600 mt-4">
              If you don't receive a confirmation email within 10 minutes, please contact support.
            </p>
          </div>
        </div>
      </Layout>
    );
  }

  // Show loading state while fetching enhanced data
  if (isLoadingDetails) {
    return (
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ghana-green mx-auto mb-4"></div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Loading Booking Details...</h2>
            <p className="text-gray-600">Please wait while we fetch your complete booking information.</p>
          </div>
        </div>
      </Layout>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Layout>
      {/* Success Header */}
      <div className="bg-gradient-to-r from-green-600 to-ghana-green text-white py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center">
              <CheckCircle className="h-12 w-12 text-green-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold mb-4">Payment Successful!</h1>
          <p className="text-xl text-green-100 mb-2">
            Your {isTicket ? 'tickets have' : 'booking has'} been confirmed
          </p>
          <p className="text-green-200">
            {isTicket ? 'Ticket' : 'Booking'} Reference: <span className="font-bold">{bookingRef}</span>
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Booking Details */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-ghana-green" />
                  <span>{isTicket ? 'Ticket Details' : 'Booking Details'}</span>
                </CardTitle>
                <CardDescription>
                  Your {isTicket ? 'event ticket information' : 'tour booking information'}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {getEventName()}
                    </h3>
                    {isTicket && paymentData.artist && (
                      <p className="text-gray-600 mb-2 font-medium">{paymentData.artist}</p>
                    )}
                    
                    {/* Enhanced Booking Details */}
                    <div className="space-y-3 text-sm">
                      {isTicket ? (
                        // Event Details
                        <>
                          <div className="flex items-center space-x-2 text-gray-600">
                            <Calendar className="h-4 w-4" />
                            <span>
                              {new Date(paymentData.date!).toLocaleDateString('en-GB', {
                                weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
                              })}
                            </span>
                          </div>
                          {paymentData.time && (
                            <div className="flex items-center space-x-2 text-gray-600">
                              <Clock className="h-4 w-4" />
                              <span>{paymentData.time}</span>
                            </div>
                          )}
                          {paymentData.venue && (
                            <div className="flex items-center space-x-2 text-gray-600">
                              <MapPin className="h-4 w-4" />
                              <span>{paymentData.venue}</span>
                            </div>
                          )}
                          <div className="flex items-center space-x-2 text-gray-600">
                            <Users className="h-4 w-4" />
                            <span>{paymentData.quantity} × {paymentData.ticketType || 'Ticket'}</span>
                          </div>
                        </>
                      ) : (
                        // Tour Details
                        <>
                          {(() => {
                            const bookingDetails = getBookingDetails();
                            const selectedDate = bookingDetails?.bookingData?.selectedDate;
                            const duration = bookingDetails?.bookingData?.duration;
                            const travelersInfo = getTravelersInfo();
                            
                            return (
                              <>
                                {selectedDate && (
                                  <div className="flex items-center space-x-2 text-gray-600">
                                    <Calendar className="h-4 w-4" />
                                    <span>
                                      {new Date(selectedDate).toLocaleDateString('en-GB', {
                                        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
                                      })}
                                    </span>
                                  </div>
                                )}
                                
                                {duration && (
                                  <div className="flex items-center space-x-2 text-gray-600">
                                    <Clock className="h-4 w-4" />
                                    <span>{duration}</span>
                                  </div>
                                )}
                                
                                {travelersInfo && (
                                  <div className="flex items-center space-x-2 text-gray-600">
                                    <Users className="h-4 w-4" />
                                    <span>{travelersInfo}</span>
                                  </div>
                                )}
                              </>
                            );
                          })()}
                          
                          <div className="flex items-center space-x-2 text-gray-600">
                            <MapPin className="h-4 w-4" />
                            <span>Ghana</span>
                          </div>
                        </>
                      )}
                      
                      {/* Booking/Ticket Reference */}
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-gray-500 uppercase tracking-wide">
                            {isTicket ? 'Ticket Reference' : 'Booking Reference'}
                          </span>
                          <span className="font-mono text-sm font-medium">
                            {isTicket ? paymentData.ticketReference : paymentData.bookingReference}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <Badge className="bg-green-100 text-green-800 ml-4">
                    Confirmed
                  </Badge>
                </div>

                <Separator />

                {/* Booking Options & Add-ons */}
                {(() => {
                  const bookingDetails = getBookingDetails();
                  return !isTicket && bookingDetails && (
                    <>
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3">📋 Booking Summary</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {/* Selected Options */}
                          {bookingDetails.selectedOptions && (
                            <div className="space-y-2">
                              <h5 className="font-medium text-gray-700 text-sm">Selected Options</h5>
                              <div className="space-y-1 text-sm">
                                {bookingDetails.selectedOptions.accommodation && (
                                  <div className="flex justify-between">
                                    <span className="text-gray-600">Accommodation:</span>
                                    <span className="capitalize font-medium">{bookingDetails.selectedOptions.accommodation}</span>
                                  </div>
                                )}
                                {bookingDetails.selectedOptions.transport && (
                                  <div className="flex justify-between">
                                    <span className="text-gray-600">Transport:</span>
                                    <span className="capitalize font-medium">{bookingDetails.selectedOptions.transport}</span>
                                  </div>
                                )}
                                {bookingDetails.selectedOptions.meals && (
                                  <div className="flex justify-between">
                                    <span className="text-gray-600">Meals:</span>
                                    <span className="capitalize font-medium">{bookingDetails.selectedOptions.meals}</span>
                                  </div>
                                )}
                                {bookingDetails.selectedOptions.medical && (
                                  <div className="flex justify-between">
                                    <span className="text-gray-600">Medical Support:</span>
                                    <span className="capitalize font-medium">{bookingDetails.selectedOptions.medical}</span>
                                  </div>
                                )}
                              </div>
                            </div>
                          )}

                          {/* Add-ons */}
                          {bookingDetails.addOns && bookingDetails.addOns.length > 0 && (
                            <div className="space-y-2">
                              <h5 className="font-medium text-gray-700 text-sm">Add-ons & Extras</h5>
                              <div className="space-y-1 text-sm">
                                {bookingDetails.addOns.map((addon: any, index: number) => (
                                  <div key={index} className="flex justify-between">
                                    <span className="text-gray-600">{addon.name}</span>
                                    <span className="font-medium">GH¢{addon.price}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                      <Separator />
                    </>
                  );
                })()}

                {/* What's Next */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">What happens next?</h4>
                  <div className="space-y-3">
                    {isTicket ? (
                      <>
                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">1</span>
                          </div>
                          <div>
                            <p className="font-medium">Digital Tickets Sent</p>
                            <p className="text-sm text-gray-600">Your e-tickets will be sent to {paymentData.customerInfo?.email || 'your email'} within 5 minutes. You can also download them from your dashboard.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">2</span>
                          </div>
                          <div>
                            <p className="font-medium">Event Reminder</p>
                            <p className="text-sm text-gray-600">We'll send you a reminder 24 hours before the event with venue details and entry instructions.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">3</span>
                          </div>
                          <div>
                            <p className="font-medium">Enjoy the Event</p>
                            <p className="text-sm text-gray-600">Show your ticket (digital or printed) at the venue entrance and enjoy an amazing {paymentData.eventDetails?.category?.toLowerCase() || 'event'}!</p>
                          </div>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">1</span>
                          </div>
                          <div>
                            <p className="font-medium">Confirmation Email</p>
                            <p className="text-sm text-gray-600">You'll receive a detailed email with your booking confirmation and tour itinerary within 5 minutes.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">2</span>
                          </div>
                          <div>
                            <p className="font-medium">Pre-Tour Contact</p>
                            <p className="text-sm text-gray-600">Our team will contact you 48 hours before your tour with final details and meeting instructions.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">3</span>
                          </div>
                          <div>
                            <p className="font-medium">Enjoy Your Tour</p>
                            <p className="text-sm text-gray-600">Meet your guide at the specified location and enjoy your amazing Ghana experience!</p>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                </div>

                {/* Contact Information */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-3">Need Help?</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <Phone className="h-4 w-4 text-ghana-green" />
                      <span>+233 24 122 7481</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Mail className="h-4 w-4 text-ghana-green" />
                      <span>Talesandtrailsghana@gmail.com</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Payment Receipt */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Receipt className="h-5 w-5 text-ghana-green" />
                  <span>Payment Receipt</span>
                </CardTitle>
                <CardDescription>Transaction details and receipt</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-600">Transaction ID</p>
                      <p className="font-mono text-sm font-medium">{paymentData.paymentDetails?.transactionId || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Payment Method</p>
                      <div className="flex items-center space-x-2">
                        {paymentData.paymentDetails?.method === 'Mobile Money' ? (
                          <Smartphone className="h-4 w-4 text-ghana-green" />
                        ) : (
                          <CreditCard className="h-4 w-4 text-ghana-green" />
                        )}
                        <span className="font-medium">{paymentData.paymentDetails?.method || 'N/A'}</span>
                        {paymentData.paymentDetails?.provider && (
                          <Badge variant="outline" className="text-xs">
                            {paymentData.paymentDetails.provider}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    {/* Price Breakdown */}
                    <div>
                      <p className="text-sm text-gray-600 mb-2">Price Breakdown</p>
                      <div className="space-y-1 text-sm">
                        {(() => {
                          const bookingDetails = getBookingDetails();
                          if (!isTicket && bookingDetails?.bookingData) {
                            // Tour price breakdown
                            return (
                              <>
                                <div className="flex justify-between">
                                  <span className="text-gray-600">
                                    Base Price × {bookingDetails.bookingData.travelers?.adults || 1} traveler{(bookingDetails.bookingData.travelers?.adults || 1) > 1 ? 's' : ''}
                                  </span>
                                  <span>GH¢{((bookingDetails.bookingData.basePrice || 0) * (bookingDetails.bookingData.travelers?.adults || 1)).toLocaleString()}</span>
                                </div>
                                {bookingDetails.bookingData.travelers?.children > 0 && (
                                  <div className="flex justify-between">
                                    <span className="text-gray-600">
                                      Children × {bookingDetails.bookingData.travelers.children}
                                    </span>
                                    <span>GH¢{((bookingDetails.bookingData.basePrice || 0) * 0.5 * bookingDetails.bookingData.travelers.children).toLocaleString()}</span>
                                  </div>
                                )}
                                {bookingDetails.addOns?.map((addon: any, index: number) => (
                                  <div key={index} className="flex justify-between">
                                    <span className="text-gray-600">{addon.name}</span>
                                    <span>GH¢{addon.price}</span>
                                  </div>
                                ))}
                              </>
                            );
                          } else if (isTicket) {
                            // Ticket price breakdown
                            return (
                              <div className="flex justify-between">
                                <span className="text-gray-600">
                                  {paymentData.quantity || 1} × {paymentData.ticketType || 'Ticket'}
                                </span>
                                <span>GH¢{paymentData.total?.toLocaleString() || '0'}</span>
                              </div>
                            );
                          } else {
                            return (
                              <div className="flex justify-between">
                                <span className="text-gray-600">Total Amount</span>
                                <span>GH¢{paymentData.total?.toLocaleString() || '0'}</span>
                              </div>
                            );
                          }
                        })()}
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm text-gray-600">Total Amount Paid</p>
                      <p className="text-xl font-bold text-ghana-green">GH¢{paymentData.total?.toLocaleString() || '0'}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-gray-600">Payment Date</p>
                      <div className="flex items-center space-x-2">
                        <Clock className="h-4 w-4 text-gray-400" />
                        <span className="font-medium">{paymentData.paymentDetails?.timestamp ? formatDate(paymentData.paymentDetails.timestamp) : 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <Separator />

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Status</span>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="font-medium text-green-600">Payment Successful</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Action Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  onClick={handleDownloadReceipt}
                  disabled={isDownloading}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90"
                >
                  <Download className="h-4 w-4 mr-2" />
                  {isDownloading ? 'Downloading...' : 'Download Receipt'}
                </Button>
                
                <Button 
                  onClick={handleShare}
                  variant="outline"
                  className="w-full"
                >
                  <Share2 className="h-4 w-4 mr-2" />
                  Share Booking
                </Button>
                
                <Button 
                  asChild
                  variant="outline"
                  className="w-full"
                >
                  <Link to="/dashboard">
                    <Home className="h-4 w-4 mr-2" />
                    View Dashboard
                  </Link>
                </Button>
              </CardContent>
            </Card>

            {/* Important Notes */}
            <Card>
              <CardHeader>
                <CardTitle>Important Notes</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Free cancellation up to 24 hours before tour</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Please arrive 15 minutes before departure time</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Bring valid ID and comfortable walking shoes</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Weather updates will be provided if needed</p>
                </div>
              </CardContent>
            </Card>

            {/* Feedback */}
            <Card>
              <CardHeader>
                <CardTitle>Rate Your Experience</CardTitle>
                <CardDescription>Help us improve our service</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center space-x-1 mb-4">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      className="p-1 hover:scale-110 transition-transform"
                    >
                      <Star className="h-6 w-6 text-yellow-400 fill-current" />
                    </button>
                  ))}
                </div>
                <Button variant="outline" className="w-full">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Leave Feedback
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Related Tours */}
        <div className="mt-12">
          <Card>
            <CardHeader>
              <CardTitle>More Amazing Tours</CardTitle>
              <CardDescription>Discover other incredible destinations in Ghana</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="group cursor-pointer">
                  <div className="relative overflow-hidden rounded-lg mb-3">
                    <img 
                      src="https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=400"
                      alt="Aburi Gardens"
                      className="w-full h-32 object-cover group-hover:scale-105 transition-transform"
                    />
                    <Badge className="absolute top-2 left-2 bg-ghana-gold text-black">
                      Nature
                    </Badge>
                  </div>
                  <h4 className="font-medium group-hover:text-ghana-green">Aburi Gardens Nature Escape</h4>
                  <p className="text-sm text-gray-600">From GH₵280</p>
                </div>
                
                <div className="group cursor-pointer">
                  <div className="relative overflow-hidden rounded-lg mb-3">
                    <img 
                      src="https://images.pexels.com/photos/1054655/pexels-photo-1054655.jpeg?auto=compress&cs=tinysrgb&w=400"
                      alt="Mole National Park"
                      className="w-full h-32 object-cover group-hover:scale-105 transition-transform"
                    />
                    <Badge className="absolute top-2 left-2 bg-ghana-gold text-black">
                      Safari
                    </Badge>
                  </div>
                  <h4 className="font-medium group-hover:text-ghana-green">Mole National Park Safari</h4>
                  <p className="text-sm text-gray-600">From GH₵1,200</p>
                </div>
                
                <div className="group cursor-pointer">
                  <div className="relative overflow-hidden rounded-lg mb-3">
                    <img 
                      src="https://images.pexels.com/photos/5273081/pexels-photo-5273081.jpeg?auto=compress&cs=tinysrgb&w=400"
                      alt="Elmina Castle"
                      className="w-full h-32 object-cover group-hover:scale-105 transition-transform"
                    />
                    <Badge className="absolute top-2 left-2 bg-ghana-gold text-black">
                      Heritage
                    </Badge>
                  </div>
                  <h4 className="font-medium group-hover:text-ghana-green">Elmina Castle Tour</h4>
                  <p className="text-sm text-gray-600">From GH₵400</p>
                </div>
              </div>
              
              <div className="text-center mt-6">
                <Button asChild variant="outline">
                  <Link to="/destinations">
                    View All Tours
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
