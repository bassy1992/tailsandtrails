import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import { destinationsApi, Destination } from "@/lib/api";
import { useToast } from "@/contexts/ToastContext";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { 
  MapPin, Star, Users, Clock, Calendar, Car, Hotel, Utensils, Shield, 
  Camera, ChevronLeft, Heart, Share2, CheckCircle, AlertCircle, Phone, Mail 
} from "lucide-react";

// Using the Destination interface from API
type TourData = Destination;

export default function TourDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { showError, showWarning } = useToast();
  const { isAuthenticated } = useAuth();
  const [tour, setTour] = useState<TourData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(0);
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedDate, setSelectedDate] = useState(() => {
    // Set default date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  });
  const [travelers, setTravelers] = useState(1);

  // Fetch tour data from API
  useEffect(() => {
    const fetchTour = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        
        // Try to fetch by slug first, if that fails and id is numeric, try to find by ID
        let tourData;
        try {
          tourData = await destinationsApi.getDestination(id);
        } catch (error) {
          // If id is numeric, try to find the destination by ID and get its slug
          if (/^\d+$/.test(id)) {
            const allDestinations = await destinationsApi.getDestinations();
            const destination = allDestinations.find(dest => dest.id.toString() === id);
            if (destination) {
              tourData = destination;
            } else {
              throw new Error('Destination not found');
            }
          } else {
            throw error;
          }
        }
        
        setTour(tourData);
        
        // If we accessed by ID, redirect to the proper slug URL for SEO
        if (/^\d+$/.test(id) && tourData.slug !== id) {
          navigate(`/tour/${tourData.slug}`, { replace: true });
        }
      } catch (error) {
        console.error('Error fetching tour:', error);
        showError('Failed to load tour details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchTour();
  }, [id, showError]);

  // Mock additional data that's not in our API yet
  const getMockTourData = (tour: Destination) => ({
    ...tour,
    images: [tour.image], // Use main image, can be extended later
    itinerary: [
      {
        day: 1,
        title: "Tour Experience",
        activities: [
          "Meet at designated location",
          "Begin guided tour experience",
          "Explore main attractions",
          "Cultural activities and interactions",
          "Return to starting point"
        ],
        meals: tour.duration_display.includes("Day") ? ["Lunch"] : ["Breakfast", "Lunch", "Dinner"],
        accommodation: tour.duration_display.includes("Day") ? undefined : "Comfortable accommodation included"
      }
    ],
    meetingPoint: "Kwame Nkrumah Memorial Park, Accra",
    difficulty: "Easy",
    ageLimit: "Suitable for all ages",
    languages: ["English", "Local languages"],
    cancellation: "Free cancellation up to 24 hours before departure",
    reviews_data: [
      {
        name: "Happy Customer",
        rating: Math.floor(parseFloat(tour.rating)),
        comment: "Great experience! Highly recommended.",
        date: "2024-01-15",
        avatar: "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=100"
      }
    ]
  });

  // Get enhanced tour data with mock fields
  const enhancedTour = tour ? getMockTourData(tour) : null;

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ghana-green"></div>
        </div>
      </Layout>
    );
  }

  if (!tour || !enhancedTour) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Tour Not Found</h2>
            <p className="text-gray-600 mb-6">The tour you're looking for doesn't exist.</p>
            <Link to="/destinations">
              <Button className="bg-ghana-green hover:bg-ghana-green/90">
                <ChevronLeft className="h-4 w-4 mr-2" />
                Back to Destinations
              </Button>
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Breadcrumb */}
      <div className="bg-gray-50 py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex items-center space-x-2 text-sm">
            <Link to="/" className="text-gray-500 hover:text-ghana-green">Home</Link>
            <span className="text-gray-400">/</span>
            <Link to="/destinations" className="text-gray-500 hover:text-ghana-green">Destinations</Link>
            <span className="text-gray-400">/</span>
            <span className="text-gray-900">{tour.name}</span>
          </nav>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Side - Images */}
          <div className="lg:col-span-2">
            <div className="space-y-4">
              {/* Main Image */}
              <div className="relative">
                <img
                  src={enhancedTour.images[selectedImage]}
                  alt={tour.name}
                  className="w-full h-96 object-cover rounded-lg"
                />
                <div className="absolute top-4 left-4">
                  <Badge className="bg-ghana-gold text-black font-semibold">
                    {tour.category.name}
                  </Badge>
                </div>
                <div className="absolute top-4 right-4 flex space-x-2">
                  <Button size="sm" variant="secondary" className="bg-white/90 hover:bg-white">
                    <Heart className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="secondary" className="bg-white/90 hover:bg-white">
                    <Share2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Thumbnail Images */}
              {enhancedTour.images.length > 1 && (
                <div className="flex space-x-2 overflow-x-auto">
                  {enhancedTour.images.map((image, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedImage(index)}
                      className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors ${
                        selectedImage === index ? "border-ghana-green" : "border-gray-200"
                      }`}
                    >
                      <img
                        src={image}
                        alt={`${tour.name} ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Side - Booking Card */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-3xl font-bold text-ghana-green">GH₵{tour.price}</div>
                    <div className="text-sm text-gray-500">per person</div>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="font-semibold">{tour.rating}</span>
                    <span className="text-gray-500">({tour.reviews_count} reviews)</span>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Quick Info */}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4 text-gray-600" />
                    <span>{tour.duration_display}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Users className="h-4 w-4 text-gray-600" />
                    <span>Max {tour.max_group_size}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <MapPin className="h-4 w-4 text-gray-600" />
                    <span>{tour.location}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Calendar className="h-4 w-4 text-gray-600" />
                    <span>Daily</span>
                  </div>
                </div>

                <Separator />

                {/* Booking Form */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Select Date
                    </label>
                    <input
                      type="date"
                      value={selectedDate}
                      onChange={(e) => setSelectedDate(e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md focus:ring-ghana-green focus:border-ghana-green"
                      min={new Date().toISOString().split('T')[0]}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Number of Travelers
                    </label>
                    <select
                      value={travelers}
                      onChange={(e) => setTravelers(Number(e.target.value))}
                      className="w-full p-2 border border-gray-300 rounded-md focus:ring-ghana-green focus:border-ghana-green"
                    >
                      {[...Array(tour.max_group_size)].map((_, i) => (
                        <option key={i + 1} value={i + 1}>
                          {i + 1} {i === 0 ? "person" : "people"}
                        </option>
                      ))}
                    </select>
                  </div>

                  <Button
                    onClick={() => {
                      if (!selectedDate) {
                        showWarning("Please select a date first");
                        return;
                      }

                      // Check if user is authenticated
                      if (!isAuthenticated) {
                        showWarning("Please sign in to book this tour");
                        // Redirect to login with return URL
                        navigate('/login', { 
                          state: { 
                            from: `/tour/${tour.slug}`,
                            message: "Please sign in to continue with your booking"
                          } 
                        });
                        return;
                      }

                      // Navigate to booking page with tour data
                      navigate(`/booking/${tour.slug}`, {
                        state: {
                          tourId: tour.id.toString(),
                          tourName: tour.name,
                          duration: tour.duration_display,
                          basePrice: parseFloat(tour.price),
                          selectedDate: selectedDate,
                          travelers: {
                            adults: Math.max(1, travelers - (travelers > 2 ? 1 : 0)), // Assume children if more than 2
                            children: travelers > 2 ? 1 : 0
                          }
                        }
                      });
                    }}
                    className="w-full bg-ghana-green hover:bg-ghana-green/90 text-white"
                  >
                    {isAuthenticated ? "Book Now" : "Sign In to Book"}
                  </Button>

                  <Button 
                    variant="outline" 
                    className="w-full border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white"
                    onClick={() => {
                      if (!selectedDate) {
                        showWarning("Please select a date first");
                        return;
                      }

                      // Check if user is authenticated
                      if (!isAuthenticated) {
                        showWarning("Please sign in to reserve this tour");
                        // Redirect to login with return URL
                        navigate('/login', { 
                          state: { 
                            from: `/tour/${tour.slug}`,
                            message: "Please sign in to continue with your reservation"
                          } 
                        });
                        return;
                      }

                      // Navigate to booking page with reservation flag
                      navigate(`/booking/${tour.slug}`, {
                        state: {
                          tourId: tour.id.toString(),
                          tourName: tour.name,
                          duration: tour.duration_display,
                          basePrice: parseFloat(tour.price),
                          selectedDate: selectedDate,
                          travelers: {
                            adults: Math.max(1, travelers - (travelers > 2 ? 1 : 0)),
                            children: travelers > 2 ? 1 : 0
                          },
                          isReservation: true
                        }
                      });
                    }}
                  >
                    {isAuthenticated ? "Reserve (Pay Later)" : "Sign In to Reserve"}
                  </Button>
                </div>

                <Separator />

                {/* Contact Info */}
                <div className="space-y-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <Phone className="h-4 w-4 text-ghana-green" />
                    <span>+233 24 123 4567</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4 text-ghana-green" />
                    <span>tours@talesandtrails.gh</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Main Content */}
        <div className="mt-12">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              {/* Title and Description */}
              <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">{tour.name}</h1>
                <div className="flex items-center space-x-4 text-gray-600 mb-6">
                  <div className="flex items-center space-x-1">
                    <MapPin className="h-5 w-5" />
                    <span>{tour.location}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                    <span>{tour.rating} ({tour.reviews_count} reviews)</span>
                  </div>
                </div>
                <p className="text-lg text-gray-700 leading-relaxed">{tour.description}</p>
              </div>

              {/* Tabs */}
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="overview">Overview</TabsTrigger>
                  <TabsTrigger value="itinerary">Itinerary</TabsTrigger>
                  <TabsTrigger value="included">What's Included</TabsTrigger>
                  <TabsTrigger value="reviews">Reviews</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-6 mt-6">
                  {/* Highlights */}
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">Tour Highlights</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {tour.highlights.map((highlight, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <CheckCircle className="h-5 w-5 text-ghana-green flex-shrink-0" />
                          <span className="text-gray-700">{highlight.highlight}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Tour Details */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">Tour Details</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Duration:</span>
                          <span className="font-medium">{tour.duration_display}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Group Size:</span>
                          <span className="font-medium">Max {tour.max_group_size} people</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Difficulty:</span>
                          <span className="font-medium">{enhancedTour.difficulty}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Age Limit:</span>
                          <span className="font-medium">{enhancedTour.ageLimit}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Languages:</span>
                          <span className="font-medium">{enhancedTour.languages.join(", ")}</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">Meeting Point</h4>
                      <p className="text-sm text-gray-700 mb-2">{enhancedTour.meetingPoint}</p>
                      
                      <h4 className="font-semibold text-gray-900 mb-3 mt-4">Cancellation Policy</h4>
                      <p className="text-sm text-gray-700">{enhancedTour.cancellation}</p>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="itinerary" className="space-y-6 mt-6">
                  <h3 className="text-xl font-semibold text-gray-900">Detailed Itinerary</h3>
                  {enhancedTour.itinerary.map((day, index) => (
                    <Card key={index}>
                      <CardHeader>
                        <CardTitle className="flex items-center space-x-2">
                          <span className="bg-ghana-green text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">
                            {day.day}
                          </span>
                          <span>Day {day.day}: {day.title}</span>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div>
                          <h5 className="font-semibold text-gray-900 mb-2">Activities</h5>
                          <ul className="space-y-1">
                            {day.activities.map((activity, actIndex) => (
                              <li key={actIndex} className="text-sm text-gray-700 flex items-start space-x-2">
                                <span className="text-ghana-green">•</span>
                                <span>{activity}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <div className="flex flex-wrap gap-4">
                          <div>
                            <h6 className="font-medium text-gray-900 mb-1">Meals Included</h6>
                            <div className="flex space-x-2">
                              {day.meals.map((meal, mealIndex) => (
                                <Badge key={mealIndex} variant="secondary">{meal}</Badge>
                              ))}
                            </div>
                          </div>
                          
                          {day.accommodation && (
                            <div>
                              <h6 className="font-medium text-gray-900 mb-1">Accommodation</h6>
                              <Badge variant="outline">{day.accommodation}</Badge>
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </TabsContent>

                <TabsContent value="included" className="space-y-6 mt-6">
                  <h3 className="text-xl font-semibold text-gray-900">What's Included</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                        <CheckCircle className="h-5 w-5 text-ghana-green" />
                        <span>Included</span>
                      </h4>
                      <ul className="space-y-2">
                        {tour.includes.map((item, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <CheckCircle className="h-4 w-4 text-ghana-green mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-gray-700">{item.item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                        <AlertCircle className="h-5 w-5 text-red-500" />
                        <span>Not Included</span>
                      </h4>
                      <ul className="space-y-2">
                        <li className="flex items-start space-x-2">
                          <AlertCircle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-700">Personal expenses and souvenirs</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <AlertCircle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-700">Tips for guides and drivers</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <AlertCircle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-700">Travel insurance (basic coverage included)</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <AlertCircle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-700">Alcoholic beverages</span>
                        </li>
                      </ul>
                    </div>
                  </div>

                  {/* Service Icons */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <Car className="h-8 w-8 text-ghana-green mx-auto mb-2" />
                      <div className="text-sm font-medium">Transport</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <Hotel className="h-8 w-8 text-ghana-green mx-auto mb-2" />
                      <div className="text-sm font-medium">Accommodation</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <Utensils className="h-8 w-8 text-ghana-green mx-auto mb-2" />
                      <div className="text-sm font-medium">Meals</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <Shield className="h-8 w-8 text-ghana-green mx-auto mb-2" />
                      <div className="text-sm font-medium">Insurance</div>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="reviews" className="space-y-6 mt-6">
                  <div className="flex justify-between items-center">
                    <h3 className="text-xl font-semibold text-gray-900">Customer Reviews</h3>
                    <div className="flex items-center space-x-2">
                      <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                      <span className="text-lg font-semibold">{tour.rating}</span>
                      <span className="text-gray-500">({tour.reviews_count} reviews)</span>
                    </div>
                  </div>

                  <div className="space-y-6">
                    {enhancedTour.reviews_data.map((review, index) => (
                      <Card key={index}>
                        <CardContent className="pt-6">
                          <div className="flex items-start space-x-4">
                            <Avatar>
                              <AvatarImage src={review.avatar} />
                              <AvatarFallback>{review.name.charAt(0)}</AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                              <div className="flex justify-between items-start mb-2">
                                <div>
                                  <h4 className="font-semibold text-gray-900">{review.name}</h4>
                                  <div className="flex items-center space-x-1">
                                    {[...Array(5)].map((_, i) => (
                                      <Star
                                        key={i}
                                        className={`h-4 w-4 ${
                                          i < review.rating
                                            ? "fill-yellow-400 text-yellow-400"
                                            : "text-gray-300"
                                        }`}
                                      />
                                    ))}
                                  </div>
                                </div>
                                <span className="text-sm text-gray-500">{review.date}</span>
                              </div>
                              <p className="text-gray-700">{review.comment}</p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </TabsContent>
              </Tabs>
            </div>

            {/* Right Sidebar */}
            <div className="lg:col-span-1">
              <div className="space-y-6">
                {/* Similar Tours */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Similar Tours</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex space-x-3">
                      <img
                        src="https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=200"
                        alt="Aburi Gardens"
                        className="w-16 h-16 object-cover rounded-lg"
                      />
                      <div className="flex-1">
                        <h4 className="font-medium text-sm">Aburi Gardens Nature Escape</h4>
                        <p className="text-xs text-gray-500">1 Day • GH₵280</p>
                        <div className="flex items-center space-x-1 mt-1">
                          <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                          <span className="text-xs">4.6 (89)</span>
                        </div>
                      </div>
                    </div>
                    <Link to="/destinations" className="block">
                      <Button variant="outline" size="sm" className="w-full">
                        View All Tours
                      </Button>
                    </Link>
                  </CardContent>
                </Card>

                {/* Need Help */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Need Help?</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-sm text-gray-600">
                      Have questions about this tour? Our travel experts are here to help.
                    </p>
                    <div className="space-y-2">
                      <Button variant="outline" size="sm" className="w-full justify-start">
                        <Phone className="h-4 w-4 mr-2" />
                        Call Us
                      </Button>
                      <Button variant="outline" size="sm" className="w-full justify-start">
                        <Mail className="h-4 w-4 mr-2" />
                        Email Us
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}