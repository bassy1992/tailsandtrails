import { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import Layout from "@/components/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle, XCircle, Smartphone } from "lucide-react";
import { apiClient } from "@/lib/api";

export default function PaymentProcessing() {
  const { reference } = useParams<{ reference: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { tourName, amount, paymentMethod } = location.state || {};
  
  const [status, setStatus] = useState<'processing' | 'successful' | 'failed'>('processing');
  const [message, setMessage] = useState('Processing your payment...');
  const [pollingCount, setPollingCount] = useState(0);

  useEffect(() => {
    if (!reference) {
      navigate('/');
      return;
    }

    let pollInterval: NodeJS.Timeout;
    let timeoutTimer: NodeJS.Timeout;

    const checkPaymentStatus = async () => {
      try {
        const payment = await apiClient.getPaymentStatus(reference);
        
        setPollingCount(prev => prev + 1);

        if (payment.status === 'successful') {
          setStatus('successful');
          setMessage('Payment completed successfully!');
          clearInterval(pollInterval);
          clearTimeout(timeoutTimer);
          
          // Redirect to success page after 2 seconds
          setTimeout(() => {
            navigate('/payment-success', {
              state: {
                reference: payment.reference,
                tourName: tourName,
                total: parseFloat(payment.amount),
                amount: parseFloat(payment.amount),
                paymentMethod: payment.payment_method_display,
                bookingReference: payment.reference,
                paymentDetails: {
                  method: payment.payment_method_display || 'Mobile Money',
                  provider: 'Paystack',
                  transactionId: payment.reference,
                  timestamp: new Date().toISOString()
                }
              }
            });
          }, 2000);
        } else if (payment.status === 'failed' || payment.status === 'cancelled') {
          setStatus('failed');
          setMessage(payment.status === 'cancelled' ? 'Payment was cancelled' : 'Payment failed');
          clearInterval(pollInterval);
          clearTimeout(timeoutTimer);
        } else if (payment.status === 'processing' || payment.status === 'pending') {
          setMessage('Waiting for payment authorization...');
        }
      } catch (error) {
        console.error('Error checking payment status:', error);
      }
    };

    // Initial check
    checkPaymentStatus();

    // Poll every 2 seconds
    pollInterval = setInterval(checkPaymentStatus, 2000);

    // Timeout after 5 minutes
    timeoutTimer = setTimeout(() => {
      clearInterval(pollInterval);
      if (status === 'processing') {
        setStatus('failed');
        setMessage('Payment timeout. Please try again or contact support.');
      }
    }, 300000); // 5 minutes

    return () => {
      clearInterval(pollInterval);
      clearTimeout(timeoutTimer);
    };
  }, [reference, navigate, tourName, amount, status]);

  if (!reference) {
    return null;
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-center">
                {status === 'processing' && 'Processing Payment'}
                {status === 'successful' && 'Payment Successful'}
                {status === 'failed' && 'Payment Failed'}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Status Icon */}
              <div className="flex justify-center">
                {status === 'processing' && (
                  <div className="text-center">
                    <Loader2 className="h-16 w-16 text-ghana-green animate-spin mx-auto mb-4" />
                    <Smartphone className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">Check your phone for authorization prompt</p>
                  </div>
                )}
                {status === 'successful' && (
                  <CheckCircle className="h-16 w-16 text-green-600" />
                )}
                {status === 'failed' && (
                  <XCircle className="h-16 w-16 text-red-600" />
                )}
              </div>

              {/* Message */}
              <div className="text-center">
                <p className="text-lg font-medium text-gray-900">{message}</p>
                {status === 'processing' && (
                  <p className="text-sm text-gray-600 mt-2">
                    This may take a few moments. Please don't close this page.
                  </p>
                )}
              </div>

              {/* Booking Details */}
              {tourName && (
                <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tour:</span>
                    <span className="font-semibold">{tourName}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Payment Method:</span>
                    <span className="font-semibold">{paymentMethod || 'Mobile Money'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Reference:</span>
                    <span className="font-mono text-sm">{reference}</span>
                  </div>
                  <div className="flex justify-between text-lg font-bold">
                    <span>Amount:</span>
                    <span className="text-ghana-green">GH₵{amount?.toLocaleString()}</span>
                  </div>
                </div>
              )}

              {/* Actions */}
              {status === 'failed' && (
                <div className="space-y-3">
                  <Button
                    onClick={() => navigate(-1)}
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                  >
                    Try Again
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

              {/* Debug Info (only in processing state) */}
              {status === 'processing' && pollingCount > 0 && (
                <div className="text-center text-xs text-gray-400">
                  Checking status... ({pollingCount})
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
