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
    const [phoneNumber, setPhoneNumber] = useState<string>("");
    const [accountName, setAccountName] = useState<string>("");
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

        if (!momoProvider || !phoneNumber || !accountName) {
            setError('Please fill in all payment details');
            return;
        }

        setIsProcessing(true);
        setStep('processing');
        setError(null);

        try {
            // Step 1: Create payment using the payment system
            const paymentResponse = await fetch('http://localhost:8000/api/payments/checkout/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    amount: purchaseData.totalAmount,
                    currency: 'GHS',
                    payment_method: 'momo',
                    provider_code: 'mtn_momo', // Use provider code instead of ID
                    phone_number: `+233${phoneNumber.replace(/^0/, '')}`, // Format phone number
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
                        payment_provider: momoProvider,
                        account_name: accountName
                    }
                })
            });

            const paymentResult = await paymentResponse.json();

            if (paymentResult.success) {
                const paymentReference = paymentResult.payment.reference;
                setStatusMessage('Payment request sent to your phone. Please check your mobile money app and authorize the payment.');

                // Step 2: Poll for payment status
                let attempts = 0;
                const maxAttempts = 60; // 5 minutes (5 second intervals)

                const pollPaymentStatus = async () => {
                    try {
                        const statusResponse = await fetch(`http://localhost:8000/api/payments/${paymentReference}/status/`);
                        const statusResult = await statusResponse.json();

                        if (statusResult.status === 'successful') {
                            setStatusMessage('Payment successful! Creating your tickets...');
                            // Step 3: Create ticket purchase after successful payment
                            const ticketResponse = await fetch('http://localhost:8000/api/tickets/purchase/direct/', {
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
                        } else if (statusResult.status === 'failed' || statusResult.status === 'cancelled') {
                            setError('Payment was declined or cancelled. Please try again.');
                            setIsProcessing(false);
                            setStep('details');
                        } else if (statusResult.status === 'pending' || statusResult.status === 'processing') {
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
            <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8">
                <div className="max-w-4xl mx-auto px-4">
                    {/* Header */}
                    <div className="flex items-center gap-4 mb-8">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => navigate(-1)}
                            className="flex items-center gap-2"
                        >
                            <ArrowLeft className="w-4 h-4" />
                            Back
                        </Button>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">Complete Your Ticket Purchase</h1>
                            <p className="text-gray-600">Secure checkout for your event tickets</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Payment Form */}
                        <div className="lg:col-span-2 space-y-6">
                            {/* Customer Information */}
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <User className="w-5 h-5" />
                                        Customer Information
                                    </CardTitle>
                                    <CardDescription>
                                        Please provide your details for the ticket purchase
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <Label htmlFor="name">Full Name *</Label>
                                            <Input
                                                id="name"
                                                type="text"
                                                placeholder="Enter your full name"
                                                value={customerInfo.name}
                                                onChange={(e) => handleInputChange('name', e.target.value)}
                                                required
                                            />
                                        </div>
                                        <div>
                                            <Label htmlFor="email">Email Address *</Label>
                                            <Input
                                                id="email"
                                                type="email"
                                                placeholder="Enter your email"
                                                value={customerInfo.email}
                                                onChange={(e) => handleInputChange('email', e.target.value)}
                                                required
                                            />
                                        </div>
                                    </div>
                                    <div>
                                        <Label htmlFor="phone">Phone Number *</Label>
                                        <Input
                                            id="phone"
                                            type="tel"
                                            placeholder="e.g., 0241234567"
                                            value={customerInfo.phone}
                                            onChange={(e) => handleInputChange('phone', e.target.value)}
                                            required
                                        />
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Payment Method */}
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Smartphone className="w-5 h-5" />
                                        Mobile Money Payment
                                    </CardTitle>
                                    <CardDescription>
                                        Choose your mobile money provider
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div>
                                        <Label>Select Provider *</Label>
                                        <RadioGroup value={momoProvider} onValueChange={setMomoProvider} className="mt-2">
                                            <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50">
                                                <RadioGroupItem value="mtn" id="mtn" />
                                                <Label htmlFor="mtn" className="flex items-center gap-2 cursor-pointer flex-1">
                                                    <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center">
                                                        <span className="text-xs font-bold text-black">MTN</span>
                                                    </div>
                                                    MTN Mobile Money
                                                </Label>
                                            </div>
                                            <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50">
                                                <RadioGroupItem value="vodafone" id="vodafone" />
                                                <Label htmlFor="vodafone" className="flex items-center gap-2 cursor-pointer flex-1">
                                                    <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
                                                        <span className="text-xs font-bold text-white">VOD</span>
                                                    </div>
                                                    Vodafone Cash
                                                </Label>
                                            </div>
                                            <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50">
                                                <RadioGroupItem value="airteltigo" id="airteltigo" />
                                                <Label htmlFor="airteltigo" className="flex items-center gap-2 cursor-pointer flex-1">
                                                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                                        <span className="text-xs font-bold text-white">AT</span>
                                                    </div>
                                                    AirtelTigo Money
                                                </Label>
                                            </div>
                                        </RadioGroup>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <Label htmlFor="phoneNumber">Mobile Money Number *</Label>
                                            <Input
                                                id="phoneNumber"
                                                type="tel"
                                                placeholder="e.g., 0241234567"
                                                value={phoneNumber}
                                                onChange={(e) => setPhoneNumber(e.target.value)}
                                                required
                                            />
                                        </div>
                                        <div>
                                            <Label htmlFor="accountName">Account Name *</Label>
                                            <Input
                                                id="accountName"
                                                type="text"
                                                placeholder="Name on mobile money account"
                                                value={accountName}
                                                onChange={(e) => setAccountName(e.target.value)}
                                                required
                                            />
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>

                            {error && (
                                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                                    <p className="text-red-800 text-sm">{error}</p>
                                </div>
                            )}
                        </div>

                        {/* Order Summary */}
                        <div className="lg:col-span-1">
                            <Card className="sticky top-8">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Ticket className="w-5 h-5" />
                                        Order Summary
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="space-y-3">
                                        <h3 className="font-semibold text-lg">{purchaseData.ticketTitle}</h3>

                                        <div className="space-y-2 text-sm text-gray-600">
                                            <div className="flex items-center gap-2">
                                                <MapPin className="w-4 h-4" />
                                                <span>{purchaseData.venue}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Calendar className="w-4 h-4" />
                                                <span>{new Date(purchaseData.eventDate).toLocaleDateString()}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Clock className="w-4 h-4" />
                                                <span>{new Date(purchaseData.eventDate).toLocaleTimeString()}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Users className="w-4 h-4" />
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