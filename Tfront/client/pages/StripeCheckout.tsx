import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, CreditCard, Shield, AlertCircle } from "lucide-react";

interface PaymentData {
  tourName: string;
  total: number;
  bookingReference: string;
  paymentMethod: string;
  bookingDetails: any;
}

export default function StripeCheckout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [paymentData, setPaymentData] = useState<PaymentData | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (location.state) {
      setPaymentData(location.state as PaymentData);
    } else {
      // Redirect back if no payment data
      navigate("/");
    }
  }, [location.state, navigate]);

  const handleStripePayment = async () => {
    if (!paymentData) return;

    setIsProcessing(true);
    setError("");

    try {
      // For now, simulate Stripe integration
      // In a real implementation, you would:
      // 1. Create a payment intent on your backend
      // 2. Use Stripe Elements to collect payment details
      // 3. Confirm the payment with Stripe
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simulate success (90% success rate for demo)
      if (Math.random() > 0.1) {
        navigate("/payment-success", {
          state: {
            ...paymentData,
            paymentDetails: {
              method: "Credit/Debit Card",
              provider: "Stripe",
              transactionId: `stripe_${Date.now()}`,
              status: "completed",
              timestamp: new Date().toISOString()
            }
          }
        });
      } else {
        throw new Error("Payment failed. Please try again.");
      }
    } catch (err: any) {
      setError(err.message || "Payment failed. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  if (!paymentData) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <p>Loading payment details...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        {/* Header */}
        <div className="flex items-center space-x-4 mb-6">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(-1)}
            className="flex items-center space-x-2"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back</span>
          </Button>
          <div>
            <h1 className="text-2xl font-bold">Secure Card Payment</h1>
            <p className="text-gray-600">Complete your booking with Stripe</p>
          </div>
        </div>

        <div className="grid gap-6">
          {/* Payment Summary */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <CreditCard className="h-5 w-5 text-ghana-green" />
                <span>Payment Summary</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="font-medium">Tour</span>
                <span>{paymentData.tourName}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">Booking Reference</span>
                <span className="font-mono text-sm">{paymentData.bookingReference}</span>
              </div>
              <Separator />
              <div className="flex justify-between text-lg font-bold">
                <span>Total Amount</span>
                <span>GH₵{paymentData.total.toLocaleString()}</span>
              </div>
            </CardContent>
          </Card>

          {/* Stripe Payment Form */}
          <Card>
            <CardHeader>
              <CardTitle>Card Details</CardTitle>
              <CardDescription>
                Your payment is secured by Stripe. We don't store your card details.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Security Notice */}
              <div className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg">
                <Shield className="h-5 w-5 text-blue-600 mt-0.5" />
                <div className="text-sm">
                  <p className="font-medium text-blue-900">Secure Payment</p>
                  <p className="text-blue-700">
                    This is a demo. In production, Stripe Elements would be integrated here 
                    to securely collect your card details.
                  </p>
                </div>
              </div>

              {/* Demo Notice */}
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-start space-x-3">
                  <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5" />
                  <div className="text-sm">
                    <p className="font-medium text-yellow-900">Demo Mode</p>
                    <p className="text-yellow-700">
                      This is a demonstration. To enable real Stripe payments, you need to:
                    </p>
                    <ul className="mt-2 list-disc list-inside text-yellow-700 space-y-1">
                      <li>Add your Stripe publishable and secret keys</li>
                      <li>Integrate Stripe Elements for card collection</li>
                      <li>Set up webhook endpoints for payment confirmation</li>
                    </ul>
                  </div>
                </div>
              </div>

              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <AlertCircle className="h-5 w-5 text-red-600" />
                    <p className="text-red-700 font-medium">{error}</p>
                  </div>
                </div>
              )}

              {/* Payment Button */}
              <Button
                onClick={handleStripePayment}
                disabled={isProcessing}
                className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white py-3"
                size="lg"
              >
                {isProcessing ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Processing Payment...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Shield className="h-4 w-4" />
                    <span>Pay GH₵{paymentData.total.toLocaleString()} Securely</span>
                  </div>
                )}
              </Button>

              <p className="text-xs text-gray-500 text-center">
                By clicking "Pay Securely", you agree to our terms and conditions.
                Your payment is protected by Stripe's security measures.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}