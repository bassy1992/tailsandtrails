import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Calendar, MapPin, Search, Star, Users, Clock, Car, Hotel, Utensils, Shield } from "lucide-react";
import { Link } from "react-router-dom";
import VideoSection from "@/components/VideoSection";
import { destinationsApi, Destination } from "@/lib/api";

export default function Index() {
  const [searchTerm, setSearchTerm] = useState("");
  const [featuredTours, setFeaturedTours] = useState<Destination[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFeaturedTours = async () => {
      try {
        setLoading(true);
        const destinations = await destinationsApi.getDestinations();
        // Filter featured destinations or take first 4
        const featured = destinations.filter(d => d.is_featured).slice(0, 4);
        if (featured.length === 0) {
          setFeaturedTours(destinations.slice(0, 4));
        } else {
          setFeaturedTours(featured);
        }
      } catch (error) {
        console.error('Failed to load destinations:', error);
      } finally {
        setLoading(false);
      }
    };

    loadFeaturedTours();
  }, []);

  const featuredVideos = [
    {
      id: 1,
      title: "Volta Region Waterfalls Discovery",
      description: "Discover the magnificent Wli Waterfalls and other hidden gems in the Volta Region. A perfect blend of nature, hiking, and local culture.",
      thumbnail: "https://images.pexels.com/photos/33475234/pexels-photo-33475234.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/31934467/13602616_360_640_25fps.mp4",
      duration: "10:15",
      views: "15.2K",
      category: "nature",
      location: "Volta Region"
    },
    {
      id: 2,
      title: "Cape Coast Castle - A Journey Through History",
      description: "Explore the historic Cape Coast Castle and learn about its significance in Ghana's heritage.",
      thumbnail: "https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/29603787/12740641_640_360_60fps.mp4",
      duration: "8:45",
      views: "12.5K",
      category: "heritage",
      location: "Cape Coast"
    },
    {
      id: 3,
      title: "Kakum National Park Canopy Adventure",
      description: "Experience the breathtaking canopy walk 40 meters above the forest floor.",
      thumbnail: "https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/17844988/17844988-sd_240_426_30fps.mp4",
      duration: "6:30",
      views: "8.9K",
      category: "adventure",
      location: "Kakum National Park"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      location: "USA",
      rating: 5,
      comment: "Absolutely incredible experience! The Cape Coast tour was educational and moving. Our guide was knowledgeable and the accommodations were excellent.",
      avatar: "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=100"
    },
    {
      name: "Emmanuel Asante",
      location: "UK",
      rating: 5,
      comment: "Tales and Trails Ghana made my first trip to Ghana unforgettable. The Kakum canopy walk was breathtaking and the cultural experiences were authentic.",
      avatar: "https://images.pexels.com/photos/1040880/pexels-photo-1040880.jpeg?auto=compress&cs=tinysrgb&w=100"
    },
    {
      name: "Marie Dubois",
      location: "France",
      rating: 4,
      comment: "Wonderful organization and attention to detail. The Aburi Gardens tour was peaceful and the transport was comfortable throughout.",
      avatar: "https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=100"
    }
  ];

  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-ghana-green to-ghana-blue text-white">
        <div className="absolute inset-0 bg-black/40"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 md:py-24">
          <div className="text-center space-y-6 sm:space-y-8">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold leading-tight px-2">
              Discover Ghana's
              <span className="block text-ghana-gold mt-2">Rich Heritage</span>
            </h1>
            <p className="text-base sm:text-lg md:text-xl lg:text-2xl max-w-3xl mx-auto text-gray-200 px-4">
              Experience the beauty, culture, and history of Ghana with our comprehensive tour packages including transport, accommodation, meals, and medical support.
            </p>
            
            {/* Search Bar */}
            <div className="max-w-2xl mx-auto bg-white rounded-lg p-3 sm:p-4 shadow-lg">
              <div className="flex flex-col gap-3 sm:gap-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <Input
                    type="text"
                    placeholder="Where do you want to go?"
                    className="pl-10 text-gray-900 h-11"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <Input
                    type="date"
                    className="pl-10 text-gray-900 h-11"
                  />
                </div>
                <Button className="bg-ghana-gold hover:bg-ghana-gold/90 text-black font-semibold h-11 w-full">
                  Search Tours
                </Button>
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-3 sm:gap-4 text-xs sm:text-sm px-4">
              <div className="flex items-center space-x-2">
                <Car className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Transport Included</span>
              </div>
              <div className="flex items-center space-x-2">
                <Hotel className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Quality Hotels</span>
              </div>
              <div className="flex items-center space-x-2">
                <Utensils className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Local Cuisine</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Medical Support</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Tours */}
      <section className="py-12 sm:py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-3 sm:space-y-4 mb-8 sm:mb-12">
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 px-4">Featured Tours</h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 max-w-2xl mx-auto px-4">
              Discover our most popular destinations and experience the best of Ghana
            </p>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-600">Loading featured tours...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {featuredTours.map((tour) => (
                <Card key={tour.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="relative">
                    <img
                      src={tour.image}
                      alt={tour.name}
                      className="w-full h-48 object-cover"
                    />
                    <Badge className="absolute top-2 right-2 bg-ghana-gold text-black">
                      {tour.duration_display}
                    </Badge>
                  </div>
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{tour.name}</CardTitle>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-ghana-green">GH₵{tour.price}</div>
                        <div className="text-sm text-gray-500">per person</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1 text-sm text-gray-600">
                      <MapPin className="h-4 w-4" />
                      <span>{tour.location}</span>
                    </div>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <CardDescription className="mb-3 line-clamp-2">{tour.description}</CardDescription>
                    <div className="flex items-center space-x-1 mb-3">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="font-semibold">{tour.rating}</span>
                      <span className="text-gray-500">({tour.reviews_count} reviews)</span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {tour.includes.slice(0, 3).map((item, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {item.item}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Link to={`/tour/${tour.slug}`} className="w-full">
                      <Button className="w-full bg-ghana-green hover:bg-ghana-green/90">
                        Book Now
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link to="/destinations">
              <Button variant="outline" size="lg" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                View All Destinations
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Statistics */}
      <section className="py-12 sm:py-16 bg-ghana-green text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 sm:gap-8 text-center">
            <div className="space-y-1 sm:space-y-2">
              <div className="text-3xl sm:text-4xl font-bold text-ghana-gold">500+</div>
              <div className="text-sm sm:text-base md:text-lg">Happy Tourists</div>
            </div>
            <div className="space-y-1 sm:space-y-2">
              <div className="text-3xl sm:text-4xl font-bold text-ghana-gold">15+</div>
              <div className="text-sm sm:text-base md:text-lg">Destinations</div>
            </div>
            <div className="space-y-1 sm:space-y-2">
              <div className="text-3xl sm:text-4xl font-bold text-ghana-gold">50+</div>
              <div className="text-sm sm:text-base md:text-lg">Tour Packages</div>
            </div>
            <div className="space-y-1 sm:space-y-2">
              <div className="text-3xl sm:text-4xl font-bold text-ghana-gold">24/7</div>
              <div className="text-sm sm:text-base md:text-lg">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Videos */}
      <VideoSection
        title="Experience Ghana Through Video"
        subtitle="Watch immersive videos of our most popular destinations and get inspired for your next adventure"
        videos={featuredVideos}
        maxVideos={3}
        layout="grid"
      />

      {/* Testimonials */}
      <section className="py-12 sm:py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-3 sm:space-y-4 mb-8 sm:mb-12">
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 px-4">What Our Tourists Say</h2>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 max-w-2xl mx-auto px-4">
              Read experiences from travelers who discovered Ghana with us
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="text-center">
                <CardContent className="pt-6">
                  <div className="flex justify-center mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`h-5 w-5 ${
                          i < testimonial.rating
                            ? "fill-yellow-400 text-yellow-400"
                            : "text-gray-300"
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-gray-600 mb-6 italic">"{testimonial.comment}"</p>
                  <div className="flex items-center justify-center space-x-3">
                    <Avatar>
                      <AvatarImage src={testimonial.avatar} />
                      <AvatarFallback>{testimonial.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <div className="font-semibold">{testimonial.name}</div>
                      <div className="text-sm text-gray-500">{testimonial.location}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-12 sm:py-16 bg-gradient-to-r from-ghana-gold to-amber-400 text-black">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6 sm:space-y-8">
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold px-4">Ready to Explore Ghana?</h2>
          <p className="text-base sm:text-lg md:text-xl px-4">
            Join hundreds of satisfied tourists who have discovered the beauty and culture of Ghana with us. 
            Book your adventure today!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center px-4">
            <Link to="/destinations" className="w-full sm:w-auto">
              <Button size="lg" className="bg-ghana-green hover:bg-ghana-green/90 text-white w-full sm:w-auto">
                Plan Your Trip
              </Button>
            </Link>
            <Link to="/contact" className="w-full sm:w-auto">
              <Button size="lg" variant="outline" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white w-full sm:w-auto">
                Contact Us
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
