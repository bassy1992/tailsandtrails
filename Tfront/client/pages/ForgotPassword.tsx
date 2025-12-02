import { useState } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Mail, MapPin } from "lucide-react";
import { Link } from "react-router-dom";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      console.log("Password reset requested for:", email);
      setIsLoading(false);
      setIsSubmitted(true);
    }, 2000);
  };

  if (isSubmitted) {
    return (
      <Layout>
        <div className="min-h-[calc(100vh-80px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
            <div className="text-center">
              <div className="flex items-center justify-center space-x-3 mb-4">
                <img
                  src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fbfa2b897e15b4475b41dbeceafc18e1c?format=webp&width=200"
                  alt="Tales and Trails Ghana Logo"
                  className="h-10 w-auto"
                />
                <h2 className="text-3xl font-bold text-gray-900">Check Your Email</h2>
              </div>
            </div>

            <Card className="border-0 shadow-lg">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail className="h-8 w-8 text-ghana-green" />
                </div>
                <CardTitle className="text-xl text-ghana-green">Email Sent!</CardTitle>
                <CardDescription>
                  We've sent password reset instructions to <strong>{email}</strong>
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <p className="text-sm text-gray-600 text-center">
                  Check your email and follow the link to reset your password. 
                  If you don't see the email, check your spam folder.
                </p>
                
                <div className="space-y-3">
                  <Button
                    onClick={() => setIsSubmitted(false)}
                    variant="outline"
                    className="w-full"
                  >
                    Try Different Email
                  </Button>
                  
                  <Link to="/login" className="block">
                    <Button className="w-full bg-ghana-green hover:bg-ghana-green/90">
                      Back to Login
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-[calc(100vh-80px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          {/* Header */}
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <img
                src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fbfa2b897e15b4475b41dbeceafc18e1c?format=webp&width=200"
                alt="Tales and Trails Ghana Logo"
                className="h-10 w-auto"
              />
              <h2 className="text-3xl font-bold text-gray-900">Reset Password</h2>
            </div>
            <p className="text-gray-600">
              Enter your email address and we'll send you a link to reset your password
            </p>
          </div>

          <Card className="border-0 shadow-lg">
            <CardHeader className="space-y-1 pb-6">
              <CardTitle className="text-2xl text-center text-ghana-green">Forgot Password</CardTitle>
              <CardDescription className="text-center">
                No worries, we'll help you get back into your account
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="Enter your email address"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                  disabled={isLoading}
                >
                  {isLoading ? "Sending..." : "Send Reset Link"}
                </Button>
              </form>

              {/* Back to Login */}
              <div className="text-center">
                <Link
                  to="/login"
                  className="inline-flex items-center text-sm text-ghana-green hover:text-ghana-green/80 transition-colors"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Login
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Additional Help */}
          <div className="text-center">
            <p className="text-xs text-gray-500">
              Still having trouble? Contact our support team at{" "}
              <Link to="/contact" className="text-ghana-green hover:underline">
                talesandtrailsghana@gmail.com
              </Link>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
