import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
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
    AlertCircle, Loader2, Phone, User, CreditCard,
    Ticket, Calendar, MapPin, Clock, Users
} from "lucide-react";

interface TicketPurchaseData {
    type: string;
    ticketId: number;
    ticketTitle: string;
    venue: string;
    eventDate: string;
    quantity: number;
    unitPrice: number;
    totalAmount: number;
    customerInfo: {
        name: string;
        email: string;
        phone: string;
    };
}

// Helper function to map frontend provider names to backend payment method codes
const getPaymentMethodCode = (provider: string): string => {
    const mapping: { [key: string]: string } = {
        'MTN Mobile Money': 'mtn_momo',
        'Vodafone Cash': 'vodafone_cash',
        'AirtelTigo Money': 'airteltigo_money'
    };
    return mapping[provider] || 'momo';
};

export default function TicketCheckout() {
    const navigate = useNavigate();

    const [purchaseData, setPurchaseData] = useState<TicketPurchaseData | null>(null);
    const [customerInfo, setCustomerInfo] = useState({
        name: '',
        email: '',
        phone: ''
    });
    const [momoProvider, setMomoProvider] = useState<string>("");
    const [isProcessing, setIsProcessing] = useState(false);
    const [step, setStep] = useState<'details' | 'processing' | 'verify'>('details');
    const [statusMessage, setStatusMessage] = useState<string>('Payment request sent to your phone');
    const [pollingAttempts, setPollingAttempts] = useState<number>(0);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Get ticket purchase data from localStorage
        const storedData = localStorage.getItem('pendingTicketPurchase');
        if (storedData) {
            try {
                const data = JSON.parse(storedData);
                setPurchaseData(data);

                // Pre-fill customer info if available
                if (data.customerInfo) {
                    setCustomerInfo({
                        name: data.customerInfo.name || '',
                        email: data.customerInfo.email || '',
                        phone: data.customerInfo.phone || ''
                    });
                    setPhoneNumber(data.customerInfo.phone || '');
                }
            } catch (e) {
                console.error('Error parsing ticket purchase data:', e);
                navigate('/tickets');
            }
        } else {
            // No purchase data, redirect back to tickets
            navigate('/tickets');
        }
    }, [navigate]);

    const handleInputChange = (field: string, value: string) => {
        setCustomerInfo(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handlePurchase = async () => {
        if (!purchaseData || !customerInfo.name || !customerInfo.email || !customerInfo.phone) {
            setError('Please fill in all required fields');
            return;
        }

        if (!momoProvider) {
            setError('Please select a mobile money provider');
            return;
        }

        setIsProcessing(true);
        setStep('processing');
        setError(null);

        try {
            // Use Paystack for mobile money (same as other working checkouts)
            const paymentResponse = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/paystack/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    amount: purchaseData.totalAmount,
                    currency: 'GHS',
                    payment_method: 'mobile_money',
                    provider: momoProvider.toLowerCase(), // mtn, vodafone, airteltigo
                    phone_number: customerInfo.phone.startsWith('0') ? customerInfo.phone : `0${customerInfo.phone}`,
                    email: customerInfo.email,
                    description: `Ticket Purchase: ${purchaseData.ticketTitle} (${purchaseData.quantity} tickets)`,
                    booking_details: {
                        type: 'ticket',
                        ticket_id: purchaseData.ticketId,
                        ticket_title: purchaseData.ticketTitle,
                        quantity: purchaseData.quantity,
                        unit_price: purchaseData.unitPrice,
                        customer_name: customerInfo.name,
                        customer_email: customerInfo.email,
                        customer_phone: customerInfo.phone,
                        payment_provider: momoProvider
                    }
                })
            });

            const paymentResult = await paymentResponse.json();

            if (paymentResult.success) {
                const paymentReference = paymentResult.payment.reference;
                const authorizationUrl = paymentResult.paystack?.authorization_url;
                
                // Update the stored ticket purchase data with customer info
                const updatedPurchaseData = {
                    ...purchaseData,
                    customerInfo: {
                        name: customerInfo.name,
                        email: customerInfo.email,
                        phone: customerInfo.phone
                    },
                    paymentProvider: momoProvider
                };
                localStorage.setItem('pendingTicketPurchase', JSON.stringify(updatedPurchaseData));
                
                // Check if we have an authorization URL (this should always be present for Paystack)
                if (authorizationUrl) {
                    console.log('🎫 Redirecting to Paystack for mobile money:', authorizationUrl);
                    // Store payment reference for callback
                    localStorage.setItem('pendingPaymentReference', paymentReference);
                    // Redirect to Paystack website
                    window.location.href = authorizationUrl;
                    return; // Exit here as we're redirecting
                }
                
                // Fallback for test mode or if no authorization URL
                const isTestMode = paymentResult.test_mode;
                const message = isTestMode ? 
                    'Test Mode: Mobile money payment simulated. Payment will be automatically approved in 10 seconds.' :
                    'Payment request sent to your phone. Please check your mobile money app and authorize the payment.';
                    
                setStatusMessage(message);

                // Step 2: Poll for payment status (fallback only)
                let attempts = 0;
                const maxAttempts = 60; // 5 minutes (5 second intervals)

                const pollPaymentStatus = async () => {
                    try {
                        const statusResponse = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/paystack/verify/${paymentReference}/`);
                        const statusResult = await statusResponse.json();
                        
                        const paymentStatus = statusResult.payment?.status;
                        const isTestMode = statusResult.test_mode;

                        if (paymentStatus === 'successful') {
                            const message = isTestMode ? 
                                'Test mode: Payment approved! Creating your tickets...' : 
                                'Payment successful! Creating your tickets...';
                            setStatusMessage(message);
                            // Step 3: Create ticket purchase after successful payment
                            const ticketResponse = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/tickets/purchase/direct/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    ticket_id: purchaseData.ticketId,
                                    quantity: purchaseData.quantity,
                                    total_amount: purchaseData.totalAmount,
                                    customer_name: customerInfo.name,
                                    customer_email: customerInfo.email,
                                    customer_phone: customerInfo.phone,
                                    payment_method: getPaymentMethodCode(momoProvider),
                                    payment_reference: paymentReference,
                                    special_requests: `Mobile Money Payment - ${momoProvider} - ${phoneNumber} - Account: ${accountName}`
                                })
                            });

                            const ticketResult = await ticketResponse.json();

                            if (ticketResult.success) {
                                // Clear the stored data
                                localStorage.removeItem('pendingTicketPurchase');

                                // Navigate to success page with purchase details
                                navigate('/ticket-purchase-success', {
                                    state: {
                                        purchase: ticketResult.purchase,
                                        paymentReference: paymentReference,
                                        paymentDetails: {
                                            method: 'Mobile Money',
                                            provider: momoProvider,
                                            phone: phoneNumber,
                                            accountName: accountName
                                        }
                                    }
                                });
                            } else {
                                setError('Payment successful but failed to create ticket. Please contact support.');
                                setIsProcessing(false);
                                setStep('details');
                            }
                        } else if (paymentStatus === 'failed' || paymentStatus === 'cancelled') {
                            setError('Payment was declined or cancelled. Please try again.');
                            setIsProcessing(false);
                            setStep('details');
                        } else if (paymentStatus === 'pending' || paymentStatus === 'processing') {
                            attempts++;
                            if (attempts < maxAttempts) {
                                const minutes = Math.floor(attempts * 5 / 60);
                                const seconds = attempts * 5 % 60;
                                setStatusMessage(`Waiting for payment authorization... (${minutes}:${String(seconds).padStart(2, '0')})`);
                                setTimeout(pollPaymentStatus, 5000); // Poll every 5 seconds
                            } else {
                                setError('Payment timeout. Please try again or contact support if money was deducted.');
                                setIsProcessing(false);
                                setStep('details');
                            }
                        }
                    } catch (pollError) {
                        console.error('Payment status polling error:', pollError);
                        attempts++;
                        if (attempts < maxAttempts) {
                            setTimeout(pollPaymentStatus, 5000);
                        } else {
                            setError('Unable to verify payment status. Please contact support.');
                            setIsProcessing(false);
                            setStep('details');
                        }
                    }
                };

                // Start polling after 2 seconds
                setTimeout(pollPaymentStatus, 2000);

            } else {
                setError(paymentResult.error || 'Failed to initiate payment');
                setIsProcessing(false);
                setStep('details');
            }
        } catch (err) {
            console.error('Payment initiation error:', err);
            setError('An error occurred while processing your payment');
            setIsProcessing(false);
            setStep('details');
        }
    };

    if (!purchaseData) {
        return (
            <Layout>
                <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
                    <div className="flex items-center space-x-2">
                        <Loader2 className="h-6 w-6 animate-spin" />
                        <span>Loading...</span>
                    </div>
                </div>
            </Layout>
        );
    }

    if (step === 'processing') {
        return (
            <Layout>
                <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
                    <Card className="w-full max-w-md">
                        <CardContent className="pt-6">
                            <div className="text-center space-y-4">
                                <div className="flex justify-center">
                                    <div className="relative">
                                        <Smartphone className="h-16 w-16 text-ghana-green" />
                                        <div className="absolute -top-1 -right-1">
                                            <div className="h-4 w-4 bg-green-500 rounded-full animate-pulse"></div>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-900">Processing Payment</h3>
                                    <p className="text-sm text-gray-600 mt-2">{statusMessage}</p>
                                </div>
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <div className="flex items-center space-x-2 text-blue-800">
                                        <AlertCircle className="h-4 w-4" />
                                        <span className="text-sm font-medium">Check your phone for the payment prompt</span>
                                    </div>
                                </div>
                                <Button
                                    variant="outline"
                                    onClick={() => {
                                        setStep('details');
                                        setIsProcessing(false);
                                    }}
                                    className="w-full"
                                >
                                    Cancel Payment
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-4 sm:py-8">
                <div className="mobile-container max-w-4xl">
                    {/* Header - Mobile Optimized */}
                    <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-6 sm:mb-8">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => navigate(-1)}
                            className="flex items-center gap-2 w-fit"
                        >
                            <ArrowLeft className="w-4 h-4" />
                            Back
                        </Button>
                        <div className="flex-1">
                            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight">
                                Complete Your Ticket Purchase
                            </h1>
                            <p className="text-gray-600 text-sm sm:text-base mt-1">
                                Secure checkout for your event tickets
                            </p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
                        {/* Payment Form - Mobile Optimized */}
                        <div className="lg:col-span-2 space-y-4 sm:space-y-6">
                            {/* Customer Information */}
                            <Card>
                                <CardHeader className="pb-4">
                                    <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
                                        <User className="w-5 h-5" />
                                        Customer Information
                                    </CardTitle>
                                    <CardDescription className="text-sm">
                                        Please provide your details for the ticket purchase
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="space-y-4">
                                        <div>
                                            <Label htmlFor="name" className="mobile-form-label">Full Name *</Label>
                                            <Input
                                                id="name"
                                                type="text"
                                                placeholder="Enter your full name"
                                                className="mobile-input"
                                                value={customerInfo.name}
                                                onChange={(e) => handleInputChange('name', e.target.value)}
                                                required
                                            />
                                        </div>
                                        <div>
                                            <Label htmlFor="email" className="mobile-form-label">Email Address *</Label>
                                            <Input
                                                id="email"
                                                type="email"
                                                placeholder="Enter your email"
                                                className="mobile-input"
                                                value={customerInfo.email}
                                                onChange={(e) => handleInputChange('email', e.target.value)}
                                                required
                                            />
                                        </div>
                                        <div>
                                            <Label htmlFor="phone" className="mobile-form-label">Phone Number *</Label>
                                            <Input
                                                id="phone"
                                                type="tel"
                                                placeholder="e.g., 0241234567"
                                                className="mobile-input"
                                                value={customerInfo.phone}
                                                onChange={(e) => handleInputChange('phone', e.target.value)}
                                                required
                                            />
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Payment Method - Mobile Optimized */}
                            <Card>
                                <CardHeader className="pb-4">
                                    <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
                                        <Smartphone className="w-5 h-5" />
                                        Mobile Money Payment
                                    </CardTitle>
                                    <CardDescription className="text-sm">
                                        Choose your mobile money provider
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div>
                                        <Label className="mobile-form-label">Select Provider *</Label>
                                        <RadioGroup value={momoProvider} onValueChange={setMomoProvider} className="mt-3 space-y-3">
                                            <div className="touch-target flex items-center space-x-3 p-4 border-2 rounded-lg hover:bg-gray-50 transition-colors">
                                                <RadioGroupItem value="mtn" id="mtn" className="flex-shrink-0" />
                                                <Label htmlFor="mtn" className="flex items-center gap-3 cursor-pointer flex-1">
                                                    <div className="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center flex-shrink-0">
                                                        <span className="text-sm font-bold text-black">MTN</span>
                                                    </div>
                                                    <span className="font-medium">MTN Mobile Money</span>
                                                </Label>
                                            </div>
                                            <div className="touch-target flex items-center space-x-3 p-4 border-2 rounded-lg hover:bg-gray-50 transition-colors">
                                                <RadioGroupItem value="vodafone" id="vodafone" className="flex-shrink-0" />
                                                <Label htmlFor="vodafone" className="flex items-center gap-3 cursor-pointer flex-1">
                                                    <div className="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0">
                                                        <span className="text-sm font-bold text-white">VOD</span>
                                                    </div>
                                                    <span className="font-medium">Vodafone Cash</span>
                                                </Label>
                                            </div>
                                            <div className="touch-target flex items-center space-x-3 p-4 border-2 rounded-lg hover:bg-gray-50 transition-colors">
                                                <RadioGroupItem value="airteltigo" id="airteltigo" className="flex-shrink-0" />
                                                <Label htmlFor="airteltigo" className="flex items-center gap-3 cursor-pointer flex-1">
                                                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                                                        <span className="text-sm font-bold text-white">AT</span>
                                                    </div>
                                                    <span className="font-medium">AirtelTigo Money</span>
                                                </Label>
                                            </div>
                                        </RadioGroup>
                                    </div>
                                </CardContent>
                            </Card>

                            {error && (
                                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                                    <p className="text-red-800 text-sm">{error}</p>
                                </div>
                            )}
                        </div>

                        {/* Order Summary - Mobile Optimized */}
                        <div className="lg:col-span-1 order-first lg:order-last">
                            <Card className="lg:sticky lg:top-8">
                                <CardHeader className="pb-4">
                                    <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
                                        <Ticket className="w-5 h-5" />
                                        Order Summary
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="space-y-3">
                                        <h3 className="font-semibold text-base sm:text-lg leading-tight">
                                            {purchaseData.ticketTitle}
                                        </h3>

                                        <div className="space-y-3 text-sm text-gray-600">
                                            <div className="flex items-start gap-3">
                                                <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                                <span className="flex-1">{purchaseData.venue}</span>
                                            </div>
                                            <div className="flex items-center gap-3">
                                                <Calendar className="w-4 h-4 flex-shrink-0" />
                                                <span>{new Date(purchaseData.eventDate).toLocaleDateString()}</span>
                                            </div>
                                            <div className="flex items-center gap-3">
                                                <Clock className="w-4 h-4 flex-shrink-0" />
                                                <span>{new Date(purchaseData.eventDate).toLocaleTimeString()}</span>
                                            </div>
                                            <div className="flex items-center gap-3">
                                                <Users className="w-4 h-4 flex-shrink-0" />
                                                <span>{purchaseData.quantity} ticket{purchaseData.quantity > 1 ? 's' : ''}</span>
                                            </div>
                                        </div>
                                    </div>

                                    <Separator />

                                    <div className="space-y-2">
                                        <div className="flex justify-between">
                                            <span>Ticket Price</span>
                                            <span>GH₵ {purchaseData.unitPrice}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>Quantity</span>
                                            <span>{purchaseData.quantity}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>Subtotal</span>
                                            <span>GH₵ {purchaseData.totalAmount}</span>
                                        </div>
                                    </div>

                                    <Separator />

                                    <div className="flex justify-between font-semibold text-lg">
                                        <span>Total</span>
                                        <span className="text-ghana-green">GH₵ {purchaseData.totalAmount}</span>
                                    </div>

                                    <Button
                                        onClick={handlePurchase}
                                        disabled={isProcessing || !customerInfo.name || !customerInfo.email || !customerInfo.phone || !momoProvider || !phoneNumber || !accountName}
                                        className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                                        size="lg"
                                    >
                                        {isProcessing ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Processing...
                                            </>
                                        ) : (
                                            <>
                                                <Smartphone className="w-4 h-4 mr-2" />
                                                Pay GH₵ {purchaseData.totalAmount}
                                            </>
                                        )}
                                    </Button>

                                    <div className="text-xs text-gray-500 text-center space-y-1">
                                        <p className="flex items-center justify-center gap-1">
                                            <Shield className="w-3 h-3" />
                                            Your payment is secured with bank-level encryption
                                        </p>
                                        <p>You will receive a payment prompt on your phone</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
} 