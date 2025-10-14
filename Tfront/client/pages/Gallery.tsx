import { useState } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { VisuallyHidden } from "@/components/ui/visually-hidden";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Camera, MapPin, Calendar, Filter, Video, Play, Clock, Eye } from "lucide-react";
import { Link } from "react-router-dom";

export default function Gallery() {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [activeTab, setActiveTab] = useState("photos");

  const galleryImages = [
    {
      id: 1,
      src: "https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Cape Coast Castle",
      location: "Cape Coast",
      category: "heritage",
      description: "Historic architecture of the UNESCO World Heritage Site"
    },
    {
      id: 2,
      src: "https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Aburi Botanical Gardens",
      location: "Aburi",
      category: "nature",
      description: "Lush gardens with stunning mountain views"
    },
    {
      id: 3,
      src: "https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Kumasi Street Life",
      location: "Kumasi",
      category: "culture",
      description: "Vibrant street culture and local fashion"
    },
    {
      id: 4,
      src: "https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Forest Canopy Walk",
      location: "Kakum National Park",
      category: "adventure",
      description: "Thrilling canopy walk through pristine rainforest"
    },
    {
      id: 5,
      src: "https://images.pexels.com/photos/30211750/pexels-photo-30211750.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Accra Coastline",
      location: "Accra",
      category: "coastal",
      description: "Beautiful sandy beaches with traditional fishing boats"
    },
    {
      id: 6,
      src: "https://images.pexels.com/photos/15887695/pexels-photo-15887695.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Street Vendors",
      location: "Accra",
      category: "culture",
      description: "Local entrepreneurs and vibrant street life"
    },
    {
      id: 7,
      src: "https://images.pexels.com/photos/5110556/pexels-photo-5110556.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Coastal Fort",
      location: "Ghana Coast",
      category: "heritage",
      description: "Historic coastal fortifications and serene beaches"
    },
    {
      id: 8,
      src: "https://images.pexels.com/photos/32981288/pexels-photo-32981288.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Traditional Architecture",
      location: "Northern Ghana",
      category: "heritage",
      description: "Ancient mosque with distinctive Sudano-Sahelian architecture"
    },
    {
      id: 9,
      src: "https://images.pexels.com/photos/12190172/pexels-photo-12190172.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Volta River",
      location: "Volta Region",
      category: "nature",
      description: "Peaceful river journey through lush landscapes"
    },
    {
      id: 10,
      src: "https://images.pexels.com/photos/3561167/pexels-photo-3561167.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Elmina Market",
      location: "Elmina",
      category: "culture",
      description: "Bustling local market near historic Elmina Castle"
    },
    {
      id: 11,
      src: "https://images.pexels.com/photos/33475234/pexels-photo-33475234.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Mountain Waterfalls",
      location: "Volta Region",
      category: "nature",
      description: "Spectacular waterfalls in Ghana's mountainous regions"
    },
    {
      id: 12,
      src: "https://images.pexels.com/photos/7803877/pexels-photo-7803877.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Traditional Fashion",
      location: "Ghana",
      category: "culture",
      description: "Beautiful traditional Ghanaian clothing and headwrap"
    },
    {
      id: 13,
      src: "https://images.pexels.com/photos/33489790/pexels-photo-33489790.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Local Market Scene",
      location: "Various",
      category: "culture",
      description: "Authentic market experiences and local produce"
    },
    {
      id: 14,
      src: "https://images.pexels.com/photos/1422408/pexels-photo-1422408.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Modern Accra",
      location: "Accra",
      category: "urban",
      description: "Contemporary architecture and urban development"
    },
    {
      id: 15,
      src: "https://images.pexels.com/photos/33500839/pexels-photo-33500839.jpeg?auto=compress&cs=tinysrgb&w=800",
      title: "Wildlife Encounter",
      location: "National Parks",
      category: "adventure",
      description: "Close encounters with Ghana's diverse wildlife"
    }
  ];

  const galleryVideos = [
    {
      id: 1,
      title: "Cape Coast Castle - A Journey Through History",
      description: "Explore the historic Cape Coast Castle and learn about its significance in Ghana's heritage. This immersive documentary takes you through centuries of history.",
      thumbnail: "https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/29603787/12740641_640_360_60fps.mp4",
      duration: "8:45",
      views: "12.5K",
      category: "heritage",
      location: "Cape Coast"
    },
    {
      id: 2,
      title: "Kakum National Park Canopy Adventure",
      description: "Experience the breathtaking canopy walk 40 meters above the forest floor. Join us on this thrilling adventure through Ghana's pristine rainforest.",
      thumbnail: "https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/17844988/17844988-sd_240_426_30fps.mp4",
      duration: "6:30",
      views: "8.9K",
      category: "adventure",
      location: "Kakum National Park"
    },
    {
      id: 3,
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
      id: 4,
      title: "Ashanti Culture & Traditions",
      description: "Immerse yourself in the rich Ashanti culture. Visit Manhyia Palace, witness traditional ceremonies, and learn about ancient customs that live on today.",
      thumbnail: "https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/7823374/7823374-hd_720_1280_60fps.mp4",
      duration: "12:20",
      views: "9.7K",
      category: "culture",
      location: "Kumasi"
    },
    {
      id: 5,
      title: "Ghana's Golden Beaches",
      description: "Relax on Ghana's pristine beaches along the Atlantic coast. From fishing villages to luxury resorts, experience coastal Ghana at its finest.",
      thumbnail: "https://images.pexels.com/photos/30211750/pexels-photo-30211750.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/19019788/19019788-sd_240_426_30fps.mp4",
      duration: "7:55",
      views: "11.3K",
      category: "coastal",
      location: "Ghana Coast"
    },
    {
      id: 6,
      title: "Accra City Life & Modern Ghana",
      description: "Experience the vibrant capital city of Accra. From bustling markets to modern architecture, see how tradition meets modernity in Ghana's heartbeat.",
      thumbnail: "https://images.pexels.com/photos/1422408/pexels-photo-1422408.jpeg?auto=compress&cs=tinysrgb&w=600",
      videoUrl: "https://videos.pexels.com/video-files/32156428/13711037_360_640_50fps.mp4",
      duration: "9:10",
      views: "13.8K",
      category: "urban",
      location: "Accra"
    }
  ];

  const categories = [
    { key: "all", label: "All" },
    { key: "heritage", label: "Heritage" },
    { key: "nature", label: "Nature" },
    { key: "culture", label: "Culture" },
    { key: "adventure", label: "Adventure" },
    { key: "coastal", label: "Coastal" },
    { key: "urban", label: "Urban" }
  ];

  const filteredImages = selectedCategory === "all" 
    ? galleryImages 
    : galleryImages.filter(img => img.category === selectedCategory);

  const filteredVideos = selectedCategory === "all" 
    ? galleryVideos 
    : galleryVideos.filter(video => video.category === selectedCategory);

  const getTabCounts = () => {
    const imageCount = selectedCategory === "all" ? galleryImages.length : galleryImages.filter(img => img.category === selectedCategory).length;
    const videoCount = selectedCategory === "all" ? galleryVideos.length : galleryVideos.filter(video => video.category === selectedCategory).length;
    return { imageCount, videoCount };
  };

  const { imageCount, videoCount } = getTabCounts();

  return (
    <Layout>
      {/* Header */}
      <section className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Camera className="h-8 w-8 text-ghana-gold" />
              <h1 className="text-4xl md:text-5xl font-bold">Media Gallery</h1>
            </div>
            <p className="text-xl text-gray-200 max-w-3xl mx-auto">
              Discover the breathtaking beauty of Ghana through our curated collection of photos and videos. 
              From historic castles to pristine nature reserves, experience Ghana's diverse landscapes and rich culture.
            </p>
            <div className="flex items-center justify-center space-x-6 text-sm mt-8">
              <div className="flex items-center space-x-2">
                <MapPin className="h-5 w-5" />
                <span>15+ Destinations</span>
              </div>
              <div className="flex items-center space-x-2">
                <Camera className="h-5 w-5" />
                <span>{galleryImages.length} Photos</span>
              </div>
              <div className="flex items-center space-x-2">
                <Video className="h-5 w-5" />
                <span>{galleryVideos.length} Videos</span>
              </div>
              <div className="flex items-center space-x-2">
                <Calendar className="h-5 w-5" />
                <span>Updated Daily</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Filter Categories */}
      <section className="py-8 bg-gray-50 border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-4 mb-6">
            <Filter className="h-5 w-5 text-gray-600" />
            <span className="font-medium text-gray-700">Filter by Category:</span>
          </div>
          <div className="flex flex-wrap gap-3">
            {categories.map((category) => (
              <Button
                key={category.key}
                variant={selectedCategory === category.key ? "default" : "outline"}
                onClick={() => setSelectedCategory(category.key)}
                className={`${
                  selectedCategory === category.key
                    ? "bg-ghana-green hover:bg-ghana-green/90 text-white"
                    : "border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white"
                } transition-colors`}
              >
                {category.label}
              </Button>
            ))}
          </div>
        </div>
      </section>

      {/* Tabs for Photos and Videos */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto mb-8">
              <TabsTrigger value="photos" className="flex items-center space-x-2">
                <Camera className="h-4 w-4" />
                <span>Photos ({imageCount})</span>
              </TabsTrigger>
              <TabsTrigger value="videos" className="flex items-center space-x-2">
                <Video className="h-4 w-4" />
                <span>Videos ({videoCount})</span>
              </TabsTrigger>
            </TabsList>

            {/* Photos Tab */}
            <TabsContent value="photos" className="space-y-8">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Photo Gallery</h2>
                <p className="text-gray-600">{imageCount} photo{imageCount !== 1 ? 's' : ''} found</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredImages.map((image) => (
                  <Dialog key={image.id}>
                    <DialogTrigger asChild>
                      <Card className="overflow-hidden cursor-pointer group hover:shadow-xl transition-all duration-300">
                        <div className="relative">
                          <img
                            src={image.src}
                            alt={image.title}
                            className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
                          />
                          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300"></div>
                          <div className="absolute top-3 left-3">
                            <Badge className="bg-ghana-gold text-black font-semibold">
                              {image.category.charAt(0).toUpperCase() + image.category.slice(1)}
                            </Badge>
                          </div>
                        </div>
                        <CardContent className="p-4">
                          <h3 className="font-semibold text-lg mb-1 group-hover:text-ghana-green transition-colors">
                            {image.title}
                          </h3>
                          <div className="flex items-center text-gray-600 mb-2">
                            <MapPin className="h-4 w-4 mr-1" />
                            <span className="text-sm">{image.location}</span>
                          </div>
                          <p className="text-sm text-gray-500 leading-relaxed">
                            {image.description}
                          </p>
                        </CardContent>
                      </Card>
                    </DialogTrigger>
                    <DialogContent className="max-w-4xl max-h-[90vh] p-0">
                      <VisuallyHidden>
                        <DialogTitle>{image.title}</DialogTitle>
                      </VisuallyHidden>
                      <div className="relative">
                        <img
                          src={image.src.replace('w=800', 'w=1200')}
                          alt={image.title}
                          className="w-full h-auto max-h-[80vh] object-contain"
                        />
                        <div className="p-6 bg-white">
                          <div className="flex items-start justify-between">
                            <div>
                              <h3 className="text-2xl font-bold text-gray-900 mb-2">{image.title}</h3>
                              <div className="flex items-center text-gray-600 mb-3">
                                <MapPin className="h-5 w-5 mr-2" />
                                <span className="text-lg">{image.location}</span>
                              </div>
                              <p className="text-gray-700 leading-relaxed">{image.description}</p>
                            </div>
                            <Badge className="bg-ghana-gold text-black font-semibold ml-4">
                              {image.category.charAt(0).toUpperCase() + image.category.slice(1)}
                            </Badge>
                          </div>
                        </div>
                      </div>
                    </DialogContent>
                  </Dialog>
                ))}
              </div>

              {filteredImages.length === 0 && (
                <div className="text-center py-12">
                  <Camera className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-xl font-semibold text-gray-600 mb-2">No photos found</h3>
                  <p className="text-gray-500">Try selecting a different category</p>
                </div>
              )}
            </TabsContent>

            {/* Videos Tab */}
            <TabsContent value="videos" className="space-y-8">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Video Gallery</h2>
                <p className="text-gray-600">{videoCount} video{videoCount !== 1 ? 's' : ''} found</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {filteredVideos.map((video) => (
                  <Card key={video.id} className="overflow-hidden hover:shadow-xl transition-all duration-300 group">
                    <div className="relative cursor-pointer">
                      <img
                        src={video.thumbnail}
                        alt={video.title}
                        className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all duration-300 flex items-center justify-center">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button
                              size="lg"
                              className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-ghana-gold hover:bg-ghana-gold/90 text-black"
                            >
                              <Play className="h-5 w-5 mr-2" />
                              Play
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-4xl max-h-[90vh] p-0">
                            <VisuallyHidden>
                              <DialogTitle>{video.title}</DialogTitle>
                            </VisuallyHidden>
                            <div className="relative">
                              <video
                                controls
                                autoPlay
                                className="w-full h-auto max-h-[80vh]"
                                poster={video.thumbnail}
                              >
                                <source src={video.videoUrl} type="video/mp4" />
                                Your browser does not support the video tag.
                              </video>
                              <div className="p-6 bg-white">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{video.title}</h3>
                                <div className="flex items-center text-gray-600 mb-3">
                                  <MapPin className="h-5 w-5 mr-2" />
                                  <span className="mr-4">{video.location}</span>
                                  <Clock className="h-5 w-5 mr-2" />
                                  <span className="mr-4">{video.duration}</span>
                                  <Eye className="h-5 w-5 mr-2" />
                                  <span>{video.views} views</span>
                                </div>
                                <p className="text-gray-700">{video.description}</p>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      </div>
                      <div className="absolute top-3 left-3">
                        <Badge className="bg-ghana-gold text-black font-semibold">
                          {video.category.charAt(0).toUpperCase() + video.category.slice(1)}
                        </Badge>
                      </div>
                      <div className="absolute bottom-3 right-3 bg-black/70 text-white px-2 py-1 rounded text-sm">
                        {video.duration}
                      </div>
                    </div>

                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg leading-tight group-hover:text-ghana-green transition-colors">
                        {video.title}
                      </CardTitle>
                      <div className="flex items-center text-gray-600 text-sm">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span className="mr-3">{video.location}</span>
                        <Eye className="h-4 w-4 mr-1" />
                        <span>{video.views} views</span>
                      </div>
                    </CardHeader>

                    <CardContent className="pt-0">
                      <CardDescription className="text-sm leading-relaxed">
                        {video.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {filteredVideos.length === 0 && (
                <div className="text-center py-12">
                  <Video className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-xl font-semibold text-gray-600 mb-2">No videos found</h3>
                  <p className="text-gray-500">Try selecting a different category</p>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Call to Action */}
      <section className="bg-ghana-green text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl font-bold">Ready to Experience These Places?</h2>
          <p className="text-xl text-gray-200">
            These stunning destinations are waiting for you. Book your Ghana adventure today and create your own unforgettable memories.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/destinations">
              <Button size="lg" className="bg-ghana-gold hover:bg-ghana-gold/90 text-black">
                Book a Tour
              </Button>
            </Link>
            <Link to="/destinations">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-ghana-green">
                View Destinations
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
