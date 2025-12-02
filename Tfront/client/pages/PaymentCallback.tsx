import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Layout from "@/components/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle, XCircle } from "lucide-react";
import { apiClient } from "@/lib/api";

export default function PaymentCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const reference = searchParams.get('reference');
  
  const [status, setStatus] = useState<'verifying' | 'success' | 'failed'>('verifying');
  const [message, setMessage] = useState('Verifying your payment...');
  const [paymentData, setPaymentData] = useState<any>(null);

  useEffect(() => {
    if (!reference) {
      setStatus('failed');
      setMessage('No payment reference found');
      return;
    }

    const verifyPayment = async () => {
      try {
        // Verify payment with Paystack
        const verifyResponse = await apiClient.verifyPaystack(reference);
        
        if (verifyResponse.success) {
          // Get full payment details
          const payment = await apiClient.getPaymentStatus(reference);
          setPaymentData(payment);
          
          if (payment.status === 'successful') {
            setStatus('success');
            setMessage('Payment completed successfully!');
            
            // Redirect to success page after 2 seconds
            setTimeout(() => {
              navigate('/payment-success', {
                state: {
                  reference: payment.reference,
                  amount: payment.amount,
                  paymentMethod: payment.payment_method_display,
                  tourName: payment.metadata?.booking_details?.destination?.name || 'Tour Package'
                }
              });
            }, 2000);
          } else if (payment.status === 'failed') {
            setStatus('failed');
            setMessage('Payment verification failed. Please try again.');
          } else {
            setStatus('failed');
            setMessage('Payment status unclear. Please contact support.');
          }
        } else {
          setStatus('failed');
          setMessage(verifyResponse.error || 'Payment verification failed');
        }
      } catch (error: any) {
        console.error('Payment verification error:', error);
        setStatus('failed');
        setMessage(error.message || 'An error occurred while verifying your payment');
      }
    };

    verifyPayment();
  }, [reference, navigate]);

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-center">
                {status === 'verifying' && 'Verifying Payment'}
                {status === 'success' && 'Payment Successful'}
                {status === 'failed' && 'Payment Failed'}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Status Icon */}
              <div className="flex justify-center">
                {status === 'verifying' && (
                  <Loader2 className="h-16 w-16 text-ghana-green animate-spin" />
                )}
                {status === 'success' && (
                  <CheckCircle className="h-16 w-16 text-green-600" />
                )}
                {status === 'failed' && (
                  <XCircle className="h-16 w-16 text-red-600" />
                )}
              </div>

              {/* Message */}
              <div className="text-center">
                <p className="text-lg font-medium text-gray-900">{message}</p>
                {status === 'verifying' && (
                  <p className="text-sm text-gray-600 mt-2">
                    Please wait while we confirm your payment with Paystack...
                  </p>
                )}
                {status === 'success' && (
                  <p className="text-sm text-gray-600 mt-2">
                    Redirecting to confirmation page...
                  </p>
                )}
              </div>

              {/* Payment Details */}
              {paymentData && (
                <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Reference:</span>
                    <span className="font-mono text-sm">{paymentData.reference}</span>
                  </div>
                  <div className="flex justify-between text-lg font-bold">
                    <span>Amount:</span>
                    <span className="text-ghana-green">
                      {paymentData.currency} {parseFloat(paymentData.amount).toLocaleString()}
                    </span>
                  </div>
                </div>
              )}

              {/* Actions for failed payments */}
              {status === 'failed' && (
                <div className="space-y-3">
                  <Button
                    onClick={() => navigate('/destinations')}
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                  >
                    Browse Tours
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => navigate('/')}
                    className="w-full"
                  >
                    Back to Home
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
