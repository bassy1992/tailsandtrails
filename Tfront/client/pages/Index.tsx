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
import { destinationsApi, Destination, galleryApi, GalleryVideo } from "@/lib/api";

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

// Helper function to remove price information from text - AGGRESSIVE VERSION
const removePriceInfo = (text: string): string => {
  if (!text) return '';
  
  // Convert to string and handle all possible encodings
  let cleaned = String(text);
  
  // Remove ALL price patterns - be very aggressive
  cleaned = cleaned
    // Remove any GH followed by currency symbol and numbers
    .replace(/GH[¢₵￠]\s*\d+/gi, '')
    .replace(/GH\s*¢\s*\d+/gi, '')
    .replace(/GH\s*₵\s*\d+/gi, '')
    // Remove standalone currency symbols with numbers
    .replace(/[¢₵￠]\s*\d+/gi, '')
    // Remove "per person" in any form
    .replace(/per\s*person/gi, '')
    .replace(/perperson/gi, '')
    // Remove any remaining standalone numbers that look like prices (50-9999)
    .replace(/\b\d{2,4}\b/g, '')
    // Remove extra whitespace
    .replace(/\s+/g, ' ')
    .trim();
  
  return cleaned;
};

export default function Index() {
  console.log('=== INDEX PAGE COMPONENT LOADED ===');
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
  const [featuredTours, setFeaturedTours] = useState<Destination[]>([]);
  const [isLoadingFeatured, setIsLoadingFeatured] = useState(true);
  const [featuredVideos, setFeaturedVideos] = useState<any[]>([]);
  const [isLoadingVideos, setIsLoadingVideos] = useState(true);
  const searchTimeoutRef = useRef<NodeJS.Timeout>();
  const searchResultsRef = useRef<HTMLDivElement>(null);

  // Fetch categories, featured tours, and videos on component mount
  useEffect(() => {
    fetchCategories();
    fetchFeaturedTours();
    fetchFeaturedVideos();
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
      const data = await destinationsApi.getCategories();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchFeaturedTours = async () => {
    console.log('=== FETCH FEATURED TOURS STARTED ===');
    try {
      setIsLoadingFeatured(true);
      // Fetch destinations and filter for featured ones, or get first 4 if no featured flag
      const destinations = await destinationsApi.getDestinations({ ordering: '-rating' });
      console.log('Fetched destinations:', destinations.length);
      
      // Get featured destinations or top-rated ones
      const featured = destinations.filter(dest => dest.is_featured).slice(0, 4);
      console.log('Featured tours found:', featured.length);
      
      // Clean price info from all tour data
      const cleanTourData = (tours: Destination[]) => {
        return tours.map(tour => {
          console.log('BEFORE CLEANING:', {
            name: tour.name,
            location: tour.location,
            description: tour.description.substring(0, 100)
          });
          
          const cleaned = {
            ...tour,
            name: removePriceInfo(tour.name),
            location: removePriceInfo(tour.location),
            description: removePriceInfo(tour.description)
          };
          
          console.log('AFTER CLEANING:', {
            name: cleaned.name,
            location: cleaned.location,
            description: cleaned.description.substring(0, 100)
          });
          
          return cleaned;
        });
      };
      
      // If we don't have enough featured destinations, fill with top-rated ones
      if (featured.length < 4) {
        const topRated = destinations.slice(0, 4 - featured.length);
        setFeaturedTours(cleanTourData([...featured, ...topRated]));
      } else {
        setFeaturedTours(cleanTourData(featured));
      }
    } catch (error) {
      console.error('=== ERROR FETCHING FEATURED TOURS ===', error);
      // Fallback to empty array if API fails
      setFeaturedTours([]);
    } finally {
      setIsLoadingFeatured(false);
      console.log('=== FETCH FEATURED TOURS COMPLETED ===');
    }
  };

  const fetchFeaturedVideos = async () => {
    try {
      setIsLoadingVideos(true);
      
      // Try to fetch featured videos from gallery API
      const galleryVideos = await galleryApi.getVideos({ 
        featured: true, 
        ordering: '-views' 
      });
      
      if (galleryVideos && galleryVideos.length > 0) {
        // Transform GalleryVideo to Video interface expected by VideoSection
        const transformedVideos = galleryVideos.slice(0, 3).map((video: GalleryVideo) => ({
          id: video.id,
          title: video.title,
          description: video.description,
          thumbnail: video.thumbnail_url,
          videoUrl: video.video_url,
          duration: video.duration,
          views: video.formatted_views,
          category: video.category?.name || 'general',
          location: video.location
        }));
        
        setFeaturedVideos(transformedVideos);
      } else {
        // Fallback to hardcoded videos if no gallery videos available
        const fallbackVideos = [
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
        
        setFeaturedVideos(fallbackVideos);
      }
    } catch (error) {
      console.error('Error fetching featured videos:', error);
      
      // Fallback to hardcoded videos if API fails
      const fallbackVideos = [
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
      
      setFeaturedVideos(fallbackVideos);
    } finally {
      setIsLoadingVideos(false);
    }
  };

  const performSearch = async () => {
    setIsSearching(true);
    try {
      const searchParams: any = {};
      
      if (searchTerm) searchParams.search = searchTerm;
      if (priceFilter) searchParams.price_category = priceFilter;
      if (durationFilter) searchParams.duration_category = durationFilter;
      if (categoryFilter) searchParams.category = parseInt(categoryFilter);
      
      const destinations = await destinationsApi.getDestinations(searchParams);
      
      const formattedResults = destinations.map((dest: Destination) => ({
        id: dest.id,
        name: dest.name,
        location: dest.location,
        price: Currency.format(dest.price),
        duration: dest.duration_display,
        rating: parseFloat(dest.rating),
        image: dest.image_url || '',
        category: dest.category?.name || ''
      }));
      
      setSearchResults(formattedResults);
      setShowResults(formattedResults.length > 0);
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
      {/* Hero Section - Mobile Optimized */}
      <section className="relative bg-gradient-to-r from-ghana-green to-ghana-blue text-white min-h-[50vh] sm:min-h-[60vh] lg:min-h-[70vh] flex items-center">
        <div className="absolute inset-0 bg-black/40"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
          <div className="text-center space-y-4 sm:space-y-6 lg:space-y-8">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white">
              Discover Ghana's
              <span className="block text-ghana-gold mt-1 sm:mt-2">Rich Heritage</span>
            </h1>
            <p className="text-base sm:text-lg lg:text-xl text-gray-200 max-w-3xl mx-auto px-4">
              Experience the beauty, culture, and history of Ghana with our comprehensive tour packages including transport, accommodation, meals, and medical support.
            </p>
            
            {/* Enhanced Search Bar - Mobile Optimized */}
            <div className="max-w-4xl mx-auto bg-white rounded-lg p-4 sm:p-6 shadow-lg" ref={searchResultsRef}>
              <div className="space-y-3 sm:space-y-4">
                {/* Main Search Row - Stack on Mobile */}
                <div className="flex flex-col gap-3 sm:gap-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4 sm:h-5 sm:w-5" />
                    <Input
                      type="text"
                      placeholder="Search destinations..."
                      className="pl-9 sm:pl-10 text-gray-900 h-11 sm:h-12 text-sm sm:text-base"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      onFocus={() => searchResults.length > 0 && setShowResults(true)}
                    />
                    {isSearching && (
                      <Loader2 className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4 sm:h-5 sm:w-5 animate-spin" />
                    )}
                  </div>
                  
                  <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                    <div className="relative flex-1">
                      <Calendar className="hidden sm:block absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5 pointer-events-none z-10" />
                      <Input
                        type="date"
                        className="px-3 sm:pl-10 text-gray-900 h-11 sm:h-12 text-sm sm:text-base w-full"
                        value={searchDate}
                        onChange={(e) => setSearchDate(e.target.value)}
                        placeholder="Select date"
                      />
                    </div>
                    <Button 
                      className="bg-ghana-gold hover:bg-ghana-gold/90 text-black font-semibold h-11 sm:h-12 text-sm sm:text-base px-6 whitespace-nowrap"
                      onClick={handleSearchSubmit}
                    >
                      Search Tours
                    </Button>
                  </div>
                </div>

                {/* Filters Row - Mobile Optimized */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Filter className="h-4 w-4 text-gray-500" />
                    <span className="text-xs sm:text-sm text-gray-600 font-medium">Filters:</span>
                  </div>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <Select value={priceFilter} onValueChange={setPriceFilter}>
                      <SelectTrigger className="w-full h-10 sm:h-11 text-sm sm:text-base">
                        <SelectValue placeholder="Price" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="budget">Budget (&lt; {Currency.symbol}300)</SelectItem>
                        <SelectItem value="mid">Mid-range ({Currency.symbol}300-600)</SelectItem>
                        <SelectItem value="luxury">Luxury (&gt; {Currency.symbol}600)</SelectItem>
                      </SelectContent>
                    </Select>

                    <Select value={durationFilter} onValueChange={setDurationFilter}>
                      <SelectTrigger className="w-full h-10 sm:h-11 text-sm sm:text-base">
                        <SelectValue placeholder="Duration" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="day">Day Trip</SelectItem>
                        <SelectItem value="weekend">Weekend (2-3 days)</SelectItem>
                        <SelectItem value="week">Week+ (4+ days)</SelectItem>
                      </SelectContent>
                    </Select>

                    <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                      <SelectTrigger className="w-full h-10 sm:h-11 text-sm sm:text-base">
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
                      className="text-gray-500 hover:text-gray-700 text-xs sm:text-sm"
                    >
                      <X className="h-4 w-4 mr-1" />
                      Clear
                    </Button>
                  )}
                </div>

                {/* Search Results Dropdown */}
                {showResults && searchResults.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-[60vh] sm:max-h-96 overflow-y-auto">
                    <div className="p-2 sm:p-3 border-b border-gray-100">
                      <div className="flex items-center justify-between">
                        <span className="text-xs sm:text-sm font-medium text-gray-700">
                          Found {searchResults.length} destination{searchResults.length !== 1 ? 's' : ''}
                        </span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowResults(false)}
                          className="h-6 w-6 p-0"
                        >
                          <X className="h-3 w-3 sm:h-4 sm:w-4" />
                        </Button>
                      </div>
                    </div>
                    <div className="max-h-[50vh] sm:max-h-80 overflow-y-auto">
                      {searchResults.map((result) => (
                        <Link
                          key={result.id}
                          to={`/tour/${result.id}`}
                          className="block p-3 sm:p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                          onClick={() => setShowResults(false)}
                        >
                          <div className="flex items-center space-x-3 sm:space-x-4">
                            <img
                              src={result.image || 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=100'}
                              alt={result.name}
                              className="w-14 h-14 sm:w-16 sm:h-16 object-cover rounded-lg flex-shrink-0"
                            />
                            <div className="flex-1 min-w-0">
                              <h4 className="font-semibold text-gray-900 text-sm sm:text-base truncate">{result.name}</h4>
                              <div className="flex items-center space-x-2 text-xs sm:text-sm text-gray-600">
                                <MapPin className="h-3 w-3 flex-shrink-0" />
                                <span className="truncate">{result.location}</span>
                                <span>•</span>
                                <Clock className="h-3 w-3 flex-shrink-0" />
                                <span className="truncate">{result.duration}</span>
                              </div>
                              <div className="flex items-center justify-between mt-1">
                                <div className="flex items-center space-x-1">
                                  <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                                  <span className="text-xs sm:text-sm font-medium">{result.rating}</span>
                                </div>
                                <span className="font-bold text-ghana-green text-xs sm:text-sm">{result.price}</span>
                              </div>
                            </div>
                          </div>
                        </Link>
                      ))}
                    </div>
                    <div className="p-2 sm:p-3 border-t border-gray-100">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleSearchSubmit}
                        className="w-full text-xs sm:text-sm"
                      >
                        View All Results
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-3 sm:gap-4 text-xs sm:text-sm px-4">
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Car className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Transport Included</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Hotel className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Quality Hotels</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Utensils className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Local Cuisine</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Shield className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Medical Support</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Tours - No Prices Displayed */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900">Featured Tours</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Discover our most popular destinations and experience the best of Ghana
            </p>
          </div>

          {isLoadingFeatured ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[...Array(4)].map((_, index) => (
                <Card key={index} className="overflow-hidden animate-pulse">
                  <div className="w-full h-48 bg-gray-300"></div>
                  <CardHeader className="pb-2">
                    <div className="h-4 bg-gray-300 rounded mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded w-2/3"></div>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <div className="h-3 bg-gray-300 rounded mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded w-3/4"></div>
                  </CardContent>
                  <CardFooter>
                    <div className="w-full h-10 bg-gray-300 rounded"></div>
                  </CardFooter>
                </Card>
              ))}
            </div>
          ) : featuredTours.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {featuredTours.map((tour) => (
                <Card key={tour.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="relative">
                    <img
                      src={tour.image_url || 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800'}
                      alt={tour.name}
                      className="w-full h-48 object-cover"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800';
                      }}
                    />
                    <Badge className="absolute top-2 right-2 bg-ghana-gold text-black">
                      {tour.duration_display}
                    </Badge>
                    {tour.is_featured && (
                      <Badge className="absolute top-2 left-2 bg-red-500 text-white">
                        Featured
                      </Badge>
                    )}
                  </div>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg line-clamp-2">
                      {tour.name}
                    </CardTitle>
                    <div className="flex items-center space-x-1 text-sm text-gray-600">
                      <MapPin className="h-4 w-4" />
                      <span>{tour.location}</span>
                    </div>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <CardDescription className="mb-3 line-clamp-2">
                      {tour.description}
                    </CardDescription>
                    <div className="flex items-center space-x-1 mb-3">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="font-semibold">{tour.rating}</span>
                      <span className="text-gray-500">({tour.reviews_count} reviews)</span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      <Badge variant="secondary" className="text-xs">
                        {tour.category.name}
                      </Badge>
                      {tour.highlights.slice(0, 2).map((highlight, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {highlight.highlight}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Link to={`/destinations/${tour.slug}`} className="w-full">
                      <Button className="w-full bg-ghana-green hover:bg-ghana-green/90">
                        Book Now
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No featured tours available at the moment.</p>
              <Link to="/destinations">
                <Button className="mt-4 bg-ghana-green hover:bg-ghana-green/90">
                  View All Destinations
                </Button>
              </Link>
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
      {isLoadingVideos ? (
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Experience Ghana Through Video</h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Watch immersive videos of our most popular destinations and get inspired for your next adventure
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(3)].map((_, index) => (
                <Card key={index} className="overflow-hidden animate-pulse">
                  <div className="w-full h-48 bg-gray-300"></div>
                  <CardHeader className="pb-2">
                    <div className="h-4 bg-gray-300 rounded mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded w-2/3"></div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="h-3 bg-gray-300 rounded mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded w-3/4"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      ) : featuredVideos.length > 0 ? (
        <VideoSection
          title="Experience Ghana Through Video"
          subtitle="Watch immersive videos of our most popular destinations and get inspired for your next adventure"
          videos={featuredVideos}
          maxVideos={3}
          layout="grid"
        />
      ) : (
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Experience Ghana Through Video</h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
                Watch immersive videos of our most popular destinations and get inspired for your next adventure
              </p>
              <p className="text-gray-500 text-lg">No featured videos available at the moment.</p>
              <Link to="/videos">
                <Button className="mt-4 bg-ghana-green hover:bg-ghana-green/90">
                  View All Videos
                </Button>
              </Link>
            </div>
          </div>
        </section>
      )}

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
