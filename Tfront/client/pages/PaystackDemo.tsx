import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { CreditCard, Smartphone, Shield } from "lucide-react";

export default function PaystackDemo() {
  const navigate = useNavigate();
  const [amount, setAmount] = useState<string>("50");
  const [email, setEmail] = useState<string>("test@example.com");
  const [name, setName] = useState<string>("John Doe");

  const handleCardPayment = () => {
    const paymentData = {
      total: parseFloat(amount),
      paymentMethod: 'card',
      tourName: 'Paystack Demo - Card Payment',
      bookingReference: `DEMO_CARD_${Date.now()}`,
      customerInfo: {
        email: email,
        name: name
      }
    };

    navigate('/paystack-checkout', { state: paymentData });
  };

  const handleMomoPayment = () => {
    const paymentData = {
      total: parseFloat(amount),
      paymentMethod: 'mobile_money',
      tourName: 'Paystack Demo - Mobile Money',
      bookingReference: `DEMO_MOMO_${Date.now()}`,
      customerInfo: {
        email: email,
        name: name
      }
    };

    navigate('/momo-checkout', { state: paymentData });
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Paystack Ghana Demo
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Test both card and mobile money payments powered by Paystack Ghana
            </p>
            <Badge className="mt-4 bg-green-100 text-green-800 px-4 py-2">
              Test Mode - Safe to Use
            </Badge>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Demo Form */}
            <Card>
              <CardHeader>
                <CardTitle>Payment Demo</CardTitle>
                <CardDescription>
                  Enter test details to try Paystack integration
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                
                {/* Amount */}
                <div className="space-y-2">
                  <Label htmlFor="amount">Amount (GH₵)</Label>
                  <Input
                    id="amount"
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="50.00"
                    min="1"
                    step="0.01"
                  />
                </div>

                {/* Email */}
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="test@example.com"
                  />
                </div>

                {/* Name */}
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="John Doe"
                  />
                </div>

                <Separator />

                {/* Payment Buttons */}
                <div className="space-y-4">
                  <Button 
                    onClick={handleCardPayment}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3"
                    disabled={!amount || !email || !name}
                  >
                    <CreditCard className="h-4 w-4 mr-2" />
                    Pay with Card (GH₵{amount})
                  </Button>

                  <Button 
                    onClick={handleMomoPayment}
                    className="w-full bg-green-600 hover:bg-green-700 text-white py-3"
                    disabled={!amount || !email || !name}
                  >
                    <Smartphone className="h-4 w-4 mr-2" />
                    Pay with Mobile Money (GH₵{amount})
                  </Button>
                </div>

                {/* Security Notice */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <Shield className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <h4 className="font-medium text-blue-900">Test Mode</h4>
                      <p className="text-sm text-blue-700 mt-1">
                        This is a demo using Paystack test keys. No real money will be charged.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Information Panel */}
            <div className="space-y-6">
              
              {/* Card Payment Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CreditCard className="h-5 w-5 text-blue-600" />
                    <span>Card Payments</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium">Test Card Numbers:</h4>
                      <div className="text-sm text-gray-600 space-y-1 mt-2">
                        <div>Success: <code className="bg-gray-100 px-2 py-1 rounded">4084084084084081</code></div>
                        <div>Decline: <code className="bg-gray-100 px-2 py-1 rounded">4084084084084099</code></div>
                        <div>Insufficient: <code className="bg-gray-100 px-2 py-1 rounded">4084084084084107</code></div>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium">Supported Cards:</h4>
                      <p className="text-sm text-gray-600">Visa, Mastercard, Verve</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Mobile Money Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Smartphone className="h-5 w-5 text-green-600" />
                    <span>Mobile Money</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium">Supported Providers:</h4>
                      <div className="space-y-2 mt-2">
                        <div className="flex items-center space-x-2">
                          <div className="w-4 h-4 bg-yellow-400 rounded-full"></div>
                          <span className="text-sm">MTN Mobile Money</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-4 h-4 bg-red-600 rounded-full"></div>
                          <span className="text-sm">Vodafone Cash</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-4 h-4 bg-blue-600 rounded-full"></div>
                          <span className="text-sm">AirtelTigo Money</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium">Test Numbers:</h4>
                      <p className="text-sm text-gray-600">Use any valid Ghana mobile number in test mode</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Features */}
              <Card>
                <CardHeader>
                  <CardTitle>Paystack Features</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>PCI DSS Compliant</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>3D Secure Authentication</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>Real-time Webhooks</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>Mobile Money Integration</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>Instant Settlement</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Back Button */}
          <div className="text-center mt-12">
            <Button 
              variant="outline" 
              onClick={() => navigate('/destinations')}
              className="px-8"
            >
              Back to Tours
            </Button>
          </div>
        </div>
      </div>
    </Layout>
  );
}