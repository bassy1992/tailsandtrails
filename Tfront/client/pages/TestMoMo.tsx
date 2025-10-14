import React, { useState } from 'react';
import Layout from '../components/Layout';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Badge } from '../components/ui/badge';
import { Separator } from '../components/ui/separator';
import { 
  Smartphone, CheckCircle, AlertCircle, Loader2, 
  Phone, User, CreditCard, ArrowRight 
} from 'lucide-react';

export default function TestMoMo() {
  const [amount, setAmount] = useState('50');
  const [email, setEmail] = useState('test@example.com');
  const [phone, setPhone] = useState('0244123456');
  const [provider, setProvider] = useState('mtn');
  const [accountName, setAccountName] = useState('Test User');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [step, setStep] = useState<'form' | 'processing' | 'result'>('form');

  const handleTest = async () => {
    setIsProcessing(true);
    setStep('processing');
    setResult(null);

    try {
      // Step 1: Create payment
      const response = await fetch('http://localhost:8000/api/payments/paystack/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: parseFloat(amount),
          email: email,
          payment_method: 'mobile_money',
          provider: provider,
          phone_number: phone,
          description: `Test MTN MoMo Payment - GH₵${amount}`
        })
      });

      const paymentResult = await response.json();
      
      if (paymentResult.success) {
        const paymentRef = paymentResult.payment.reference;
        
        // Step 2: Simulate waiting for authorization
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Step 3: Complete payment (simulate user authorization)
        const completeResponse = await fetch(`http://localhost:8000/api/payments/${paymentRef}/complete/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            status: 'successful'
          })
        });

        const completeResult = await completeResponse.json();
        
        setResult({
          success: true,
          payment: completeResult.payment || paymentResult.payment,
          paystack: paymentResult.paystack,
          message: 'Payment completed successfully!'
        });
      } else {
        setResult({
          success: false,
          error: paymentResult.error || 'Payment failed'
        });
      }
    } catch (error) {
      setResult({
        success: false,
        error: `Network error: ${error}`
      });
    } finally {
      setIsProcessing(false);
      setStep('result');
    }
  };

  const resetTest = () => {
    setStep('form');
    setResult(null);
    setIsProcessing(false);
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-ghana-green mb-2">
              MTN MoMo Integration Test
            </h1>
            <p className="text-gray-600">
              Test the MTN Mobile Money integration with Paystack
            </p>
            <Badge className="mt-2 bg-blue-100 text-blue-800">
              Test Mode - Safe to Use
            </Badge>
          </div>

          <div className="max-w-2xl mx-auto">
            {/* Test Form */}
            {step === 'form' && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Smartphone className="w-5 h-5 text-ghana-green" />
                    Test Payment Details
                  </CardTitle>
                  <CardDescription>
                    Enter test details to verify MTN MoMo integration
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Amount */}
                  <div className="space-y-2">
                    <Label htmlFor="amount">Amount (GH₵)</Label>
                    <div className="relative">
                      <CreditCard className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <Input
                        id="amount"
                        type="number"
                        placeholder="50"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="pl-10"
                        min="1"
                        max="1000"
                      />
                    </div>
                  </div>

                  {/* Email */}
                  <div className="space-y-2">
                    <Label htmlFor="email">Email Address</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="test@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>

                  {/* Provider Selection */}
                  <div className="space-y-3">
                    <Label>Mobile Money Provider</Label>
                    <RadioGroup value={provider} onValueChange={setProvider} className="space-y-3">
                      <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="mtn" id="mtn" />
                        <Label htmlFor="mtn" className="flex-1 cursor-pointer">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center">
                              <span className="text-xs font-bold text-black">MTN</span>
                            </div>
                            <div>
                              <p className="font-medium">MTN Mobile Money</p>
                              <p className="text-sm text-gray-600">*170#</p>
                            </div>
                          </div>
                        </Label>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50">
                        <RadioGroupItem value="vodafone" id="vodafone" />
                        <Label htmlFor="vodafone" className="flex-1 cursor-pointer">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
                              <span className="text-xs font-bold text-white">VF</span>
                            </div>
                            <div>
                              <p className="font-medium">Vodafone Cash</p>
                              <p className="text-sm text-gray-600">*110#</p>
                            </div>
                          </div>
                        </Label>
                      </div>
                    </RadioGroup>
                  </div>

                  {/* Phone Number */}
                  <div className="space-y-2">
                    <Label htmlFor="phone">Mobile Money Number</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <Input
                        id="phone"
                        type="tel"
                        placeholder="0244123456"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>

                  {/* Account Name */}
                  <div className="space-y-2">
                    <Label htmlFor="accountName">Account Holder Name</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <Input
                        id="accountName"
                        type="text"
                        placeholder="Test User"
                        value={accountName}
                        onChange={(e) => setAccountName(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>

                  <Separator />

                  {/* Test Button */}
                  <Button 
                    onClick={handleTest}
                    disabled={!amount || !email || !phone || !provider || !accountName}
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white py-3"
                    size="lg"
                  >
                    <ArrowRight className="h-4 w-4 mr-2" />
                    Test MTN MoMo Payment (GH₵{amount})
                  </Button>

                  {/* Info */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="font-medium text-blue-900">Test Mode</h4>
                        <p className="text-sm text-blue-700 mt-1">
                          This is a safe test that won't charge any real money. 
                          It tests the integration with Paystack's test environment.
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Processing */}
            {step === 'processing' && (
              <Card>
                <CardContent className="py-12 text-center">
                  <div className="flex flex-col items-center space-y-6">
                    <div className="relative">
                      <div className="w-20 h-20 bg-ghana-green/10 rounded-full flex items-center justify-center">
                        <Loader2 className="h-10 w-10 text-ghana-green animate-spin" />
                      </div>
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        Testing MTN MoMo Integration
                      </h3>
                      <p className="text-gray-600">
                        Creating payment and simulating authorization...
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Results */}
            {step === 'result' && result && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {result.success ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <AlertCircle className="w-5 h-5 text-red-600" />
                    )}
                    Test Results
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {result.success ? (
                    <div className="space-y-4">
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                        <div className="flex items-center space-x-2">
                          <CheckCircle className="h-5 w-5 text-green-600" />
                          <span className="font-medium text-green-800">
                            MTN MoMo Integration Working!
                          </span>
                        </div>
                        <p className="text-sm text-green-700 mt-1">
                          {result.message}
                        </p>
                      </div>

                      {/* Payment Details */}
                      <div className="space-y-3">
                        <h4 className="font-medium">Payment Details:</h4>
                        <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Reference:</span>
                            <span className="font-mono">{result.payment?.reference}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Amount:</span>
                            <span>GH₵{result.payment?.amount}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Status:</span>
                            <Badge className="bg-green-100 text-green-800">
                              {result.payment?.status}
                            </Badge>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Provider:</span>
                            <span className="capitalize">{provider} Mobile Money</span>
                          </div>
                        </div>
                      </div>

                      {/* Paystack Info */}
                      {result.paystack && (
                        <div className="space-y-3">
                          <h4 className="font-medium">Paystack Response:</h4>
                          <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                            {result.paystack.test_mode && (
                              <div className="flex justify-between">
                                <span className="text-gray-600">Test Mode:</span>
                                <Badge className="bg-blue-100 text-blue-800">Active</Badge>
                              </div>
                            )}
                            <div className="flex justify-between">
                              <span className="text-gray-600">Display Text:</span>
                              <span className="text-right max-w-xs">
                                {result.paystack.display_text}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2">
                        <AlertCircle className="h-5 w-5 text-red-600" />
                        <span className="font-medium text-red-800">Test Failed</span>
                      </div>
                      <p className="text-sm text-red-700 mt-1">
                        {result.error}
                      </p>
                    </div>
                  )}

                  <Button 
                    onClick={resetTest}
                    variant="outline"
                    className="w-full"
                  >
                    Run Another Test
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}