import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { VisuallyHidden } from "@/components/ui/visually-hidden";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Camera, MapPin, Calendar, Filter, Video, Play, Clock, Eye, Loader2, ChevronLeft, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import { galleryApi, GalleryCategory, ImageGallery, GalleryVideo } from "@/lib/api";
import { useToast } from "@/contexts/ToastContext";

export default function Gallery() {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [activeTab, setActiveTab] = useState("photos");
  const [categories, setCategories] = useState<GalleryCategory[]>([]);
  const [galleries, setGalleries] = useState<ImageGallery[]>([]);
  const [videos, setVideos] = useState<GalleryVideo[]>([]);
  const [selectedGallery, setSelectedGallery] = useState<ImageGallery | null>(null);
  const [isGalleryModalOpen, setIsGalleryModalOpen] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [galleryLoading, setGalleryLoading] = useState(false);
  const [videoLoading, setVideoLoading] = useState(false);
  const [galleryDetailLoading, setGalleryDetailLoading] = useState(false);
  const { showError } = useToast();

  // Fetch data on component mount
  useEffect(() => {
    fetchInitialData();
  }, []);

  // Fetch data when category changes
  useEffect(() => {
    if (categories.length > 0) {
      fetchGalleries();
      fetchVideos();
    }
  }, [selectedCategory, categories]);

  // Keyboard navigation for slider
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (isGalleryModalOpen && selectedGallery?.images) {
        if (event.key === 'ArrowLeft') {
          prevImage();
        } else if (event.key === 'ArrowRight') {
          nextImage();
        } else if (event.key === 'Escape') {
          setIsGalleryModalOpen(false);
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isGalleryModalOpen, selectedGallery]);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      const categoriesData = await galleryApi.getCategories();
      setCategories(categoriesData);
    } catch (error) {
      console.error('Error fetching gallery data:', error);
      showError('Failed to load gallery data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchGalleries = async () => {
    try {
      setGalleryLoading(true);
      const params = selectedCategory !== "all" ? { category: selectedCategory } : {};
      const galleriesData = await galleryApi.getGalleries(params);
      setGalleries(galleriesData);
    } catch (error) {
      console.error('Error fetching galleries:', error);
      showError('Failed to load galleries. Please try again.');
    } finally {
      setGalleryLoading(false);
    }
  };

  const fetchVideos = async () => {
    try {
      setVideoLoading(true);
      const params = selectedCategory !== "all" ? { category: selectedCategory } : {};
      const videosData = await galleryApi.getVideos(params);
      setVideos(videosData);
    } catch (error) {
      console.error('Error fetching videos:', error);
      showError('Failed to load videos. Please try again.');
    } finally {
      setVideoLoading(false);
    }
  };

  const fetchGalleryDetails = async (slug: string) => {
    try {
      setGalleryDetailLoading(true);
      const galleryDetails = await galleryApi.getGallery(slug);
      setSelectedGallery(galleryDetails);
      setIsGalleryModalOpen(true);
    } catch (error) {
      console.error('Error fetching gallery details:', error);
      showError('Failed to load gallery details. Please try again.');
    } finally {
      setGalleryDetailLoading(false);
    }
  };

  const handleGalleryClick = (gallery: ImageGallery) => {
    setCurrentImageIndex(0); // Reset to first image
    fetchGalleryDetails(gallery.slug);
  };

  const nextImage = () => {
    if (selectedGallery?.images) {
      setCurrentImageIndex((prev) => 
        prev === selectedGallery.images!.length - 1 ? 0 : prev + 1
      );
    }
  };

  const prevImage = () => {
    if (selectedGallery?.images) {
      setCurrentImageIndex((prev) => 
        prev === 0 ? selectedGallery.images!.length - 1 : prev - 1
      );
    }
  };

  const goToImage = (index: number) => {
    setCurrentImageIndex(index);
  };

  // Touch/swipe support for mobile
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      nextImage();
    } else if (isRightSwipe) {
      prevImage();
    }
  };

  // Create category options for filtering
  const categoryOptions = [
    { key: "all", label: "All" },
    ...(categories || []).map(cat => ({ key: cat.slug, label: cat.name }))
  ];

  const getTabCounts = () => {
    const totalImages = galleries.reduce((sum, gallery) => sum + gallery.image_count, 0);
    return { 
      imageCount: totalImages, 
      videoCount: videos.length 
    };
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
                <span>{loading ? '...' : imageCount} Photos</span>
              </div>
              <div className="flex items-center space-x-2">
                <Video className="h-5 w-5" />
                <span>{loading ? '...' : videos.length} Videos</span>
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
            {loading ? (
              <div className="flex space-x-2">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-10 w-20 bg-gray-200 rounded animate-pulse"></div>
                ))}
              </div>
            ) : (
              categoryOptions.map((category) => (
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
              ))
            )}
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

              {galleryLoading ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {[...Array(8)].map((_, i) => (
                    <Card key={i} className="overflow-hidden animate-pulse">
                      <div className="w-full h-64 bg-gray-300"></div>
                      <CardContent className="p-4">
                        <div className="h-4 bg-gray-300 rounded mb-2"></div>
                        <div className="h-3 bg-gray-300 rounded w-2/3 mb-2"></div>
                        <div className="h-3 bg-gray-300 rounded"></div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {galleries.map((gallery) => (
                      <Card 
                        key={gallery.id}
                        className="overflow-hidden cursor-pointer group hover:shadow-xl transition-all duration-300"
                        onClick={() => handleGalleryClick(gallery)}
                      >
                        <div className="relative">
                          <img
                            src={gallery.main_image_url}
                            alt={gallery.title}
                            className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800';
                            }}
                          />
                          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300"></div>
                          <div className="absolute top-3 left-3">
                            <Badge className="bg-ghana-gold text-black font-semibold">
                              {gallery.category_name || 'Uncategorized'}
                            </Badge>
                          </div>
                          {gallery.is_featured && (
                            <div className="absolute top-3 right-3">
                              <Badge className="bg-red-500 text-white">
                                Featured
                              </Badge>
                            </div>
                          )}
                          <div className="absolute bottom-3 right-3 bg-black/70 text-white px-2 py-1 rounded text-sm">
                            {gallery.image_count} photos
                          </div>
                        </div>
                        <CardContent className="p-4">
                          <h3 className="font-semibold text-lg mb-1 group-hover:text-ghana-green transition-colors">
                            {gallery.title}
                          </h3>
                          <div className="flex items-center text-gray-600 mb-2">
                            <MapPin className="h-4 w-4 mr-1" />
                            <span className="text-sm">{gallery.location}</span>
                          </div>
                          <p className="text-sm text-gray-500 leading-relaxed line-clamp-2">
                            {gallery.description}
                          </p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>

                  {galleries.length === 0 && !galleryLoading && (
                    <div className="text-center py-12">
                      <Camera className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                      <h3 className="text-xl font-semibold text-gray-600 mb-2">No galleries found</h3>
                      <p className="text-gray-500">
                        {selectedCategory === "all" 
                          ? "No photo galleries available at the moment" 
                          : "No photo galleries found in this category"
                        }
                      </p>
                    </div>
                  )}
                </>
              )}
            </TabsContent>

            {/* Videos Tab */}
            <TabsContent value="videos" className="space-y-8">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Video Gallery</h2>
                <p className="text-gray-600">{videoCount} video{videoCount !== 1 ? 's' : ''} found</p>
              </div>

              {videoLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {[...Array(6)].map((_, i) => (
                    <Card key={i} className="overflow-hidden animate-pulse">
                      <div className="w-full h-48 bg-gray-300"></div>
                      <CardHeader className="pb-2">
                        <div className="h-4 bg-gray-300 rounded mb-2"></div>
                        <div className="h-3 bg-gray-300 rounded w-2/3"></div>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="h-3 bg-gray-300 rounded"></div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {videos.map((video) => (
                      <Card key={video.id} className="overflow-hidden hover:shadow-xl transition-all duration-300 group">
                        <div className="relative cursor-pointer">
                          <img
                            src={video.thumbnail_url}
                            alt={video.title}
                            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600';
                            }}
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
                                  {video.video_url ? (
                                    <video
                                      controls
                                      autoPlay
                                      className="w-full h-auto max-h-[80vh]"
                                      poster={video.thumbnail_url}
                                    >
                                      <source src={video.video_url} type="video/mp4" />
                                      Your browser does not support the video tag.
                                    </video>
                                  ) : (
                                    <div className="w-full h-64 bg-gray-200 flex items-center justify-center">
                                      <p className="text-gray-500">Video not available</p>
                                    </div>
                                  )}
                                  <div className="p-6 bg-white">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{video.title}</h3>
                                    <div className="flex items-center text-gray-600 mb-3">
                                      <MapPin className="h-5 w-5 mr-2" />
                                      <span className="mr-4">{video.location}</span>
                                      <Clock className="h-5 w-5 mr-2" />
                                      <span className="mr-4">{video.duration}</span>
                                      <Eye className="h-5 w-5 mr-2" />
                                      <span>{video.formatted_views} views</span>
                                    </div>
                                    <p className="text-gray-700">{video.description}</p>
                                    {video.videographer && (
                                      <p className="text-sm text-gray-500 mt-2">Video by: {video.videographer}</p>
                                    )}
                                  </div>
                                </div>
                              </DialogContent>
                            </Dialog>
                          </div>
                          <div className="absolute top-3 left-3">
                            <Badge className="bg-ghana-gold text-black font-semibold">
                              {video.category?.name || 'Uncategorized'}
                            </Badge>
                          </div>
                          {video.is_featured && (
                            <div className="absolute top-3 right-3">
                              <Badge className="bg-red-500 text-white">
                                Featured
                              </Badge>
                            </div>
                          )}
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
                            <span>{video.formatted_views} views</span>
                          </div>
                        </CardHeader>

                        <CardContent className="pt-0">
                          <CardDescription className="text-sm leading-relaxed line-clamp-2">
                            {video.description}
                          </CardDescription>
                        </CardContent>
                      </Card>
                ))}
              </div>

                  {videos.length === 0 && !videoLoading && (
                    <div className="text-center py-12">
                      <Video className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                      <h3 className="text-xl font-semibold text-gray-600 mb-2">No videos found</h3>
                      <p className="text-gray-500">
                        {selectedCategory === "all" 
                          ? "No videos available at the moment" 
                          : "No videos found in this category"
                        }
                      </p>
                    </div>
                  )}
                </>
              )}
            </TabsContent>
          </Tabs>

          {/* Gallery Detail Modal */}
          <Dialog open={isGalleryModalOpen} onOpenChange={setIsGalleryModalOpen}>
            <DialogContent className="max-w-7xl max-h-[95vh] p-0 overflow-hidden">
              <VisuallyHidden>
                <DialogTitle>{selectedGallery?.title || 'Gallery'}</DialogTitle>
                <DialogDescription>
                  View multiple images of {selectedGallery?.title || 'this gallery'}
                </DialogDescription>
              </VisuallyHidden>
              {galleryDetailLoading ? (
                <div className="p-6 text-center">
                  <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
                  <p>Loading gallery details...</p>
                </div>
              ) : selectedGallery ? (
                <div className="relative">
                  <div className="p-6 bg-white border-b">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">{selectedGallery.title}</h3>
                        <div className="flex items-center text-gray-600 mb-3">
                          <MapPin className="h-5 w-5 mr-2" />
                          <span className="text-lg mr-4">{selectedGallery.location}</span>
                          <Camera className="h-5 w-5 mr-2" />
                          <span>{selectedGallery.image_count} photos</span>
                        </div>
                        <p className="text-gray-700 leading-relaxed">{selectedGallery.description}</p>
                        {selectedGallery.photographer && (
                          <p className="text-sm text-gray-500 mt-2">Photos by: {selectedGallery.photographer}</p>
                        )}
                      </div>
                      <Badge className="bg-ghana-gold text-black font-semibold ml-4">
                        {selectedGallery.category?.name || selectedGallery.category_name || 'Uncategorized'}
                      </Badge>
                    </div>
                  </div>
                  {/* Image Slider */}
                  <div className="relative">
                    {selectedGallery.images && selectedGallery.images.length > 0 ? (
                      <>
                        {/* Main Image Display */}
                        <div 
                          className="relative h-[60vh] bg-black flex items-center justify-center"
                          onTouchStart={onTouchStart}
                          onTouchMove={onTouchMove}
                          onTouchEnd={onTouchEnd}
                        >
                          <img
                            key={currentImageIndex} // Force re-render for transition
                            src={selectedGallery.images[currentImageIndex]?.image_url}
                            alt={selectedGallery.images[currentImageIndex]?.caption || `Image ${currentImageIndex + 1}`}
                            className="max-h-full max-w-full object-contain select-none transition-opacity duration-300 ease-in-out"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800';
                            }}
                            draggable={false}
                          />
                          
                          {/* Navigation Arrows */}
                          {selectedGallery.images.length > 1 && (
                            <>
                              <button
                                onClick={prevImage}
                                className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-all duration-200"
                                aria-label="Previous image"
                              >
                                <ChevronLeft className="h-6 w-6" />
                              </button>
                              <button
                                onClick={nextImage}
                                className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-all duration-200"
                                aria-label="Next image"
                              >
                                <ChevronRight className="h-6 w-6" />
                              </button>
                            </>
                          )}

                          {/* Image Counter and Instructions */}
                          <div className="absolute top-4 right-4 bg-black/70 text-white px-3 py-1 rounded-full text-sm">
                            {currentImageIndex + 1} / {selectedGallery.images.length}
                          </div>
                          
                          {/* Navigation Instructions */}
                          {selectedGallery.images.length > 1 && (
                            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/70 text-white px-3 py-1 rounded-full text-xs">
                              Use ← → keys or swipe to navigate
                            </div>
                          )}

                          {/* Main Image Badge */}
                          {selectedGallery.images[currentImageIndex]?.is_main && (
                            <div className="absolute top-4 left-4">
                              <Badge className="bg-blue-500 text-white">
                                Main Image
                              </Badge>
                            </div>
                          )}
                        </div>

                        {/* Image Caption */}
                        {selectedGallery.images[currentImageIndex]?.caption && (
                          <div className="bg-gray-50 px-6 py-4 border-t">
                            <p className="text-gray-700 text-center">
                              {selectedGallery.images[currentImageIndex].caption}
                            </p>
                          </div>
                        )}

                        {/* Thumbnail Navigation */}
                        {selectedGallery.images.length > 1 && (
                          <div className="p-4 bg-gray-50 border-t">
                            <div className="flex gap-2 overflow-x-auto pb-2">
                              {selectedGallery.images.map((image, index) => (
                                <button
                                  key={image.id}
                                  onClick={() => goToImage(index)}
                                  className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-all duration-200 ${
                                    index === currentImageIndex
                                      ? 'border-ghana-green shadow-lg'
                                      : 'border-gray-300 hover:border-gray-400'
                                  }`}
                                >
                                  <img
                                    src={image.thumbnail_url || image.image_url}
                                    alt={`Thumbnail ${index + 1}`}
                                    className="w-full h-full object-cover"
                                  />
                                </button>
                              ))}
                            </div>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="h-[60vh] flex items-center justify-center bg-gray-50">
                        <div className="text-center">
                          <Camera className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                          <p className="text-gray-500 text-lg">No images available for this gallery</p>
                          <p className="text-red-500 text-sm mt-2">
                            API returned {selectedGallery.image_count} images but images array is {selectedGallery.images ? 'empty' : 'undefined'}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ) : null}
            </DialogContent>
          </Dialog>
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
