import { useEffect, useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  CheckCircle, Download, Calendar, MapPin, Users, Phone, 
  Mail, Share2, Star, Smartphone, CreditCard, Clock,
  Receipt, Home, MessageCircle
} from "lucide-react";

interface PaymentSuccessData {
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
  paymentDetails: {
    method: string;
    provider?: string;
    phone?: string;
    transactionId: string;
    timestamp: string;
  };
}

export default function PaymentSuccess() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const paymentData = location.state as PaymentSuccessData;
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    if (!paymentData) {
      navigate('/dashboard');
      return;
    }
  }, [paymentData, navigate]);

  const generateBookingReference = () => {
    return `GH${Date.now().toString().slice(-6)}`;
  };

  const bookingRef = paymentData?.ticketReference || paymentData?.bookingReference || generateBookingReference();
  const isTicket = !!paymentData?.eventName;

  const handleDownloadReceipt = async () => {
    setIsDownloading(true);
    // Simulate download
    setTimeout(() => {
      setIsDownloading(false);
      // In real app, this would generate and download a PDF
      alert('Receipt downloaded successfully!');
    }, 2000);
  };

  const handleShare = () => {
    const isTicket = !!paymentData?.eventName;
    const title = isTicket ? 'Tales and Trails Ghana - Event Ticket Confirmation' : 'Tales and Trails Ghana - Booking Confirmation';
    const text = isTicket
      ? `I just got tickets for ${paymentData?.eventName} by ${paymentData?.artist}! Ticket reference: ${bookingRef}`
      : `I just booked an amazing tour: ${paymentData?.tourName}. Booking reference: ${bookingRef}`;

    if (navigator.share) {
      navigator.share({
        title,
        text,
        url: window.location.href,
      });
    } else {
      // Fallback for browsers that don't support Web Share API
      navigator.clipboard.writeText(text);
      alert(isTicket ? 'Ticket details copied to clipboard!' : 'Booking details copied to clipboard!');
    }
  };

  if (!paymentData) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Session Expired</h2>
            <p className="text-gray-600 mb-6">Please check your dashboard for booking details.</p>
            <Button onClick={() => navigate('/dashboard')} className="bg-ghana-green hover:bg-ghana-green/90">
              Go to Dashboard
            </Button>
          </div>
        </div>
      </Layout>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Layout>
      {/* Success Header */}
      <div className="bg-gradient-to-r from-green-600 to-ghana-green text-white py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center">
              <CheckCircle className="h-12 w-12 text-green-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold mb-4">Payment Successful!</h1>
          <p className="text-xl text-green-100 mb-2">
            Your {isTicket ? 'tickets have' : 'booking has'} been confirmed
          </p>
          <p className="text-green-200">
            {isTicket ? 'Ticket' : 'Booking'} Reference: <span className="font-bold">{bookingRef}</span>
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Booking Details */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-ghana-green" />
                  <span>{isTicket ? 'Ticket Details' : 'Booking Details'}</span>
                </CardTitle>
                <CardDescription>
                  Your {isTicket ? 'event ticket information' : 'tour booking information'}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {isTicket ? paymentData.eventName : paymentData.tourName}
                    </h3>
                    {isTicket && paymentData.artist && (
                      <p className="text-gray-600 mb-2 font-medium">{paymentData.artist}</p>
                    )}
                    <div className="space-y-2 text-sm text-gray-600">
                      <div className="flex items-center space-x-2">
                        <Calendar className="h-4 w-4" />
                        <span>
                          {isTicket
                            ? new Date(paymentData.date!).toLocaleDateString('en-GB', {
                                weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
                              })
                            : 'September 20-22, 2025'
                          }
                        </span>
                      </div>
                      {isTicket ? (
                        <>
                          <div className="flex items-center space-x-2">
                            <Clock className="h-4 w-4" />
                            <span>{paymentData.time}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <MapPin className="h-4 w-4" />
                            <span>{paymentData.venue}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Users className="h-4 w-4" />
                            <span>{paymentData.quantity} × {paymentData.ticketType}</span>
                          </div>
                        </>
                      ) : (
                        <>
                          <div className="flex items-center space-x-2">
                            <Users className="h-4 w-4" />
                            <span>2 Adults, 1 Child</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <MapPin className="h-4 w-4" />
                            <span>Cape Coast, Ghana</span>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                  <Badge className="bg-green-100 text-green-800">
                    Confirmed
                  </Badge>
                </div>

                <Separator />

                {/* What's Next */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">What happens next?</h4>
                  <div className="space-y-3">
                    {isTicket ? (
                      <>
                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">1</span>
                          </div>
                          <div>
                            <p className="font-medium">Digital Tickets Sent</p>
                            <p className="text-sm text-gray-600">Your e-tickets will be sent to {paymentData.customerInfo?.email || 'your email'} within 5 minutes. You can also download them from your dashboard.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">2</span>
                          </div>
                          <div>
                            <p className="font-medium">Event Reminder</p>
                            <p className="text-sm text-gray-600">We'll send you a reminder 24 hours before the event with venue details and entry instructions.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">3</span>
                          </div>
                          <div>
                            <p className="font-medium">Enjoy the Event</p>
                            <p className="text-sm text-gray-600">Show your ticket (digital or printed) at the venue entrance and enjoy an amazing {paymentData.eventDetails?.category?.toLowerCase() || 'event'}!</p>
                          </div>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">1</span>
                          </div>
                          <div>
                            <p className="font-medium">Confirmation Email</p>
                            <p className="text-sm text-gray-600">You'll receive a detailed email with your booking confirmation and tour itinerary within 5 minutes.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">2</span>
                          </div>
                          <div>
                            <p className="font-medium">Pre-Tour Contact</p>
                            <p className="text-sm text-gray-600">Our team will contact you 48 hours before your tour with final details and meeting instructions.</p>
                          </div>
                        </div>

                        <div className="flex items-start space-x-3">
                          <div className="w-6 h-6 bg-ghana-green rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-white text-xs font-bold">3</span>
                          </div>
                          <div>
                            <p className="font-medium">Enjoy Your Tour</p>
                            <p className="text-sm text-gray-600">Meet your guide at the specified location and enjoy your amazing Ghana experience!</p>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                </div>

                {/* Contact Information */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-3">Need Help?</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <Phone className="h-4 w-4 text-ghana-green" />
                      <span>+233 24 123 4567</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Mail className="h-4 w-4 text-ghana-green" />
                      <span>support@talesandtrails.gh</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Payment Receipt */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Receipt className="h-5 w-5 text-ghana-green" />
                  <span>Payment Receipt</span>
                </CardTitle>
                <CardDescription>Transaction details and receipt</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-600">Transaction ID</p>
                      <p className="font-mono text-sm font-medium">{paymentData.paymentDetails.transactionId}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Payment Method</p>
                      <div className="flex items-center space-x-2">
                        {paymentData.paymentDetails.method === 'Mobile Money' ? (
                          <Smartphone className="h-4 w-4 text-ghana-green" />
                        ) : (
                          <CreditCard className="h-4 w-4 text-ghana-green" />
                        )}
                        <span className="font-medium">{paymentData.paymentDetails.method}</span>
                        {paymentData.paymentDetails.provider && (
                          <Badge variant="outline" className="text-xs">
                            {paymentData.paymentDetails.provider}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-600">Amount Paid</p>
                      <p className="text-xl font-bold text-ghana-green">GH₵{paymentData.total.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Payment Date</p>
                      <div className="flex items-center space-x-2">
                        <Clock className="h-4 w-4 text-gray-400" />
                        <span className="font-medium">{formatDate(paymentData.paymentDetails.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <Separator />

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Status</span>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="font-medium text-green-600">Payment Successful</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Action Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  onClick={handleDownloadReceipt}
                  disabled={isDownloading}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90"
                >
                  <Download className="h-4 w-4 mr-2" />
                  {isDownloading ? 'Downloading...' : 'Download Receipt'}
                </Button>
                
                <Button 
                  onClick={handleShare}
                  variant="outline"
                  className="w-full"
                >
                  <Share2 className="h-4 w-4 mr-2" />
                  Share Booking
                </Button>
                
                <Button 
                  asChild
                  variant="outline"
                  className="w-full"
                >
                  <Link to="/dashboard">
                    <Home className="h-4 w-4 mr-2" />
                    View Dashboard
                  </Link>
                </Button>
              </CardContent>
            </Card>

            {/* Important Notes */}
            <Card>
              <CardHeader>
                <CardTitle>Important Notes</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Free cancellation up to 24 hours before tour</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Please arrive 15 minutes before departure time</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Bring valid ID and comfortable walking shoes</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p>Weather updates will be provided if needed</p>
                </div>
              </CardContent>
            </Card>

            {/* Feedback */}
            <Card>
              <CardHeader>
                <CardTitle>Rate Your Experience</CardTitle>
                <CardDescription>Help us improve our service</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center space-x-1 mb-4">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      className="p-1 hover:scale-110 transition-transform"
                    >
                      <Star className="h-6 w-6 text-yellow-400 fill-current" />
                    </button>
                  ))}
                </div>
                <Button variant="outline" className="w-full">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Leave Feedback
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Related Tours */}
        <div className="mt-12">
          <Card>
            <CardHeader>
              <CardTitle>More Amazing Tours</CardTitle>
              <CardDescription>Discover other incredible destinations in Ghana</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="group cursor-pointer">
                  <div className="relative overflow-hidden rounded-lg mb-3">
                    <img 
                      src="https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=400"
                      alt="Aburi Gardens"
                      className="w-full h-32 object-cover group-hover:scale-105 transition-transform"
                    />
                    <Badge className="absolute top-2 left-2 bg-ghana-gold text-black">
                      Nature
                    </Badge>
                  </div>
                  <h4 className="font-medium group-hover:text-ghana-green">Aburi Gardens Nature Escape</h4>
                  <p className="text-sm text-gray-600">From GH₵280</p>
                </div>
                
                <div className="group cursor-pointer">
                  <div className="relative overflow-hidden rounded-lg mb-3">
                    <img 
                      src="https://images.pexels.com/photos/1054655/pexels-photo-1054655.jpeg?auto=compress&cs=tinysrgb&w=400"
                      alt="Mole National Park"
                      className="w-full h-32 object-cover group-hover:scale-105 transition-transform"
                    />
                    <Badge className="absolute top-2 left-2 bg-ghana-gold text-black">
                      Safari
                    </Badge>
                  </div>
                  <h4 className="font-medium group-hover:text-ghana-green">Mole National Park Safari</h4>
                  <p className="text-sm text-gray-600">From GH₵1,200</p>
                </div>
                
                <div className="group cursor-pointer">
                  <div className="relative overflow-hidden rounded-lg mb-3">
                    <img 
                      src="https://images.pexels.com/photos/5273081/pexels-photo-5273081.jpeg?auto=compress&cs=tinysrgb&w=400"
                      alt="Elmina Castle"
                      className="w-full h-32 object-cover group-hover:scale-105 transition-transform"
                    />
                    <Badge className="absolute top-2 left-2 bg-ghana-gold text-black">
                      Heritage
                    </Badge>
                  </div>
                  <h4 className="font-medium group-hover:text-ghana-green">Elmina Castle Tour</h4>
                  <p className="text-sm text-gray-600">From GH₵400</p>
                </div>
              </div>
              
              <div className="text-center mt-6">
                <Button asChild variant="outline">
                  <Link to="/destinations">
                    View All Tours
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
