import { useState } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { VisuallyHidden } from "@/components/ui/visually-hidden";
import { Play, MapPin, Clock, Eye, Filter, Video } from "lucide-react";
import { Link } from "react-router-dom";

export default function Videos() {
  const [selectedCategory, setSelectedCategory] = useState("all");

  const videoContent = [
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
    { key: "all", label: "All Videos", count: videoContent.length },
    { key: "heritage", label: "Heritage", count: videoContent.filter(video => video.category === "heritage").length },
    { key: "nature", label: "Nature", count: videoContent.filter(video => video.category === "nature").length },
    { key: "culture", label: "Culture", count: videoContent.filter(video => video.category === "culture").length },
    { key: "adventure", label: "Adventure", count: videoContent.filter(video => video.category === "adventure").length },
    { key: "coastal", label: "Coastal", count: videoContent.filter(video => video.category === "coastal").length },
    { key: "urban", label: "Urban", count: videoContent.filter(video => video.category === "urban").length }
  ];

  const filteredVideos = selectedCategory === "all" 
    ? videoContent 
    : videoContent.filter(video => video.category === selectedCategory);

  return (
    <Layout>
      {/* Header */}
      <section className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Video className="h-8 w-8 text-ghana-gold" />
              <h1 className="text-4xl md:text-5xl font-bold">Video Gallery</h1>
            </div>
            <p className="text-xl text-gray-200 max-w-3xl mx-auto">
              Watch immersive videos showcasing Ghana's stunning destinations, rich culture, and unforgettable experiences. 
              Get inspired for your next adventure through our curated video collection.
            </p>
            <div className="flex items-center justify-center space-x-6 text-sm mt-8">
              <div className="flex items-center space-x-2">
                <MapPin className="h-5 w-5" />
                <span>15+ Destinations</span>
              </div>
              <div className="flex items-center space-x-2">
                <Video className="h-5 w-5" />
                <span>{videoContent.length} Videos</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5" />
                <span>60+ Minutes</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Video Section */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Featured Video</h2>
            <p className="text-gray-600">Start your journey with our most popular destination video</p>
          </div>
          
          <div className="max-w-4xl mx-auto">
            <Card className="overflow-hidden">
              <div className="relative group cursor-pointer">
                <img
                  src={videoContent[2].thumbnail}
                  alt={videoContent[2].title}
                  className="w-full h-80 object-cover"
                />
                <div className="absolute inset-0 bg-black/40 group-hover:bg-black/50 transition-all duration-300 flex items-center justify-center">
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button size="lg" className="bg-ghana-gold hover:bg-ghana-gold/90 text-black">
                        <Play className="h-6 w-6 mr-2" />
                        Watch Now
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="max-w-4xl max-h-[90vh] p-0">
                      <VisuallyHidden>
                        <DialogTitle>{videoContent[2].title}</DialogTitle>
                      </VisuallyHidden>
                      <div className="relative">
                        <video
                          controls
                          autoPlay
                          className="w-full h-auto max-h-[80vh]"
                          poster={videoContent[2].thumbnail}
                        >
                          <source src={videoContent[2].videoUrl} type="video/mp4" />
                          Your browser does not support the video tag.
                        </video>
                      </div>
                    </DialogContent>
                  </Dialog>
                </div>
                <Badge className="absolute top-4 left-4 bg-ghana-gold text-black">
                  Featured
                </Badge>
                <div className="absolute bottom-4 right-4 bg-black/70 text-white px-2 py-1 rounded text-sm">
                  {videoContent[2].duration}
                </div>
              </div>
              <CardContent className="p-6">
                <h3 className="text-2xl font-bold mb-2">{videoContent[2].title}</h3>
                <div className="flex items-center text-gray-600 mb-3">
                  <MapPin className="h-4 w-4 mr-1" />
                  <span className="mr-4">{videoContent[2].location}</span>
                  <Eye className="h-4 w-4 mr-1" />
                  <span>{videoContent[2].views} views</span>
                </div>
                <p className="text-gray-700">{videoContent[2].description}</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Filter Categories */}
      <section className="py-8 bg-white border-b">
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
                <Badge 
                  variant="secondary" 
                  className={`ml-2 ${
                    selectedCategory === category.key ? "bg-white/20 text-white" : "bg-ghana-green/10 text-ghana-green"
                  }`}
                >
                  {category.count}
                </Badge>
              </Button>
            ))}
          </div>
        </div>
      </section>

      {/* Video Grid */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900">
              {selectedCategory === "all" ? "All Videos" : categories.find(c => c.key === selectedCategory)?.label}
            </h2>
            <p className="text-gray-600">
              {filteredVideos.length} video{filteredVideos.length !== 1 ? 's' : ''} available
            </p>
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
        </div>
      </section>

      {/* Video Upload Section for Admin */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Card className="border-2 border-dashed border-ghana-green/30">
            <CardContent className="p-8 space-y-6">
              <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto">
                <Video className="h-8 w-8 text-ghana-green" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Share Your Ghana Experience</h3>
                <p className="text-gray-600 leading-relaxed">
                  Have amazing footage from your Ghana tour? We'd love to feature your videos in our gallery! 
                  Share your experiences and inspire other travelers to discover Ghana's beauty.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/contact">
                  <Button size="lg" className="bg-ghana-green hover:bg-ghana-green/90">
                    Submit Your Video
                  </Button>
                </Link>
                <Link to="/destinations">
                  <Button size="lg" variant="outline" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                    Book Your Tour
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Call to Action */}
      <section className="bg-ghana-green text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl font-bold">Ready to Create Your Own Adventure?</h2>
          <p className="text-xl text-gray-200">
            These videos showcase just a glimpse of what Ghana has to offer. Book your tour today and experience 
            these incredible destinations firsthand.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/destinations">
              <Button size="lg" className="bg-ghana-gold hover:bg-ghana-gold/90 text-black">
                Explore Destinations
              </Button>
            </Link>
            <Link to="/contact">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-ghana-green">
                Plan Custom Tour
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
