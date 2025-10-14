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
  ArrowLeft, CreditCard, Shield, CheckCircle, 
  AlertCircle, Loader2, Mail, User, Smartphone
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

export default function PaystackCheckout() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const paymentData = location.state as PaymentData;
  
  const [paymentType, setPaymentType] = useState<string>("card");
  const [email, setEmail] = useState<string>("");
  const [fullName, setFullName] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [momoProvider, setMomoProvider] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [step, setStep] = useState<'details' | 'processing' | 'redirect'>('details');
  
  useEffect(() => {
    if (!paymentData) {
      navigate('/booking/1');
      return;
    }
    
    // Pre-fill customer info if available
    if (paymentData.customerInfo) {
      setEmail(paymentData.customerInfo.email || '');
      setFullName(paymentData.customerInfo.name || 
        `${paymentData.customerInfo.firstName || ''} ${paymentData.customerInfo.lastName || ''}`.trim());
      setPhoneNumber(paymentData.customerInfo.phone || '');
    }
  }, [paymentData, navigate]);

  const handlePayment = async () => {
    if (!email || !fullName) {
      alert("Please fill in all required fields");
      return;
    }

    if (paymentType === 'mobile_money' && (!phoneNumber || !momoProvider)) {
      alert("Please fill in mobile money details");
      return;
    }

    setIsProcessing(true);
    setStep('processing');

    try {
      const authToken = localStorage.getItem('auth_token');
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (authToken) {
        headers['Authorization'] = `Token ${authToken}`;
      }
      
      // Format phone number for Ghana
      const formattedPhone = phoneNumber.startsWith('+') 
        ? phoneNumber 
        : `+233${phoneNumber.replace(/^0/, '')}`;
      
      const requestData: any = {
        amount: paymentData.total,
        currency: 'GHS',
        payment_method: paymentType,
        email: email,
        description: paymentData.tourName || paymentData.eventName || 'Payment',
        booking_details: paymentData.bookingDetails || null,
      };

      // Add mobile money specific data
      if (paymentType === 'mobile_money') {
        requestData.provider = momoProvider;
        requestData.phone_number = formattedPhone;
      }
      
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/paystack/create/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestData)
      });

      const result = await response.json();

      if (result.success) {
        if (paymentType === 'card' && result.paystack?.authorization_url) {
          // For card payments, redirect to Paystack
          setStep('redirect');
          
          // Store payment reference for later verification
          sessionStorage.setItem('paymentReference', result.payment.reference);
          
          // Redirect to Paystack
          window.location.href = result.paystack.authorization_url;
        } else if (paymentType === 'mobile_money') {
          // For mobile money, redirect to mobile money checkout
          navigate('/momo-checkout', { 
            state: {
              ...paymentData,
              paymentReference: result.payment.reference,
              paystackData: result.paystack
            }
          });
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
                <h1 className="text-2xl font-bold">Secure Payment</h1>
                <p className="text-ghana-gold">Powered by Paystack Ghana</p>
              </div>
            </div>
            <Badge className="bg-white text-ghana-green px-4 py-2">
              {step === 'details' && 'Step 1 of 2'}
              {step === 'processing' && 'Processing...'}
              {step === 'redirect' && 'Redirecting...'}
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
                    <CreditCard className="h-5 w-5 text-ghana-green" />
                    <span>Payment Method</span>
                  </CardTitle>
                  <CardDescription>
                    Choose your preferred payment method
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  
                  {/* Payment Method Selection */}
                  <div className="space-y-3">
                    <Label className="text-base font-medium">Select Payment Method</Label>
                    <RadioGroup value={paymentType} onValueChange={setPaymentType} className="space-y-3">
                      <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="card" id="card" />
                        <Label htmlFor="card" className="flex-1 cursor-pointer">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                <CreditCard className="h-4 w-4 text-white" />
                              </div>
                              <div>
                                <p className="font-medium">Credit/Debit Card</p>
                                <p className="text-sm text-gray-600">Visa, Mastercard, Verve</p>
                              </div>
                            </div>
                            <Badge variant="outline" className="text-blue-600">Instant</Badge>
                          </div>
                        </Label>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="mobile_money" id="mobile_money" />
                        <Label htmlFor="mobile_money" className="flex-1 cursor-pointer">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                                <Smartphone className="h-4 w-4 text-white" />
                              </div>
                              <div>
                                <p className="font-medium">Mobile Money</p>
                                <p className="text-sm text-gray-600">MTN, Vodafone, AirtelTigo</p>
                              </div>
                            </div>
                            <Badge variant="outline" className="text-green-600">Popular</Badge>
                          </div>
                        </Label>
                      </div>
                    </RadioGroup>
                  </div>

                  <Separator />

                  {/* Customer Information */}
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Customer Information</h3>
                    
                    {/* Email */}
                    <div className="space-y-2">
                      <Label htmlFor="email">Email Address *</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                        <Input
                          id="email"
                          type="email"
                          placeholder="your@email.com"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    {/* Full Name */}
                    <div className="space-y-2">
                      <Label htmlFor="fullName">Full Name *</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                        <Input
                          id="fullName"
                          type="text"
                          placeholder="John Doe"
                          value={fullName}
                          onChange={(e) => setFullName(e.target.value)}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    {/* Mobile Money Specific Fields */}
                    {paymentType === 'mobile_money' && (
                      <>
                        <div className="space-y-2">
                          <Label htmlFor="phone">Mobile Money Phone Number *</Label>
                          <div className="relative">
                            <Smartphone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
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
                        </div>

                        <div className="space-y-3">
                          <Label className="text-base font-medium">Mobile Money Provider *</Label>
                          <RadioGroup value={momoProvider} onValueChange={setMomoProvider} className="space-y-2">
                            <div className="flex items-center space-x-3 p-3 border rounded-lg">
                              <RadioGroupItem value="mtn" id="mtn_provider" />
                              <Label htmlFor="mtn_provider" className="flex-1 cursor-pointer">
                                <div className="flex items-center space-x-3">
                                  <div className="w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center">
                                    <span className="text-xs font-bold text-black">M</span>
                                  </div>
                                  <span>MTN Mobile Money</span>
                                </div>
                              </Label>
                            </div>
                            
                            <div className="flex items-center space-x-3 p-3 border rounded-lg">
                              <RadioGroupItem value="vodafone" id="vod_provider" />
                              <Label htmlFor="vod_provider" className="flex-1 cursor-pointer">
                                <div className="flex items-center space-x-3">
                                  <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center">
                                    <span className="text-xs font-bold text-white">V</span>
                                  </div>
                                  <span>Vodafone Cash</span>
                                </div>
                              </Label>
                            </div>
                            
                            <div className="flex items-center space-x-3 p-3 border rounded-lg">
                              <RadioGroupItem value="airteltigo" id="at_provider" />
                              <Label htmlFor="at_provider" className="flex-1 cursor-pointer">
                                <div className="flex items-center space-x-3">
                                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                                    <span className="text-xs font-bold text-white">A</span>
                                  </div>
                                  <span>AirtelTigo Money</span>
                                </div>
                              </Label>
                            </div>
                          </RadioGroup>
                        </div>
                      </>
                    )}
                  </div>

                  {/* Security Notice */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Shield className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="font-medium text-blue-900">Secure Payment by Paystack</h4>
                        <p className="text-sm text-blue-700 mt-1">
                          Your payment information is encrypted and secure. Paystack is PCI DSS compliant and trusted by thousands of businesses in Ghana.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Pay Button */}
                  <Button 
                    onClick={handlePayment}
                    disabled={!email || !fullName || (paymentType === 'mobile_money' && (!phoneNumber || !momoProvider)) || isProcessing}
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white py-3"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Processing Payment...
                      </>
                    ) : (
                      `Pay GH₵${paymentData.total.toLocaleString()} with ${paymentType === 'card' ? 'Card' : 'Mobile Money'}`
                    )}
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Processing Step */}
            {(step === 'processing' || step === 'redirect') && (
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
                        {step === 'processing' ? 'Processing Payment' : 'Redirecting to Paystack'}
                      </h3>
                      <p className="text-gray-600">
                        {step === 'processing' 
                          ? 'Please wait while we process your payment request...'
                          : 'You will be redirected to complete your payment securely...'
                        }
                      </p>
                    </div>
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
                <div className="space-y-2">
                  <h4 className="font-medium text-gray-900">
                    {paymentData.eventName || paymentData.tourName}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {paymentData.eventName ? (
                      <>
                        <span>Ticket Reference: {paymentData.ticketReference}</span><br/>
                        <span>{paymentData.artist} • {paymentData.venue}</span><br/>
                        <span>{new Date(paymentData.date!).toLocaleDateString('en-GB')} • {paymentData.time}</span>
                      </>
                    ) : (
                      <span>Booking Reference: {paymentData.bookingReference}</span>
                    )}
                  </p>
                </div>
                
                <Separator />
                
                <div className="flex justify-between items-center text-lg font-bold">
                  <span>Total Amount</span>
                  <span className="text-ghana-green">GH₵{paymentData.total.toLocaleString()}</span>
                </div>

                {paymentType && (
                  <>
                    <Separator />
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Payment Method:</span>
                        <span className="font-medium capitalize">
                          {paymentType === 'card' ? 'Credit/Debit Card' : 'Mobile Money'}
                        </span>
                      </div>
                      {email && (
                        <div className="flex justify-between">
                          <span className="text-gray-600">Email:</span>
                          <span className="font-medium">{email}</span>
                        </div>
                      )}
                    </div>
                  </>
                )}

                <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                  <div className="flex items-center space-x-2">
                    <Shield className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium text-green-800">Secured by Paystack</span>
                  </div>
                  <p className="text-xs text-green-700 mt-1">
                    PCI DSS compliant payment processing
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