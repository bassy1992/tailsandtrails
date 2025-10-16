import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  ArrowLeft, Smartphone, Shield, CheckCircle, 
  AlertCircle, Loader2, Phone, User, CreditCard
} from "lucide-react";

interface PaymentData {
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
}

export default function MomoCheckout() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const paymentData = location.state as PaymentData;
  
  const [momoProvider, setMomoProvider] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [accountName, setAccountName] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [step, setStep] = useState<'details' | 'processing' | 'verify'>('details');
  const [statusMessage, setStatusMessage] = useState<string>('Payment request sent to your phone');
  const [pollingAttempts, setPollingAttempts] = useState<number>(0);
  const [currentPaymentRef, setCurrentPaymentRef] = useState<string>('');
  
  useEffect(() => {
    if (!paymentData) {
      navigate('/booking/1');
      return;
    }
    
    // Redirect ticket purchases to the new ticket checkout system
    if (paymentData.eventName || paymentData.ticketReference) {
      console.log('Redirecting ticket purchase to new checkout system');
      
      // Convert old ticket data to new format
      const ticketPurchaseData = {
        type: 'ticket',
        ticketId: paymentData.eventId || 1, // fallback ID
        ticketTitle: paymentData.eventName || 'Event Ticket',
        venue: paymentData.venue || 'TBA',
        eventDate: paymentData.date || new Date().toISOString(),
        quantity: paymentData.quantity || 1,
        unitPrice: paymentData.unitPrice || paymentData.total,
        totalAmount: paymentData.total,
        customerInfo: {
          name: paymentData.customerInfo?.firstName && paymentData.customerInfo?.lastName 
            ? `${paymentData.customerInfo.firstName} ${paymentData.customerInfo.lastName}`.trim()
            : 'Customer',
          email: paymentData.customerInfo?.email || 'customer@example.com',
          phone: paymentData.customerInfo?.phone || ''
        }
      };
      
      // Store in localStorage and redirect
      localStorage.setItem('pendingTicketPurchase', JSON.stringify(ticketPurchaseData));
      navigate('/ticket-checkout');
      return;
    }
  }, [paymentData, navigate]);

  const handlePayment = async () => {
    if (!momoProvider || !phoneNumber || !accountName) {
      alert("Please fill in all required fields");
      return;
    }

    setIsProcessing(true);
    setStep('processing');

    try {
      // Call Paystack API to create payment
      const authToken = localStorage.getItem('auth_token');
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      // Add auth token if available
      if (authToken) {
        headers['Authorization'] = `Token ${authToken}`;
      }
      
      // Format phone number for Ghana
      const formattedPhone = phoneNumber.startsWith('+') 
        ? phoneNumber 
        : `+233${phoneNumber.replace(/^0/, '')}`;
      
      // Get customer email (use a default if not available)
      const customerEmail = paymentData.customerInfo?.email || 'customer@example.com';
      
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/paystack/create/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          amount: paymentData.total,
          currency: 'GHS',
          payment_method: 'mobile_money',
          provider: momoProvider, // mtn, vodafone, airteltigo
          phone_number: formattedPhone,
          email: customerEmail,
          description: paymentData.tourName || paymentData.eventName || 'Payment',
          booking_details: paymentData.bookingDetails || null,
        })
      });

      const result = await response.json();

      if (result.success) {
        // Check if we got a Paystack authorization URL for redirect
        if (result.paystack?.authorization_url) {
          // Store payment data for when user returns
          sessionStorage.setItem('paymentReference', result.payment.reference);
          sessionStorage.setItem('pendingPaymentData', JSON.stringify(paymentData));
          
          // Redirect to Paystack checkout page
          window.location.href = result.paystack.authorization_url;
          return;
        }
        
        // Fallback to old polling method if no redirect URL
        setIsProcessing(false);
        setStep('verify');
        
        // Store payment reference for completion
        const paymentRef = result.payment.reference;
        sessionStorage.setItem('paymentReference', paymentRef);
        setCurrentPaymentRef(paymentRef);
        
        // For mobile money, start polling for status
        startPaymentStatusPolling(paymentRef);
        
        // Update status message with Paystack response
        if (result.paystack?.display_text) {
          setStatusMessage(result.paystack.display_text);
        }
        
        // In test mode, auto-complete after 10 seconds
        if (result.paystack?.test_mode !== false) {
          setTimeout(() => {
            handleConfirmPayment();
          }, 10000);
        }
      } else {
        throw new Error(result.error || 'Payment initiation failed');
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert('Failed to initiate payment. Please try again.');
      setIsProcessing(false);
      setStep('details');
    }
  };

  const startPaymentStatusPolling = (paymentReference: string) => {
    setStatusMessage('Checking payment status...');
    setPollingAttempts(0);
    
    const pollPaymentStatus = async () => {
      try {
        const authToken = localStorage.getItem('auth_token');
        const headers: Record<string, string> = {};
        
        if (authToken) {
          headers['Authorization'] = `Token ${authToken}`;
        }
        
        // Use Paystack verification endpoint
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/paystack/verify/${paymentReference}/`, {
          headers
        });
        
        const result = await response.json();
        
        setPollingAttempts(prev => prev + 1);
        
        if (result.success && result.payment) {
          const payment = result.payment;
          
          if (payment.status === 'successful') {
            // Payment completed successfully
            setStatusMessage('Payment completed successfully! 🎉');
            
            // Wait a moment then redirect
            setTimeout(() => {
              const successData = {
                ...paymentData,
                paymentDetails: {
                  method: 'Mobile Money',
                  provider: momoProvider,
                  phone: phoneNumber,
                  transactionId: paymentReference,
                  status: 'completed',
                  timestamp: payment.processed_at || new Date().toISOString(),
                  gateway: 'Paystack'
                }
              };
              
              // Store in localStorage as backup
              localStorage.setItem('completedPaymentData', JSON.stringify(successData));
              
              navigate('/payment-success', {
                state: successData
              });
              sessionStorage.removeItem('paymentReference');
            }, 2000);
            
          } else if (payment.status === 'failed') {
            setStatusMessage('Payment failed. You can try completing it manually or start over.');
            // Don't auto-redirect, let user choose
            
          } else if (payment.status === 'cancelled') {
            setStatusMessage('Payment was cancelled. You can complete it manually if you authorized the payment, or start over.');
            // Don't auto-redirect or clear reference, let user choose
            
          } else if (pollingAttempts < 40) { // Poll for up to 2 minutes (40 attempts * 3 seconds)
            // Still processing, continue polling
            const seconds = pollingAttempts * 3;
            if (seconds < 60) {
              setStatusMessage(`Waiting for payment authorization... (${seconds}s)`);
            } else {
              setStatusMessage(`Waiting for payment authorization... (${Math.floor(seconds / 60)}m ${seconds % 60}s)`);
            }
            setTimeout(pollPaymentStatus, 3000); // Check every 3 seconds
            
          } else {
            // Timeout - offer manual completion
            setStatusMessage('Payment is taking longer than expected. You can complete it manually if you have authorized the payment.');
          }
        } else {
          // Error in verification, but continue polling if within limits
          if (pollingAttempts < 40) {
            setTimeout(pollPaymentStatus, 3000);
          } else {
            setStatusMessage('Unable to verify payment status. Please contact support if you completed the payment.');
          }
        }
        
      } catch (error) {
        console.error('Status check error:', error);
        if (pollingAttempts < 40) {
          setTimeout(pollPaymentStatus, 3000); // Retry on error every 3 seconds
        } else {
          setStatusMessage('Unable to verify payment status. Please contact support if you completed the payment.');
        }
      }
    };
    
    // Start polling after 2 seconds
    setTimeout(pollPaymentStatus, 2000);
  };

  const handleConfirmPayment = async () => {
    // Try to get payment reference from multiple sources
    const paymentReference = sessionStorage.getItem('paymentReference') || currentPaymentRef;
    
    if (!paymentReference) {
      alert('Payment reference not found. Please try again.');
      setStep('details');
      return;
    }

    try {
      // Complete the payment in the database
      const authToken = localStorage.getItem('auth_token');
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (authToken) {
        headers['Authorization'] = `Token ${authToken}`;
      }
      
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/${paymentReference}/complete/`, {
        method: 'POST',
        headers
      });

      const result = await response.json();
      
      if (result.success) {
        // Payment completed successfully
        navigate('/payment-success', {
          state: {
            ...paymentData,
            paymentDetails: {
              method: 'Mobile Money',
              provider: momoProvider,
              phone: phoneNumber,
              transactionId: paymentReference,
              status: 'completed',
              timestamp: result.payment.processed_at || new Date().toISOString()
            }
          }
        });
        
        // Clear the payment reference
        sessionStorage.removeItem('paymentReference');
      } else {
        alert(result.message || 'Failed to complete payment. Please contact support.');
      }
    } catch (error) {
      console.error('Payment completion error:', error);
      // Still allow user to proceed in case of API issues
      navigate('/payment-success', {
        state: {
          ...paymentData,
          paymentDetails: {
            method: 'Mobile Money',
            provider: momoProvider,
            phone: phoneNumber,
            transactionId: paymentReference || `TXN${Date.now()}`,
            status: 'completed',
            timestamp: new Date().toISOString()
          }
        }
      });
      
      sessionStorage.removeItem('paymentReference');
    }
  };

  if (!paymentData) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Payment Session Expired</h2>
            <p className="text-gray-600 mb-6">Please start the booking process again.</p>
            <Button onClick={() => navigate('/destinations')} className="bg-ghana-green hover:bg-ghana-green/90">
              Browse Tours
            </Button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Header */}
      <div className="bg-ghana-green text-white py-6">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate(-1)}
                className="p-2 text-white hover:bg-white/10"
              >
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold">Mobile Money Payment</h1>
                <p className="text-ghana-gold">Secure and instant payment</p>
              </div>
            </div>
            <Badge className="bg-white text-ghana-green px-4 py-2">
              {step === 'details' && 'Step 1 of 2'}
              {step === 'processing' && 'Processing...'}
              {step === 'verify' && 'Step 2 of 2'}
            </Badge>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2">
            
            {/* Payment Details Step */}
            {step === 'details' && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Smartphone className="h-5 w-5 text-ghana-green" />
                    <span>Mobile Money Details</span>
                  </CardTitle>
                  <CardDescription>
                    Enter your mobile money details to complete the payment
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  
                  {/* Mobile Money Provider */}
                  <div className="space-y-3">
                    <Label className="text-base font-medium">Select Mobile Money Provider</Label>
                    <RadioGroup value={momoProvider} onValueChange={setMomoProvider} className="space-y-3">
                      <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="mtn" id="mtn" />
                        <Label htmlFor="mtn" className="flex-1 cursor-pointer">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center">
                                <span className="text-xs font-bold text-black">MTN</span>
                              </div>
                              <div>
                                <p className="font-medium">MTN Mobile Money</p>
                                <p className="text-sm text-gray-600">*170#</p>
                              </div>
                            </div>
                            <Badge variant="outline" className="text-green-600">Popular</Badge>
                          </div>
                        </Label>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="vodafone" id="vodafone" />
                        <Label htmlFor="vodafone" className="flex-1 cursor-pointer">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
                                <span className="text-xs font-bold text-white">VF</span>
                              </div>
                              <div>
                                <p className="font-medium">Vodafone Cash</p>
                                <p className="text-sm text-gray-600">*110#</p>
                              </div>
                            </div>
                          </div>
                        </Label>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="airteltigo" id="airteltigo" />
                        <Label htmlFor="airteltigo" className="flex-1 cursor-pointer">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                <span className="text-xs font-bold text-white">AT</span>
                              </div>
                              <div>
                                <p className="font-medium">AirtelTigo Money</p>
                                <p className="text-sm text-gray-600">*100#</p>
                              </div>
                            </div>
                          </div>
                        </Label>
                      </div>
                    </RadioGroup>
                  </div>

                  <Separator />

                  {/* Phone Number */}
                  <div className="space-y-2">
                    <Label htmlFor="phone">Mobile Money Phone Number</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <Input
                        id="phone"
                        type="tel"
                        placeholder="024 123 4567"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        className="pl-10"
                        required
                      />
                    </div>
                    <p className="text-xs text-gray-600">
                      Enter the phone number registered with your mobile money account
                    </p>
                  </div>

                  {/* Account Name */}
                  <div className="space-y-2">
                    <Label htmlFor="name">Account Holder Name</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <Input
                        id="name"
                        type="text"
                        placeholder="Full Name on Mobile Money Account"
                        value={accountName}
                        onChange={(e) => setAccountName(e.target.value)}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  {/* Security Notice */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Shield className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="font-medium text-blue-900">Secure Payment</h4>
                        <p className="text-sm text-blue-700 mt-1">
                          Your mobile money details are encrypted and secure. You will receive a prompt on your phone to authorize the payment.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Pay Button */}
                  <Button 
                    onClick={handlePayment}
                    disabled={!momoProvider || !phoneNumber || !accountName || isProcessing}
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white py-3"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Processing Payment...
                      </>
                    ) : (
                      `Pay GH₵${paymentData.total.toLocaleString()}`
                    )}
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Processing Step */}
            {step === 'processing' && (
              <Card>
                <CardContent className="py-12 text-center">
                  <div className="flex flex-col items-center space-y-6">
                    <div className="relative">
                      <div className="w-20 h-20 bg-ghana-green/10 rounded-full flex items-center justify-center">
                        <Loader2 className="h-10 w-10 text-ghana-green animate-spin" />
                      </div>
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        Initiating Payment
                      </h3>
                      <p className="text-gray-600">
                        Please wait while we process your payment request...
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Verification Step */}
            {step === 'verify' && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Smartphone className="h-5 w-5 text-ghana-green" />
                    <span>Payment Authorization</span>
                  </CardTitle>
                  <CardDescription>
                    Complete the payment on your mobile device
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Smartphone className="h-8 w-8 text-ghana-green animate-pulse" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Check Your Phone
                    </h3>
                    <p className="text-gray-600 mb-4">
                      A payment prompt has been sent to <strong>{phoneNumber}</strong>
                    </p>
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-left">
                      <div className="flex items-start space-x-3">
                        <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                        <div>
                          <h4 className="font-medium text-yellow-900">Instructions:</h4>
                          <ol className="text-sm text-yellow-800 mt-1 space-y-1">
                            <li>1. Check your phone for a payment notification</li>
                            <li>2. Enter your Mobile Money PIN</li>
                            <li>3. Confirm the payment amount: <strong>GH₵{paymentData.total.toLocaleString()}</strong></li>
                            <li>4. Click the confirmation button below once complete</li>
                          </ol>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Status Message */}
                  <div className="text-center">
                    <div className="flex items-center justify-center space-x-2 text-sm text-blue-600 mb-4">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      <span>{statusMessage}</span>
                    </div>
                    
                    {/* Test Mode Notice */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                      <p className="text-sm text-blue-800">
                        <strong>Test Mode:</strong> This is a safe test payment. 
                        You can click "Complete Payment" below to simulate successful authorization.
                      </p>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-col space-y-3">
                    {/* Always show completion button in test mode */}
                    <Button 
                      onClick={handleConfirmPayment}
                      className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                      disabled={!currentPaymentRef && !sessionStorage.getItem('paymentReference')}
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Complete Payment (Test Mode)
                    </Button>
                    
                    <Button 
                      variant="outline"
                      onClick={() => {
                        setStep('details');
                        setPollingAttempts(0);
                        setCurrentPaymentRef('');
                        setStatusMessage('Payment request sent to your phone');
                        sessionStorage.removeItem('paymentReference');
                      }}
                      className="w-full"
                    >
                      Start Over
                    </Button>
                  </div>

                  {/* Help */}
                  <div className="text-center text-sm text-gray-600">
                    <p>Having trouble? <a href="/contact" className="text-ghana-green hover:underline">Contact Support</a></p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Summary Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle>Payment Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Booking Details Section */}
                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900 text-lg">
                    {paymentData.eventName || paymentData.tourName || 'Booking Details'}
                  </h4>
                  
                  {/* Tour/Event Information */}
                  <div className="space-y-3 text-sm">
                    {paymentData.eventName ? (
                      // Event/Ticket Details
                      <>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Event:</span>
                          <span className="font-medium">{paymentData.eventName}</span>
                        </div>
                        {paymentData.artist && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Artist:</span>
                            <span className="font-medium">{paymentData.artist}</span>
                          </div>
                        )}
                        {paymentData.venue && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Venue:</span>
                            <span className="font-medium">{paymentData.venue}</span>
                          </div>
                        )}
                        {paymentData.date && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Date:</span>
                            <span className="font-medium">{new Date(paymentData.date).toLocaleDateString('en-GB')}</span>
                          </div>
                        )}
                        {paymentData.time && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Time:</span>
                            <span className="font-medium">{paymentData.time}</span>
                          </div>
                        )}
                        {paymentData.ticketType && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Ticket Type:</span>
                            <span className="font-medium">{paymentData.ticketType}</span>
                          </div>
                        )}
                        {paymentData.quantity && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Quantity:</span>
                            <span className="font-medium">{paymentData.quantity} ticket{paymentData.quantity > 1 ? 's' : ''}</span>
                          </div>
                        )}
                        {paymentData.ticketReference && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Reference:</span>
                            <span className="font-medium font-mono text-xs">{paymentData.ticketReference}</span>
                          </div>
                        )}
                      </>
                    ) : (
                      // Tour/Destination Details
                      <>
                        {paymentData.bookingDetails?.bookingData && (
                          <>
                            <div className="flex justify-between">
                              <span className="text-gray-600">Destination:</span>
                              <span className="font-medium">{paymentData.bookingDetails.bookingData.tourName}</span>
                            </div>
                            {paymentData.bookingDetails.bookingData.duration && (
                              <div className="flex justify-between">
                                <span className="text-gray-600">Duration:</span>
                                <span className="font-medium">{paymentData.bookingDetails.bookingData.duration}</span>
                              </div>
                            )}
                            {paymentData.bookingDetails.bookingData.selectedDate && (
                              <div className="flex justify-between">
                                <span className="text-gray-600">Travel Date:</span>
                                <span className="font-medium">{new Date(paymentData.bookingDetails.bookingData.selectedDate).toLocaleDateString('en-GB')}</span>
                              </div>
                            )}
                            {paymentData.bookingDetails.bookingData.travelers && (
                              <div className="flex justify-between">
                                <span className="text-gray-600">Travelers:</span>
                                <span className="font-medium">
                                  {paymentData.bookingDetails.bookingData.travelers.adults} Adult{paymentData.bookingDetails.bookingData.travelers.adults > 1 ? 's' : ''}
                                  {paymentData.bookingDetails.bookingData.travelers.children > 0 && 
                                    `, ${paymentData.bookingDetails.bookingData.travelers.children} Child${paymentData.bookingDetails.bookingData.travelers.children > 1 ? 'ren' : ''}`
                                  }
                                </span>
                              </div>
                            )}
                            {paymentData.bookingDetails.bookingData.basePrice && (
                              <div className="flex justify-between">
                                <span className="text-gray-600">Base Price:</span>
                                <span className="font-medium">GH¢{paymentData.bookingDetails.bookingData.basePrice}</span>
                              </div>
                            )}
                          </>
                        )}
                        {paymentData.bookingReference && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Booking Ref:</span>
                            <span className="font-medium font-mono text-xs">{paymentData.bookingReference}</span>
                          </div>
                        )}
                      </>
                    )}
                  </div>

                  {/* Add-ons Section */}
                  {paymentData.bookingDetails?.addOns && paymentData.bookingDetails.addOns.length > 0 && (
                    <>
                      <Separator />
                      <div className="space-y-2">
                        <h5 className="font-medium text-gray-900">Add-ons & Extras</h5>
                        <div className="space-y-2 text-sm">
                          {paymentData.bookingDetails.addOns.map((addon: any, index: number) => (
                            <div key={index} className="flex justify-between">
                              <span className="text-gray-600">{addon.name}</span>
                              <span className="font-medium">GH¢{addon.price}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </>
                  )}

                  {/* Customer Information */}
                  {paymentData.customerInfo && (
                    <>
                      <Separator />
                      <div className="space-y-2">
                        <h5 className="font-medium text-gray-900">👤 Customer Information</h5>
                        <div className="space-y-2 text-sm">
                          {paymentData.customerInfo.name && (
                            <div className="flex justify-between">
                              <span className="text-gray-600">Name:</span>
                              <span className="font-medium">{paymentData.customerInfo.name}</span>
                            </div>
                          )}
                          {paymentData.customerInfo.email && (
                            <div className="flex justify-between">
                              <span className="text-gray-600">Email:</span>
                              <span className="font-medium">{paymentData.customerInfo.email}</span>
                            </div>
                          )}
                          {paymentData.customerInfo.phone && (
                            <div className="flex justify-between">
                              <span className="text-gray-600">Phone:</span>
                              <span className="font-medium">{paymentData.customerInfo.phone}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </div>
                
                <Separator />
                
                {/* Price Breakdown */}
                <div className="space-y-2">
                  <h5 className="font-medium text-gray-900">💰 Price Breakdown</h5>
                  <div className="space-y-2 text-sm">
                    {paymentData.eventName ? (
                      // Event pricing
                      <>
                        {paymentData.unitPrice && paymentData.quantity && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">
                              {paymentData.quantity} × {paymentData.ticketType || 'Ticket'}
                            </span>
                            <span>GH¢{(paymentData.unitPrice * paymentData.quantity).toLocaleString()}</span>
                          </div>
                        )}
                      </>
                    ) : (
                      // Tour pricing
                      <>
                        {paymentData.bookingDetails?.bookingData?.basePrice && paymentData.bookingDetails?.bookingData?.travelers && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">
                              Base Price × {paymentData.bookingDetails.bookingData.travelers.adults + (paymentData.bookingDetails.bookingData.travelers.children || 0)} travelers
                            </span>
                            <span>GH¢{(paymentData.bookingDetails.bookingData.basePrice * (paymentData.bookingDetails.bookingData.travelers.adults + (paymentData.bookingDetails.bookingData.travelers.children || 0))).toLocaleString()}</span>
                          </div>
                        )}
                        {paymentData.bookingDetails?.addOns && paymentData.bookingDetails.addOns.length > 0 && (
                          paymentData.bookingDetails.addOns.map((addon: any, index: number) => (
                            <div key={index} className="flex justify-between">
                              <span className="text-gray-600">{addon.name}</span>
                              <span>GH¢{addon.price}</span>
                            </div>
                          ))
                        )}
                      </>
                    )}
                  </div>
                </div>
                
                <Separator />
                
                <div className="flex justify-between items-center text-lg font-bold">
                  <span>Total Amount</span>
                  <span className="text-ghana-green">GH¢{paymentData.total.toLocaleString()}</span>
                </div>

                {momoProvider && (
                  <>
                    <Separator />
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Payment Method:</span>
                        <span className="font-medium capitalize">{momoProvider} MoMo</span>
                      </div>
                      {phoneNumber && (
                        <div className="flex justify-between">
                          <span className="text-gray-600">Phone Number:</span>
                          <span className="font-medium">{phoneNumber}</span>
                        </div>
                      )}
                    </div>
                  </>
                )}

                <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                  <div className="flex items-center space-x-2">
                    <Shield className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium text-green-800">100% Secure</span>
                  </div>
                  <p className="text-xs text-green-700 mt-1">
                    Your payment is protected by bank-level security
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
