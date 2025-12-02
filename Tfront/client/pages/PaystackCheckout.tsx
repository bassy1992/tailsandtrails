import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

declare global {
  interface Window {
    PaystackPop: any;
  }
}

export default function PaystackCheckout() {
  const location = useLocation();
  const navigate = useNavigate();
  const paymentData = location.state as any;
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!paymentData) {
      navigate('/');
      return;
    }

    // Load Paystack script
    const script = document.createElement('script');
    script.src = 'https://js.paystack.co/v1/inline.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, [paymentData, navigate]);

  const initiatePayment = () => {
    if (!window.PaystackPop) {
      setError('Payment system not loaded. Please refresh and try again.');
      return;
    }

    setLoading(true);
    setError(null);

    const handler = window.PaystackPop.setup({
      key: 'pk_test_your_paystack_public_key', // Replace with your Paystack public key
      email: paymentData.userInfo.email,
      amount: Math.round(paymentData.total * 100), // Amount in pesewas (GH₵ * 100)
      currency: 'GHS',
      ref: paymentData.bookingReference,
      metadata: {
        custom_fields: [
          {
            display_name: "Tour Name",
            variable_name: "tour_name",
            value: paymentData.tourName
          },
          {
            display_name: "Customer Name",
            variable_name: "customer_name",
            value: paymentData.userInfo.name
          },
          {
            display_name: "Phone Number",
            variable_name: "phone_number",
            value: paymentData.userInfo.phone || 'N/A'
          }
        ]
      },
      callback: function(response: any) {
        // Payment successful
        console.log('Payment successful:', response);
        navigate('/payment-success', {
          state: {
            reference: response.reference,
            tourName: paymentData.tourName,
            amount: paymentData.total,
            bookingReference: paymentData.bookingReference
          }
        });
      },
      onClose: function() {
        setLoading(false);
        setError('Payment cancelled. You can try again when ready.');
      }
    });

    handler.openIframe();
  };

  if (!paymentData) {
    return null;
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-center">Complete Your Payment</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Booking Summary */}
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Tour:</span>
                  <span className="font-semibold">{paymentData.tourName}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Booking Reference:</span>
                  <span className="font-semibold">{paymentData.bookingReference}</span>
                </div>
                <div className="flex justify-between text-lg font-bold">
                  <span>Total Amount:</span>
                  <span className="text-ghana-green">GH₵{paymentData.total.toLocaleString()}</span>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="flex items-center space-x-2 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <XCircle className="h-5 w-5 text-red-600" />
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              {/* Payment Button */}
              <Button
                onClick={initiatePayment}
                disabled={loading}
                className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white h-12"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <CheckCircle className="h-5 w-5 mr-2" />
                    Pay GH₵{paymentData.total.toLocaleString()} with Paystack
                  </>
                )}
              </Button>

              {/* Info */}
              <div className="text-center text-sm text-gray-600">
                <p>Secure payment powered by Paystack</p>
                <p className="mt-1">Supports Mobile Money, Cards, and Bank Transfer</p>
              </div>

              {/* Cancel */}
              <Button
                variant="outline"
                onClick={() => navigate(-1)}
                className="w-full"
                disabled={loading}
              >
                Go Back
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
