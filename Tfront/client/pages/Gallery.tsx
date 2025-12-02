import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { VisuallyHidden } from "@/components/ui/visually-hidden";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Camera, MapPin, Calendar, Filter, Video, Play, Clock, Eye, Loader2 } from "lucide-react";
import { Link } from "react-router-dom";
import { galleryApi, GalleryCategory, GalleryImage, GalleryVideo } from "@/lib/api";

export default function Gallery() {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [activeTab, setActiveTab] = useState("photos");
  const [categories, setCategories] = useState<GalleryCategory[]>([]);
  const [images, setImages] = useState<GalleryImage[]>([]);
  const [videos, setVideos] = useState<GalleryVideo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch gallery data from API
  useEffect(() => {
    const fetchGalleryData = async () => {
      try {
        setLoading(true);
        const [categoriesData, imagesData, videosData] = await Promise.all([
          galleryApi.getCategories(),
          galleryApi.getImages(),
          galleryApi.getVideos()
        ]);
        setCategories(categoriesData);
        setImages(imagesData);
        setVideos(videosData);
        setError(null);
      } catch (err: any) {
        console.error('Error fetching gallery data:', err);
        setError(err.message || 'Failed to load gallery data');
      } finally {
        setLoading(false);
      }
    };

    fetchGalleryData();
  }, []);

  const filteredImages = selectedCategory === "all" 
    ? images 
    : images.filter(img => img.category_name?.toLowerCase() === selectedCategory || 
                           categories.find(c => c.id === img.category)?.slug === selectedCategory);

  const filteredVideos = selectedCategory === "all" 
    ? videos 
    : videos.filter(video => video.category_name?.toLowerCase() === selectedCategory || 
                             categories.find(c => c.id === video.category)?.slug === selectedCategory);

  const imageCount = filteredImages.length;
  const videoCount = filteredVideos.length;

  // Build category list with "All" option
  const categoryOptions = [
    { key: "all", label: "All", count: images.length + videos.length },
    ...categories.map(cat => ({
      key: cat.slug,
      label: cat.name,
      count: cat.image_count + cat.video_count
    }))
  ];

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
                <span>{images.length} Photos</span>
              </div>
              <div className="flex items-center space-x-2">
                <Video className="h-5 w-5" />
                <span>{videos.length} Videos</span>
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
            {categoryOptions.map((category) => (
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
                {category.count > 0 && (
                  <span className="ml-2 text-xs opacity-75">({category.count})</span>
                )}
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

              {loading ? (
                <div className="flex justify-center items-center py-12">
                  <Loader2 className="h-8 w-8 animate-spin text-ghana-green" />
                  <span className="ml-3 text-gray-600">Loading images...</span>
                </div>
              ) : error ? (
                <div className="text-center py-12">
                  <p className="text-red-600 mb-4">{error}</p>
                  <Button onClick={() => window.location.reload()}>Retry</Button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {filteredImages.map((image) => (
                    <Dialog key={image.id}>
                      <DialogTrigger asChild>
                        <Card className="overflow-hidden cursor-pointer group hover:shadow-xl transition-all duration-300">
                          <div className="relative">
                            <img
                              src={image.thumbnail_url || image.image_url}
                              alt={image.title}
                              className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
                            />
                            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300"></div>
                            {image.category_name && (
                              <div className="absolute top-3 left-3">
                                <Badge className="bg-ghana-gold text-black font-semibold">
                                  {image.category_name}
                                </Badge>
                              </div>
                            )}
                            {image.is_featured && (
                              <div className="absolute top-3 right-3">
                                <Badge className="bg-ghana-green text-white font-semibold">
                                  Featured
                                </Badge>
                              </div>
                            )}
                          </div>
                          <CardContent className="p-4">
                            <h3 className="font-semibold text-lg mb-1 group-hover:text-ghana-green transition-colors">
                              {image.title}
                            </h3>
                            {image.location && (
                              <div className="flex items-center text-gray-600 mb-2">
                                <MapPin className="h-4 w-4 mr-1" />
                                <span className="text-sm">{image.location}</span>
                              </div>
                            )}
                            {image.description && (
                              <p className="text-sm text-gray-500 leading-relaxed line-clamp-2">
                                {image.description}
                              </p>
                            )}
                          </CardContent>
                        </Card>
                      </DialogTrigger>
                      <DialogContent className="max-w-4xl max-h-[90vh] p-0">
                        <VisuallyHidden>
                          <DialogTitle>{image.title}</DialogTitle>
                        </VisuallyHidden>
                        <div className="relative">
                          <img
                            src={image.image_url}
                            alt={image.title}
                            className="w-full h-auto max-h-[80vh] object-contain"
                          />
                          <div className="p-6 bg-white">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{image.title}</h3>
                                {image.location && (
                                  <div className="flex items-center text-gray-600 mb-3">
                                    <MapPin className="h-5 w-5 mr-2" />
                                    <span className="text-lg">{image.location}</span>
                                  </div>
                                )}
                                {image.photographer && (
                                  <p className="text-sm text-gray-500 mb-2">Photo by: {image.photographer}</p>
                                )}
                                {image.description && (
                                  <p className="text-gray-700 leading-relaxed">{image.description}</p>
                                )}
                              </div>
                              {image.category_name && (
                                <Badge className="bg-ghana-gold text-black font-semibold ml-4">
                                  {image.category_name}
                                </Badge>
                              )}
                            </div>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                  ))}
                </div>
              )}

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

              {loading ? (
                <div className="flex justify-center items-center py-12">
                  <Loader2 className="h-8 w-8 animate-spin text-ghana-green" />
                  <span className="ml-3 text-gray-600">Loading videos...</span>
                </div>
              ) : error ? (
                <div className="text-center py-12">
                  <p className="text-red-600 mb-4">{error}</p>
                  <Button onClick={() => window.location.reload()}>Retry</Button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {filteredVideos.map((video) => {
                    // Check if it's a YouTube or Vimeo URL
                    const isYouTube = video.video_url.includes('youtube.com') || video.video_url.includes('youtu.be');
                    const isVimeo = video.video_url.includes('vimeo.com');
                    
                    return (
                      <Card key={video.id} className="overflow-hidden hover:shadow-xl transition-all duration-300 group">
                        <div className="relative cursor-pointer">
                          <img
                            src={video.thumbnail_url || 'https://via.placeholder.com/600x400?text=Video'}
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
                                  {isYouTube || isVimeo ? (
                                    <iframe
                                      src={video.video_url}
                                      className="w-full aspect-video"
                                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                      allowFullScreen
                                    />
                                  ) : (
                                    <video
                                      controls
                                      autoPlay
                                      className="w-full h-auto max-h-[80vh]"
                                      poster={video.thumbnail_url}
                                    >
                                      <source src={video.video_url} type="video/mp4" />
                                      Your browser does not support the video tag.
                                    </video>
                                  )}
                                  <div className="p-6 bg-white">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{video.title}</h3>
                                    <div className="flex items-center text-gray-600 mb-3 flex-wrap gap-3">
                                      {video.duration && (
                                        <div className="flex items-center">
                                          <Clock className="h-5 w-5 mr-2" />
                                          <span>{video.duration}</span>
                                        </div>
                                      )}
                                    </div>
                                    {video.description && (
                                      <p className="text-gray-700">{video.description}</p>
                                    )}
                                  </div>
                                </div>
                              </DialogContent>
                            </Dialog>
                          </div>
                          {video.category_name && (
                            <div className="absolute top-3 left-3">
                              <Badge className="bg-ghana-gold text-black font-semibold">
                                {video.category_name}
                              </Badge>
                            </div>
                          )}
                          {video.is_featured && (
                            <div className="absolute top-3 right-3">
                              <Badge className="bg-ghana-green text-white font-semibold">
                                Featured
                              </Badge>
                            </div>
                          )}
                          {video.duration && (
                            <div className="absolute bottom-3 right-3 bg-black/70 text-white px-2 py-1 rounded text-sm">
                              {video.duration}
                            </div>
                          )}
                        </div>

                        <CardHeader className="pb-2">
                          <CardTitle className="text-lg leading-tight group-hover:text-ghana-green transition-colors">
                            {video.title}
                          </CardTitle>
                        </CardHeader>

                        <CardContent className="pt-0">
                          {video.description && (
                            <CardDescription className="text-sm leading-relaxed line-clamp-3">
                              {video.description}
                            </CardDescription>
                          )}
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              )}

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
