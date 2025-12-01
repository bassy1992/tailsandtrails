import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import { destinationsApi, Destination, Category } from "@/lib/api";
import { useToast } from "@/contexts/ToastContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapPin, Search, Star, Clock, Users, DollarSign, Filter } from "lucide-react";
import { Link } from "react-router-dom";

export default function Destinations() {
  const [searchTerm, setSearchTerm] = useState("");
  const [priceFilter, setPriceFilter] = useState("all");
  const [durationFilter, setDurationFilter] = useState("all");
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const { showError } = useToast();

  // Fetch destinations and categories on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [destinationsData, categoriesData] = await Promise.all([
          destinationsApi.getDestinations(),
          destinationsApi.getCategories()
        ]);
        setDestinations(destinationsData);
        setCategories(categoriesData);
      } catch (error) {
        console.error('Error fetching destinations:', error);
        showError('Failed to load destinations. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [showError]);

  // Fetch destinations when filters change
  useEffect(() => {
    const fetchFilteredDestinations = async () => {
      try {
        const params: any = {};
        
        if (searchTerm) params.search = searchTerm;
        if (priceFilter !== "all") params.price_category = priceFilter;
        if (durationFilter !== "all") params.duration_category = durationFilter;

        const data = await destinationsApi.getDestinations(params);
        setDestinations(data);
      } catch (error) {
        console.error('Error filtering destinations:', error);
        showError('Failed to filter destinations. Please try again.');
      }
    };

    // Only fetch if not initial load
    if (!loading) {
      fetchFilteredDestinations();
    }
  }, [searchTerm, priceFilter, durationFilter, loading, showError]);
  // Dynamic categories from API
  const categoryNames = ["All", ...categories.map(cat => cat.name)];

  return (
    <Layout>
      {/* Header */}
      <section className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold">Explore Ghana's Destinations</h1>
            <p className="text-xl text-gray-200 max-w-3xl mx-auto">
              From historic castles to pristine rainforests, discover the diverse beauty of Ghana with our carefully curated tour packages.
            </p>
          </div>
        </div>
      </section>

      {/* Filters and Search */}
      <section className="py-8 bg-gray-50 border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
            {/* Search */}
            <div className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  type="text"
                  placeholder="Search destinations..."
                  className="pl-10"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>

            {/* Filters */}
            <div className="flex flex-wrap gap-4 items-center">
              <div className="flex items-center space-x-2">
                <Filter className="h-5 w-5 text-gray-600" />
                <span className="font-medium text-gray-700">Filter by:</span>
              </div>
              
              <Select value={priceFilter} onValueChange={setPriceFilter}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Price" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Prices</SelectItem>
                  <SelectItem value="budget">Budget (&lt; GH₵300)</SelectItem>
                  <SelectItem value="mid">Mid-range (GH₵300-600)</SelectItem>
                  <SelectItem value="luxury">Luxury (&gt; GH₵600)</SelectItem>
                </SelectContent>
              </Select>

              <Select value={durationFilter} onValueChange={setDurationFilter}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Duration" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Durations</SelectItem>
                  <SelectItem value="day">Day Tours</SelectItem>
                  <SelectItem value="weekend">Weekend (2-3 Days)</SelectItem>
                  <SelectItem value="week">Extended (4+ Days)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Category Tags */}
          <div className="flex flex-wrap gap-2 mt-6">
            {categoryNames.map((category) => (
              <Badge
                key={category}
                variant={category === "All" ? "default" : "secondary"}
                className="cursor-pointer hover:bg-ghana-green hover:text-white transition-colors px-3 py-1"
              >
                {category}
              </Badge>
            ))}
          </div>
        </div>
      </section>

      {/* Destinations Grid */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading && (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ghana-green"></div>
            </div>
          )}

          {!loading && (
            <>
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {destinations.length} Tour{destinations.length !== 1 ? 's' : ''} Available
              </h2>
              <p className="text-gray-600">Choose your perfect Ghana adventure</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {destinations.map((destination) => (
              <Card key={destination.id} className="overflow-hidden hover:shadow-xl transition-all duration-300 group">
                <div className="relative overflow-hidden">
                  <img
                    src={destination.image}
                    alt={destination.name}
                    className="w-full h-56 object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute top-4 left-4">
                    <Badge className="bg-ghana-gold text-black font-semibold">
                      {destination.category.name}
                    </Badge>
                  </div>
                  <div className="absolute top-4 right-4">
                    <Badge variant="secondary" className="bg-white/90">
                      {destination.duration_display}
                    </Badge>
                  </div>
                </div>

                <CardHeader className="pb-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-xl mb-1 group-hover:text-ghana-green transition-colors">
                        {destination.name}
                      </CardTitle>
                      <div className="flex items-center text-gray-600 mb-2">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span className="text-sm">{destination.location}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-ghana-green">GH₵{destination.price}</div>
                      <div className="text-xs text-gray-500">per person</div>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <CardDescription className="text-sm leading-relaxed">
                    {destination.description}
                  </CardDescription>

                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-1">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="font-semibold">{destination.rating}</span>
                      <span className="text-gray-500">({destination.reviews_count})</span>
                    </div>
                    <div className="flex items-center space-x-1 text-gray-600">
                      <Users className="h-4 w-4" />
                      <span>Max {destination.max_group_size}</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="text-sm font-semibold text-gray-700">Highlights:</div>
                    <div className="flex flex-wrap gap-1">
                      {destination.highlights.slice(0, 3).map((highlight, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {highlight.highlight}
                        </Badge>
                      ))}
                      {destination.highlights.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{destination.highlights.length - 3} more
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardContent>

                <CardFooter className="pt-2">
                  <Link to={`/tour/${destination.slug}`} className="block w-full">
                    <Button className="w-full bg-ghana-green hover:bg-ghana-green/90">
                      View Details
                    </Button>
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>

          {!loading && destinations.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-500 mb-4">
                <Search className="h-16 w-16 mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-semibold mb-2">No destinations found</h3>
                <p>Try adjusting your search or filter criteria</p>
              </div>
              <Button 
                onClick={() => {
                  setSearchTerm("");
                  setPriceFilter("all");
                  setDurationFilter("all");
                }}
                variant="outline"
              >
                Clear Filters
              </Button>
            </div>
          )}
          </>
          )}
        </div>
      </section>

      {/* Call to Action */}
      <section className="bg-ghana-green text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl font-bold">Can't Find What You're Looking For?</h2>
          <p className="text-xl text-gray-200">
            Our team can create a custom tour package tailored to your preferences and budget.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/contact">
              <Button size="lg" className="bg-ghana-gold hover:bg-ghana-gold/90 text-black">
                Custom Tour Request
              </Button>
            </Link>
            <Link to="/about">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-ghana-green">
                Learn More About Us
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
