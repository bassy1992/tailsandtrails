import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Layout from "@/components/Layout";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

export default function PaymentCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<'verifying' | 'success' | 'failed'>('verifying');
  const [message, setMessage] = useState('Verifying your payment...');

  useEffect(() => {
    const verifyPayment = async () => {
      try {
        const reference = searchParams.get('reference');
        const trxref = searchParams.get('trxref');
        
        // Use reference from URL params or session storage
        const paymentRef = reference || trxref || sessionStorage.getItem('paymentReference');
        
        if (!paymentRef) {
          setStatus('failed');
          setMessage('Payment reference not found');
          return;
        }

        // Verify payment with backend
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/payments/paystack/verify/${paymentRef}/`);
        const result = await response.json();

        if (result.success && result.payment) {
          const payment = result.payment;
          
          if (payment.status === 'successful') {
            setStatus('success');
            setMessage('Payment completed successfully!');
            
            // Clear stored reference
            sessionStorage.removeItem('paymentReference');
            
            // Handle ticket purchase completion
            setTimeout(async () => {
              // Check if this is a ticket purchase
              const ticketPurchaseData = localStorage.getItem('pendingTicketPurchase');
              
              if (ticketPurchaseData) {
                try {
                  const purchaseData = JSON.parse(ticketPurchaseData);
                  
                  // Create the ticket purchase after successful payment
                  const ticketResponse = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/tickets/purchase/direct/`, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                      ticket_id: purchaseData.ticketId,
                      quantity: purchaseData.quantity,
                      total_amount: purchaseData.totalAmount,
                      customer_name: purchaseData.customerInfo?.name || 'Customer',
                      customer_email: purchaseData.customerInfo?.email || '',
                      customer_phone: purchaseData.customerInfo?.phone || '',
                      payment_method: 'paystack_momo',
                      payment_reference: paymentRef,
                      special_requests: `Paystack Mobile Money Payment - ${paymentRef}`
                    })
                  });

                  const ticketResult = await ticketResponse.json();

                  if (ticketResult.success) {
                    // Clear the stored data
                    localStorage.removeItem('pendingTicketPurchase');
                    localStorage.removeItem('pendingPaymentReference');

                    // Navigate to ticket purchase success page
                    navigate('/ticket-purchase-success', {
                      state: {
                        purchase: ticketResult.purchase,
                        paymentReference: paymentRef,
                        paymentDetails: {
                          method: 'Mobile Money',
                          provider: 'Paystack',
                          transactionId: paymentRef,
                          amount: payment.amount,
                          currency: payment.currency
                        }
                      },
                      replace: true
                    });
                    return;
                  } else {
                    console.error('Failed to create ticket purchase:', ticketResult);
                    setStatus('failed');
                    setMessage('Payment successful but failed to create ticket. Please contact support.');
                    return;
                  }
                } catch (error) {
                  console.error('Error processing ticket purchase:', error);
                  setStatus('failed');
                  setMessage('Payment successful but failed to create ticket. Please contact support.');
                  return;
                }
              }
              
              // Handle regular tour booking payments
              const storedPaymentData = sessionStorage.getItem('pendingPaymentData');
              let originalPaymentData = null;
              
              if (storedPaymentData) {
                try {
                  originalPaymentData = JSON.parse(storedPaymentData);
                  sessionStorage.removeItem('pendingPaymentData');
                } catch (e) {
                  console.error('Error parsing stored payment data:', e);
                }
              }
              
              // Determine payment method from payment data
              const paymentMethod = payment.payment_method === 'mobile_money' ? 'Mobile Money' : 'Card Payment';
              
              // Ensure we have the necessary data for the success page
              const successData = {
                ...originalPaymentData, // Restore original booking data
                total: payment.amount || originalPaymentData?.total || 0,
                paymentDetails: {
                  method: paymentMethod,
                  transactionId: paymentRef,
                  status: 'completed',
                  timestamp: payment.processed_at || new Date().toISOString(),
                  gateway: 'Paystack',
                  amount: payment.amount,
                  currency: payment.currency,
                  provider: payment.payment_method === 'mobile_money' ? 'Paystack' : undefined
                }
              };
              
              console.log('Redirecting to payment success with data:', successData);
              
              // Store payment data in localStorage as backup
              localStorage.setItem('completedPaymentData', JSON.stringify(successData));
              
              // Try multiple redirect methods to ensure success page is reached
              try {
                navigate('/payment-success', {
                  state: successData,
                  replace: true
                });
              } catch (error) {
                console.error('Navigation failed, trying URL redirect:', error);
                // Fallback: redirect with URL parameters
                const params = new URLSearchParams({
                  reference: paymentRef,
                  amount: (payment.amount || 0).toString(),
                  method: paymentMethod
                });
                window.location.href = `/payment-success?${params.toString()}`;
              }
            }, 2000);
          } else if (payment.status === 'failed') {
            setStatus('failed');
            setMessage('Payment failed. Please try again.');
            
            setTimeout(() => {
              navigate('/tickets');
            }, 3000);
          } else {
            // Still processing, continue checking
            setTimeout(verifyPayment, 2000);
          }
        } else {
          setStatus('failed');
          setMessage('Unable to verify payment. Please contact support.');
        }
      } catch (error) {
        console.error('Payment verification error:', error);
        setStatus('failed');
        setMessage('An error occurred while verifying your payment.');
      }
    };

    verifyPayment();
  }, [searchParams, navigate]);

  return (
    <Layout>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="py-12 text-center">
            <div className="flex flex-col items-center space-y-6">
              {status === 'verifying' && (
                <>
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                    <Loader2 className="h-8 w-8 text-blue-600 animate-spin" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      Verifying Payment
                    </h3>
                    <p className="text-gray-600">{message}</p>
                  </div>
                </>
              )}
              
              {status === 'success' && (
                <>
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-green-900 mb-2">
                      Payment Successful!
                    </h3>
                    <p className="text-green-700">{message}</p>
                    <p className="text-sm text-gray-600 mt-2">
                      Redirecting to confirmation page...
                    </p>
                  </div>
                </>
              )}
              
              {status === 'failed' && (
                <>
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                    <XCircle className="h-8 w-8 text-red-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-red-900 mb-2">
                      Payment Failed
                    </h3>
                    <p className="text-red-700">{message}</p>
                    <p className="text-sm text-gray-600 mt-2">
                      Redirecting back to tours...
                    </p>
                  </div>
                </>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}