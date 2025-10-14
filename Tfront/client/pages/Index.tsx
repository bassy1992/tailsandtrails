import { useState, useEffect, useRef } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar, MapPin, Search, Star, Users, Clock, Car, Hotel, Utensils, Shield, Filter, X, Loader2 } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import VideoSection from "@/components/VideoSection";
import Currency from "@/lib/currency";

interface SearchResult {
  id: number;
  name: string;
  location: string;
  price: string;
  duration: string;
  rating: number;
  image: string;
  category: string;
}

export default function Index() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [searchDate, setSearchDate] = useState("");
  const [priceFilter, setPriceFilter] = useState("");
  const [durationFilter, setDurationFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [categories, setCategories] = useState<any[]>([]);
  const searchTimeoutRef = useRef<NodeJS.Timeout>();
  const searchResultsRef = useRef<HTMLDivElement>(null);

  // Fetch categories on component mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Handle search with debouncing
  useEffect(() => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (searchTerm.length >= 2) {
      searchTimeoutRef.current = setTimeout(() => {
        performSearch();
      }, 300);
    } else {
      setSearchResults([]);
      setShowResults(false);
    }

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [searchTerm, priceFilter, durationFilter, categoryFilter]);

  // Close search results when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchResultsRef.current && !searchResultsRef.current.contains(event.target as Node)) {
        setShowResults(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/categories/`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const performSearch = async () => {
    setIsSearching(true);
    try {
      const params = new URLSearchParams();
      
      if (searchTerm) params.append('search', searchTerm);
      if (priceFilter) params.append('price_category', priceFilter);
      if (durationFilter) params.append('duration_category', durationFilter);
      if (categoryFilter) params.append('category', categoryFilter);
      
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/destinations/?${params.toString()}`);
      
      if (response.ok) {
        const data = await response.json();
        const formattedResults = data.results?.map((dest: any) => ({
          id: dest.id,
          name: dest.name,
          location: dest.location,
          price: Currency.format(dest.price),
          duration: formatDuration(dest.duration),
          rating: dest.rating,
          image: dest.image || dest.images?.[0]?.image_url || '',
          category: dest.category?.name || ''
        })) || [];
        
        setSearchResults(formattedResults);
        setShowResults(formattedResults.length > 0);
      }
    } catch (error) {
      console.error('Error searching destinations:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const formatDuration = (duration: string) => {
    const durationMap: { [key: string]: string } = {
      '1_day': '1 Day',
      '2_days': '2 Days',
      '3_days': '3 Days',
      '4_days': '4 Days',
      '5_days': '5 Days',
      '6_days': '6 Days',
      '7_days': '7 Days',
      '7_plus_days': '7+ Days'
    };
    return durationMap[duration] || duration;
  };

  const handleSearchSubmit = () => {
    const params = new URLSearchParams();
    if (searchTerm) params.append('search', searchTerm);
    if (priceFilter) params.append('price_category', priceFilter);
    if (durationFilter) params.append('duration_category', durationFilter);
    if (categoryFilter) params.append('category', categoryFilter);
    if (searchDate) params.append('date', searchDate);
    
    navigate(`/destinations?${params.toString()}`);
  };

  const clearFilters = () => {
    setSearchTerm("");
    setPriceFilter("");
    setDurationFilter("");
    setCategoryFilter("");
    setSearchDate("");
    setSearchResults([]);
    setShowResults(false);
  };

  const featuredTours = [
    {
      id: 1,
      name: "Cape Coast Castle Heritage Tour",
      location: "Cape Coast",
      image: "https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=800",
      price: "GH¢450",
      duration: "2 Days",
      rating: 4.8,
      reviews: 124,
      description: "Explore the historic Cape Coast Castle and learn about Ghana's rich heritage.",
      includes: ["Transport", "Accommodation", "Meals", "Guide"]
    },
    {
      id: 2,
      name: "Aburi Gardens Nature Escape",
      location: "Aburi",
      image: "https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=800",
      price: "GH¢280",
      duration: "1 Day",
      rating: 4.6,
      reviews: 89,
      description: "Relax in the beautiful botanical gardens with stunning mountain views.",
      includes: ["Transport", "Lunch", "Guide"]
    },
    {
      id: 3,
      name: "Manhyia Palace Cultural Tour",
      location: "Kumasi",
      image: "https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=800",
      price: "GH¢350",
      duration: "1 Day",
      rating: 4.7,
      reviews: 156,
      description: "Visit the seat of the Asantehene and learn about Ashanti culture.",
      includes: ["Transport", "Cultural Guide", "Lunch"]
    },
    {
      id: 4,
      name: "Kakum Canopy Walk Adventure",
      location: "Kakum National Park",
      image: "https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800",
      price: "GH¢520",
      duration: "3 Days",
      rating: 4.9,
      reviews: 203,
      description: "Experience the thrilling canopy walk and explore the rainforest.",
      includes: ["Transport", "Accommodation", "All Meals", "Park Fees"]
    }
  ];

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
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center space-y-8">
            <h1 className="text-4xl md:text-6xl font-bold leading-tight">
              Discover Ghana's
              <span className="block text-ghana-gold">Rich Heritage</span>
            </h1>
            <p className="text-xl md:text-2xl max-w-3xl mx-auto text-gray-200">
              Experience the beauty, culture, and history of Ghana with our comprehensive tour packages including transport, accommodation, meals, and medical support.
            </p>
            
            {/* Enhanced Search Bar */}
            <div className="max-w-4xl mx-auto bg-white rounded-lg p-6 shadow-lg" ref={searchResultsRef}>
              <div className="space-y-4">
                {/* Main Search Row */}
                <div className="flex flex-col lg:flex-row gap-4">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <Input
                      type="text"
                      placeholder="Search destinations, locations, or activities..."
                      className="pl-10 text-gray-900"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      onFocus={() => searchResults.length > 0 && setShowResults(true)}
                    />
                    {isSearching && (
                      <Loader2 className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5 animate-spin" />
                    )}
                  </div>
                  <div className="flex-1 relative">
                    <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <Input
                      type="date"
                      className="pl-10 text-gray-900"
                      value={searchDate}
                      onChange={(e) => setSearchDate(e.target.value)}
                    />
                  </div>
                  <Button 
                    className="bg-ghana-gold hover:bg-ghana-gold/90 text-black font-semibold px-8"
                    onClick={handleSearchSubmit}
                  >
                    Search Tours
                  </Button>
                </div>

                {/* Filters Row */}
                <div className="flex flex-col sm:flex-row gap-4 items-center">
                  <div className="flex items-center gap-2">
                    <Filter className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600 font-medium">Filters:</span>
                  </div>
                  
                  <div className="flex flex-wrap gap-3 flex-1">
                    <Select value={priceFilter} onValueChange={setPriceFilter}>
                      <SelectTrigger className="w-32">
                        <SelectValue placeholder="Price" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="budget">Budget (&lt; {Currency.symbol}300)</SelectItem>
                        <SelectItem value="mid">Mid-range ({Currency.symbol}300-600)</SelectItem>
                        <SelectItem value="luxury">Luxury (&gt; {Currency.symbol}600)</SelectItem>
                      </SelectContent>
                    </Select>

                    <Select value={durationFilter} onValueChange={setDurationFilter}>
                      <SelectTrigger className="w-32">
                        <SelectValue placeholder="Duration" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="day">Day Trip</SelectItem>
                        <SelectItem value="weekend">Weekend (2-3 days)</SelectItem>
                        <SelectItem value="week">Week+ (4+ days)</SelectItem>
                      </SelectContent>
                    </Select>

                    <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                      <SelectTrigger className="w-40">
                        <SelectValue placeholder="Category" />
                      </SelectTrigger>
                      <SelectContent>
                        {categories.map((category) => (
                          <SelectItem key={category.id} value={category.id.toString()}>
                            {category.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {(searchTerm || priceFilter || durationFilter || categoryFilter) && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={clearFilters}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <X className="h-4 w-4 mr-1" />
                      Clear
                    </Button>
                  )}
                </div>

                {/* Search Results Dropdown */}
                {showResults && searchResults.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
                    <div className="p-3 border-b border-gray-100">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">
                          Found {searchResults.length} destination{searchResults.length !== 1 ? 's' : ''}
                        </span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowResults(false)}
                          className="h-6 w-6 p-0"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    <div className="max-h-80 overflow-y-auto">
                      {searchResults.map((result) => (
                        <Link
                          key={result.id}
                          to={`/tour/${result.id}`}
                          className="block p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                          onClick={() => setShowResults(false)}
                        >
                          <div className="flex items-center space-x-4">
                            <img
                              src={result.image || 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=100'}
                              alt={result.name}
                              className="w-16 h-16 object-cover rounded-lg"
                            />
                            <div className="flex-1">
                              <h4 className="font-semibold text-gray-900">{result.name}</h4>
                              <div className="flex items-center space-x-2 text-sm text-gray-600">
                                <MapPin className="h-3 w-3" />
                                <span>{result.location}</span>
                                <span>•</span>
                                <Clock className="h-3 w-3" />
                                <span>{result.duration}</span>
                              </div>
                              <div className="flex items-center justify-between mt-1">
                                <div className="flex items-center space-x-1">
                                  <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                                  <span className="text-sm font-medium">{result.rating}</span>
                                </div>
                                <span className="font-bold text-ghana-green">{result.price}</span>
                              </div>
                            </div>
                          </div>
                        </Link>
                      ))}
                    </div>
                    <div className="p-3 border-t border-gray-100">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleSearchSubmit}
                        className="w-full"
                      >
                        View All Results
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="flex items-center space-x-2">
                <Car className="h-5 w-5" />
                <span>Transport Included</span>
              </div>
              <div className="flex items-center space-x-2">
                <Hotel className="h-5 w-5" />
                <span>Quality Hotels</span>
              </div>
              <div className="flex items-center space-x-2">
                <Utensils className="h-5 w-5" />
                <span>Local Cuisine</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="h-5 w-5" />
                <span>Medical Support</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Tours */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900">Featured Tours</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Discover our most popular destinations and experience the best of Ghana
            </p>
          </div>

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
                    {tour.duration}
                  </Badge>
                </div>
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{tour.name}</CardTitle>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-ghana-green">{tour.price}</div>
                      <div className="text-sm text-gray-500">per person</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1 text-sm text-gray-600">
                    <MapPin className="h-4 w-4" />
                    <span>{tour.location}</span>
                  </div>
                </CardHeader>
                <CardContent className="pb-2">
                  <CardDescription className="mb-3">{tour.description}</CardDescription>
                  <div className="flex items-center space-x-1 mb-3">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="font-semibold">{tour.rating}</span>
                    <span className="text-gray-500">({tour.reviews} reviews)</span>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {tour.includes.map((item, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {item}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
                <CardFooter>
                  <Link to={`/tour/${tour.id}`} className="w-full">
                    <Button className="w-full bg-ghana-green hover:bg-ghana-green/90">
                      Book Now
                    </Button>
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>

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
      <section className="py-16 bg-ghana-green text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-4xl font-bold text-ghana-gold">500+</div>
              <div className="text-lg">Happy Tourists</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-ghana-gold">15+</div>
              <div className="text-lg">Destinations</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-ghana-gold">50+</div>
              <div className="text-lg">Tour Packages</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-ghana-gold">24/7</div>
              <div className="text-lg">Support</div>
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
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900">What Our Tourists Say</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Read experiences from travelers who discovered Ghana with us
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
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
      <section className="py-16 bg-gradient-to-r from-ghana-gold to-amber-400 text-black">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
          <h2 className="text-3xl md:text-4xl font-bold">Ready to Explore Ghana?</h2>
          <p className="text-xl">
            Join hundreds of satisfied tourists who have discovered the beauty and culture of Ghana with us. 
            Book your adventure today!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/destinations">
              <Button size="lg" className="bg-ghana-green hover:bg-ghana-green/90 text-white">
                Plan Your Trip
              </Button>
            </Link>
            <Link to="/contact">
              <Button size="lg" variant="outline" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                Contact Us
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
