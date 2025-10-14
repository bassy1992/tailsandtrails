import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  CheckCircle, Download, Mail, Calendar, MapPin, Clock, Users, 
  Ticket, ArrowRight, Smartphone, Copy, ExternalLink
} from "lucide-react";

interface TicketPurchase {
  purchase_id: string;
  ticket: {
    title: string;
    venue: {
      name: string;
      address: string;
    };
    event_date: string;
    price: string;
  };
  quantity: number;
  total_amount: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  status: string;
  payment_status: string;
  created_at: string;
}

interface PaymentDetails {
  method: string;
  provider: string;
  phone: string;
  accountName: string;
}

export default function TicketPurchaseSuccess() {
  const location = useLocation();
  const navigate = useNavigate();
  const [purchase, setPurchase] = useState<TicketPurchase | null>(null);
  const [paymentReference, setPaymentReference] = useState<string>('');
  const [paymentDetails, setPaymentDetails] = useState<PaymentDetails | null>(null);
  const [ticketCodes, setTicketCodes] = useState<string[]>([]);
  const [copied, setCopied] = useState<string | null>(null);

  useEffect(() => {
    // Get purchase data from navigation state
    if (location.state?.purchase) {
      setPurchase(location.state.purchase);
      setPaymentReference(location.state.paymentReference || '');
      setPaymentDetails(location.state.paymentDetails || null);
      
      // Fetch ticket codes
      fetchTicketCodes(location.state.purchase.purchase_id);
    } else {
      // No purchase data, redirect to tickets
      navigate('/tickets');
    }
  }, [location.state, navigate]);

  const fetchTicketCodes = async (purchaseId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/tickets/purchase/${purchaseId}/details/`);
      if (response.ok) {
        const data = await response.json();
        if (data.success && data.ticket_codes) {
          setTicketCodes(data.ticket_codes.map((code: any) => code.code));
        }
      }
    } catch (error) {
      console.error('Error fetching ticket codes:', error);
    }
  };

  const copyToClipboard = (text: string, type: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(type);
      setTimeout(() => setCopied(null), 2000);
    });
  };

  const handleDownloadTickets = () => {
    // TODO: Implement ticket download functionality
    alert('Ticket download functionality will be implemented soon!');
  };

  const handleEmailTickets = () => {
    // TODO: Implement email tickets functionality
    alert('Tickets will be sent to your email address shortly!');
  };

  if (!purchase) {
    return (
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
          <div className="text-center">
            <p>Loading purchase details...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8">
        <div className="max-w-4xl mx-auto px-4">
          {/* Success Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-6">
              <CheckCircle className="w-10 h-10 text-green-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Payment Successful!</h1>
            <p className="text-xl text-gray-600">Your tickets have been confirmed and are ready for use</p>
            
            {paymentReference && (
              <div className="mt-4">
                <Badge variant="outline" className="text-lg px-4 py-2">
                  Ticket Reference: {paymentReference}
                </Badge>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Purchase Details */}
            <div className="lg:col-span-2 space-y-6">
              {/* Ticket Details */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Ticket className="w-5 h-5" />
                    Ticket Details
                  </CardTitle>
                  <CardDescription>
                    Your event tickets are confirmed and ready
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">{purchase.ticket.title}</h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-3">
                        <div className="flex items-center gap-3 text-gray-600">
                          <MapPin className="w-5 h-5" />
                          <div>
                            <p className="font-medium">{purchase.ticket.venue?.name || 'Venue TBA'}</p>
                            {purchase.ticket.venue?.address && (
                              <p className="text-sm text-gray-500">{purchase.ticket.venue.address}</p>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center gap-3 text-gray-600">
                          <Calendar className="w-5 h-5" />
                          <div>
                            <p className="font-medium">{new Date(purchase.ticket.event_date).toLocaleDateString('en-US', {
                              weekday: 'long',
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric'
                            })}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 text-gray-600">
                          <Clock className="w-5 h-5" />
                          <div>
                            <p className="font-medium">{new Date(purchase.ticket.event_date).toLocaleTimeString('en-US', {
                              hour: '2-digit',
                              minute: '2-digit'
                            })}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center gap-3 text-gray-600">
                          <Users className="w-5 h-5" />
                          <div>
                            <p className="font-medium">{purchase.quantity} ticket{purchase.quantity > 1 ? 's' : ''}</p>
                            <p className="text-sm text-gray-500">GH₵{purchase.ticket.price} each</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          <Badge className="bg-green-100 text-green-800 px-3 py-1">
                            {purchase.status.charAt(0).toUpperCase() + purchase.status.slice(1)}
                          </Badge>
                        </div>
                        {paymentDetails && (
                          <div className="flex items-center gap-3 text-gray-600">
                            <Smartphone className="w-5 h-5" />
                            <div>
                              <p className="font-medium">{paymentDetails.provider} Mobile Money</p>
                              <p className="text-sm text-gray-500">{paymentDetails.phone}</p>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {ticketCodes.length > 0 && (
                    <>
                      <Separator />
                      <div>
                        <h4 className="font-semibold text-lg mb-3 flex items-center gap-2">
                          <Ticket className="w-5 h-5" />
                          Your Ticket Codes
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {ticketCodes.map((code, index) => (
                            <div key={index} className="bg-gray-50 p-4 rounded-lg border">
                              <div className="flex items-center justify-between">
                                <div>
                                  <p className="font-mono text-lg font-semibold">{code}</p>
                                  <p className="text-sm text-gray-500">Ticket {index + 1}</p>
                                </div>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => copyToClipboard(code, `code-${index}`)}
                                  className="h-8 w-8 p-0"
                                >
                                  {copied === `code-${index}` ? (
                                    <CheckCircle className="w-4 h-4 text-green-600" />
                                  ) : (
                                    <Copy className="w-4 h-4" />
                                  )}
                                </Button>
                              </div>
                            </div>
                          ))}
                        </div>
                        <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                          <p className="text-sm text-blue-800">
                            <strong>Important:</strong> Present these codes at the venue for entry. 
                            Keep them safe and don't share with others.
                          </p>
                        </div>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>

              {/* Customer Information */}
              <Card>
                <CardHeader>
                  <CardTitle>Customer Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-sm text-gray-600">Name</p>
                      <p className="font-medium text-lg">{purchase.customer_name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Email</p>
                      <p className="font-medium">{purchase.customer_email}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Phone</p>
                      <p className="font-medium">{purchase.customer_phone}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Purchase Date</p>
                      <p className="font-medium">{new Date(purchase.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Actions & Summary */}
            <div className="lg:col-span-1">
              <Card className="sticky top-8">
                <CardHeader>
                  <CardTitle>Purchase Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span>Purchase ID</span>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs">{purchase.purchase_id.slice(0, 8)}...</span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(purchase.purchase_id, 'purchase-id')}
                          className="h-6 w-6 p-0"
                        >
                          {copied === 'purchase-id' ? (
                            <CheckCircle className="w-3 h-3 text-green-600" />
                          ) : (
                            <Copy className="w-3 h-3" />
                          )}
                        </Button>
                      </div>
                    </div>
                    {paymentReference && (
                      <div className="flex justify-between text-sm">
                        <span>Payment Ref</span>
                        <span className="font-mono text-xs">{paymentReference}</span>
                      </div>
                    )}
                    <div className="flex justify-between text-sm">
                      <span>Quantity</span>
                      <span>{purchase.quantity}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Unit Price</span>
                      <span>GH₵ {purchase.ticket.price}</span>
                    </div>
                  </div>

                  <Separator />

                  <div className="flex justify-between font-semibold text-xl">
                    <span>Total Paid</span>
                    <span className="text-green-600">GH₵ {purchase.total_amount}</span>
                  </div>

                  <Separator />

                  <div className="space-y-3">
                    <Button 
                      onClick={handleDownloadTickets}
                      className="w-full bg-green-600 hover:bg-green-700"
                      size="lg"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download Tickets
                    </Button>
                    
                    <Button 
                      onClick={handleEmailTickets}
                      variant="outline"
                      className="w-full"
                      size="lg"
                    >
                      <Mail className="w-4 h-4 mr-2" />
                      Email Tickets
                    </Button>
                    
                    <Button 
                      onClick={() => navigate('/tickets')}
                      variant="outline"
                      className="w-full"
                      size="lg"
                    >
                      Browse More Events
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </div>

                  <div className="text-xs text-gray-500 text-center space-y-2">
                    <p className="flex items-center justify-center gap-1">
                      <Mail className="w-3 h-3" />
                      Confirmation email sent to {purchase.customer_email}
                    </p>
                    <p className="flex items-center justify-center gap-1">
                      <Ticket className="w-3 h-3" />
                      Keep your ticket codes safe for entry
                    </p>
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