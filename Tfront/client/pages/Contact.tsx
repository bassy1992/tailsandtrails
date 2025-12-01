import { useState } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapPin, Phone, Mail, Clock, Send, MessageCircle, HelpCircle, Calendar } from "lucide-react";

export default function Contact() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    subject: "",
    inquiry_type: "",
    message: "",
    preferred_contact: "email"
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate form submission
    setTimeout(() => {
      console.log("Contact form submitted:", formData);
      setIsLoading(false);
      setIsSubmitted(true);
    }, 2000);
  };

  const inquiryTypes = [
    "Tour Booking",
    "Custom Tour Request",
    "General Information", 
    "Pricing Questions",
    "Travel Support",
    "Group Bookings",
    "Partnership Inquiry",
    "Other"
  ];

  if (isSubmitted) {
    return (
      <Layout>
        <div className="min-h-[calc(100vh-80px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full text-center">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Send className="h-8 w-8 text-ghana-green" />
                </div>
                <CardTitle className="text-2xl text-ghana-green">Message Sent!</CardTitle>
                <CardDescription>
                  Thank you for contacting Tales and Trails Ghana. We've received your message and will get back to you within 24 hours.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button 
                  onClick={() => setIsSubmitted(false)}
                  className="w-full bg-ghana-green hover:bg-ghana-green/90"
                >
                  Send Another Message
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Header */}
      <section className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold">Contact Us</h1>
            <p className="text-xl text-gray-200 max-w-3xl mx-auto">
              Get in touch with our travel experts. We're here to help you plan the perfect Ghana adventure.
            </p>
          </div>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Contact Form */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl text-ghana-green">Send Us a Message</CardTitle>
                <CardDescription>
                  Fill out the form below and we'll get back to you as soon as possible.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Name and Email */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Full Name *</Label>
                      <Input
                        id="name"
                        type="text"
                        placeholder="Your full name"
                        value={formData.name}
                        onChange={(e) => handleInputChange("name", e.target.value)}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email Address *</Label>
                      <Input
                        id="email"
                        type="email"
                        placeholder="your@email.com"
                        value={formData.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  {/* Phone and Inquiry Type */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="phone">Phone Number</Label>
                      <Input
                        id="phone"
                        type="tel"
                        placeholder="+233 24 123 4567"
                        value={formData.phone}
                        onChange={(e) => handleInputChange("phone", e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="inquiry_type">Inquiry Type *</Label>
                      <Select value={formData.inquiry_type} onValueChange={(value) => handleInputChange("inquiry_type", value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select inquiry type" />
                        </SelectTrigger>
                        <SelectContent>
                          {inquiryTypes.map((type) => (
                            <SelectItem key={type} value={type}>
                              {type}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Subject */}
                  <div className="space-y-2">
                    <Label htmlFor="subject">Subject *</Label>
                    <Input
                      id="subject"
                      type="text"
                      placeholder="Brief description of your inquiry"
                      value={formData.subject}
                      onChange={(e) => handleInputChange("subject", e.target.value)}
                      required
                    />
                  </div>

                  {/* Message */}
                  <div className="space-y-2">
                    <Label htmlFor="message">Message *</Label>
                    <Textarea
                      id="message"
                      placeholder="Tell us more about your travel plans, questions, or how we can help you..."
                      value={formData.message}
                      onChange={(e) => handleInputChange("message", e.target.value)}
                      rows={6}
                      required
                    />
                  </div>

                  {/* Preferred Contact Method */}
                  <div className="space-y-2">
                    <Label htmlFor="preferred_contact">Preferred Contact Method</Label>
                    <Select value={formData.preferred_contact} onValueChange={(value) => handleInputChange("preferred_contact", value)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="email">Email</SelectItem>
                        <SelectItem value="phone">Phone Call</SelectItem>
                        <SelectItem value="whatsapp">WhatsApp</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>Sending Message...</>
                    ) : (
                      <>
                        <Send className="h-4 w-4 mr-2" />
                        Send Message
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Contact Information */}
          <div className="lg:col-span-1 space-y-6">
            {/* Contact Details */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl text-ghana-green">Get in Touch</CardTitle>
                <CardDescription>
                  Reach out to us through any of these channels
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Phone className="h-5 w-5 text-ghana-green mt-1" />
                  <div>
                    <div className="font-medium">Phone</div>
                    <div className="text-sm text-gray-600">+233 24 123 4567</div>
                    <div className="text-sm text-gray-600">+233 20 987 6543</div>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <Mail className="h-5 w-5 text-ghana-green mt-1" />
                  <div>
                    <div className="font-medium">Email</div>
                    <div className="text-sm text-gray-600">info@talesandtrails.gh</div>
                    <div className="text-sm text-gray-600">bookings@talesandtrails.gh</div>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <MapPin className="h-5 w-5 text-ghana-green mt-1" />
                  <div>
                    <div className="font-medium">Office Address</div>
                    <div className="text-sm text-gray-600">
                      123 Independence Avenue<br />
                      Accra, Ghana<br />
                      West Africa
                    </div>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <Clock className="h-5 w-5 text-ghana-green mt-1" />
                  <div>
                    <div className="font-medium">Business Hours</div>
                    <div className="text-sm text-gray-600">
                      Monday - Friday: 8:00 AM - 6:00 PM<br />
                      Saturday: 9:00 AM - 4:00 PM<br />
                      Sunday: Closed
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl text-ghana-green">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start" asChild>
                  <a href="tel:+233241234567">
                    <Phone className="h-4 w-4 mr-2" />
                    Call Us Now
                  </a>
                </Button>
                
                <Button variant="outline" className="w-full justify-start" asChild>
                  <a href="mailto:info@talesandtrails.gh">
                    <Mail className="h-4 w-4 mr-2" />
                    Send Email
                  </a>
                </Button>

                <Button variant="outline" className="w-full justify-start" asChild>
                  <a href="https://wa.me/233241234567" target="_blank" rel="noopener noreferrer">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    WhatsApp Chat
                  </a>
                </Button>

                <Button variant="outline" className="w-full justify-start" asChild>
                  <a href="/destinations">
                    <Calendar className="h-4 w-4 mr-2" />
                    Book a Tour
                  </a>
                </Button>
              </CardContent>
            </Card>

            {/* FAQ Section */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl text-ghana-green flex items-center">
                  <HelpCircle className="h-5 w-5 mr-2" />
                  Common Questions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-sm">
                <div>
                  <div className="font-medium mb-1">How far in advance should I book?</div>
                  <div className="text-gray-600">We recommend booking at least 2-4 weeks in advance, especially during peak seasons.</div>
                </div>
                
                <div>
                  <div className="font-medium mb-1">Do you offer group discounts?</div>
                  <div className="text-gray-600">Yes! We offer special rates for groups of 8 or more people. Contact us for details.</div>
                </div>
                
                <div>
                  <div className="font-medium mb-1">What's included in the tour packages?</div>
                  <div className="text-gray-600">Our packages typically include transport, accommodation, meals, and professional guides. Check individual tour details.</div>
                </div>

                <div>
                  <div className="font-medium mb-1">Can you create custom itineraries?</div>
                  <div className="text-gray-600">Absolutely! We specialize in creating personalized tours based on your interests and budget.</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Map Section */}
        <div className="mt-12">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl text-ghana-green">Our Location</CardTitle>
              <CardDescription>
                Visit our office in the heart of Accra for personalized tour planning
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <MapPin className="h-12 w-12 mx-auto mb-4 text-ghana-green" />
                  <p className="font-medium">Interactive Map</p>
                  <p className="text-sm">123 Independence Avenue, Accra, Ghana</p>
                  <p className="text-xs mt-2">Map integration would be implemented here</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
