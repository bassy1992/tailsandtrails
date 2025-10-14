import React from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Smartphone, MapPin, Calendar, Users } from 'lucide-react';

export default function TestMainCheckout() {
  const navigate = useNavigate();

  const testTourBooking = () => {
    // Simulate tour booking data
    const tourPaymentData = {
      tourName: 'Cape Coast Castle Tour',
      bookingReference: `TOUR_${Date.now()}`,
      total: 450.0,
      paymentMethod: 'mobile_money',
      bookingDetails: {
        destination: 'Cape Coast Castle',
        participants: 2,
        date: '2024-11-15',
        duration: '2 Days, 1 Night'
      },
      customerInfo: {
        name: 'Test Customer',
        email: 'test@example.com',
        phone: '0244123456'
      }
    };

    // Navigate to momo checkout with data
    navigate('/momo-checkout', { state: tourPaymentData });
  };

  const testTicketPurchase = () => {
    // Simulate ticket purchase data
    const ticketPurchaseData = {
      type: 'ticket',
      ticketId: 1,
      ticketTitle: 'Afrobeats Night Live Concert',
      venue: 'National Theatre of Ghana',
      eventDate: '2024-11-20T19:00:00Z',
      quantity: 2,
      unitPrice: 150.0,
      totalAmount: 300.0,
      customerInfo: {
        name: 'Test Customer',
        email: 'test@example.com',
        phone: '0244123456'
      }
    };

    // Store in localStorage and navigate to ticket checkout
    localStorage.setItem('pendingTicketPurchase', JSON.stringify(ticketPurchaseData));
    navigate('/ticket-checkout');
  };

  const testFromBookingPage = () => {
    // Navigate to booking page to test the full flow
    navigate('/booking/1');
  };

  const testFromTicketsPage = () => {
    // Navigate to tickets page to test the full flow
    navigate('/tickets');
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-ghana-green mb-2">
              Test Main Checkout Flow
            </h1>
            <p className="text-gray-600">
              Test the main checkout pages with sample data
            </p>
          </div>

          <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Tour Booking Test */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-ghana-green" />
                  Tour Booking Checkout
                </CardTitle>
                <CardDescription>
                  Test the tour booking → mobile money flow
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tour:</span>
                    <span>Cape Coast Castle Tour</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Participants:</span>
                    <span>2 people</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Amount:</span>
                    <span className="font-bold text-ghana-green">GH₵450</span>
                  </div>
                </div>
                
                <Button 
                  onClick={testTourBooking}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90"
                >
                  Test Tour → MoMo Checkout
                </Button>
                
                <Button 
                  onClick={testFromBookingPage}
                  variant="outline"
                  className="w-full"
                >
                  Test Full Booking Flow
                </Button>
              </CardContent>
            </Card>

            {/* Ticket Purchase Test */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-ghana-green" />
                  Ticket Purchase Checkout
                </CardTitle>
                <CardDescription>
                  Test the ticket purchase → mobile money flow
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Event:</span>
                    <span>Afrobeats Concert</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tickets:</span>
                    <span>2 tickets</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Amount:</span>
                    <span className="font-bold text-ghana-green">GH₵300</span>
                  </div>
                </div>
                
                <Button 
                  onClick={testTicketPurchase}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90"
                >
                  Test Ticket → MoMo Checkout
                </Button>
                
                <Button 
                  onClick={testFromTicketsPage}
                  variant="outline"
                  className="w-full"
                >
                  Test Full Ticket Flow
                </Button>
              </CardContent>
            </Card>

            {/* Instructions */}
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-ghana-green" />
                  How to Test Main Checkout
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Option 1: Direct Test (Above Buttons)</h4>
                    <p className="text-sm text-gray-600">
                      Use the buttons above to directly test the checkout pages with sample data.
                    </p>
                  </div>
                  
                  <div>
                    <h4 className="font-medium mb-2">Option 2: Full User Flow</h4>
                    <ol className="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                      <li>Go to <code>/destinations</code> → Select a tour → Click "Book Now"</li>
                      <li>Fill in booking details → Select "Mobile Money" → Click "Proceed"</li>
                      <li>Or go to <code>/tickets</code> → Select event → Click "Book Now"</li>
                      <li>Fill in details → Select "MTN Mobile Money" → Click "Purchase"</li>
                    </ol>
                  </div>
                  
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-medium text-blue-900 mb-2">Common Issues:</h4>
                    <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                      <li>If you go directly to <code>/momo-checkout</code> without data, it will redirect</li>
                      <li>Make sure to follow the proper booking flow</li>
                      <li>Check browser console for any JavaScript errors</li>
                      <li>Ensure both frontend (8080) and backend (8000) servers are running</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}