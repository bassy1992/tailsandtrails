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
    if (selectedGallery?.images && selectedGallery.images.length > 1) {
      setCurrentImageIndex((prev) =>
        prev === selectedGallery.images!.length - 1 ? 0 : prev + 1
      );

      // Haptic feedback simulation for mobile
      if ('vibrate' in navigator) {
        navigator.vibrate(50);
      }
    }
  };

  const prevImage = () => {
    if (selectedGallery?.images && selectedGallery.images.length > 1) {
      setCurrentImageIndex((prev) =>
        prev === 0 ? selectedGallery.images!.length - 1 : prev - 1
      );

      // Haptic feedback simulation for mobile
      if ('vibrate' in navigator) {
        navigator.vibrate(50);
      }
    }
  };

  const goToImage = (index: number) => {
    setCurrentImageIndex(index);
  };

  // Touch/swipe support for mobile
  const [touchStart, setTouchStart] = useState<{ x: number; y: number } | null>(null);
  const [touchEnd, setTouchEnd] = useState<{ x: number; y: number } | null>(null);
  const [isSwiping, setIsSwiping] = useState(false);

  const minSwipeDistance = 50;
  const maxVerticalDistance = 100; // Maximum vertical movement allowed for horizontal swipe

  const onTouchStart = (e: React.TouchEvent) => {
    const touch = e.targetTouches[0];
    setTouchStart({ x: touch.clientX, y: touch.clientY });
    setTouchEnd(null);
    setIsSwiping(false);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    if (!touchStart) return;

    const touch = e.targetTouches[0];
    const currentTouch = { x: touch.clientX, y: touch.clientY };
    setTouchEnd(currentTouch);

    // Calculate distances
    const horizontalDistance = Math.abs(touchStart.x - currentTouch.x);
    const verticalDistance = Math.abs(touchStart.y - currentTouch.y);

    // Only consider it a swipe if:
    // 1. Horizontal movement is significant
    // 2. Horizontal movement is greater than vertical movement
    // 3. Vertical movement is within acceptable range
    if (horizontalDistance > 20 &&
      horizontalDistance > verticalDistance &&
      verticalDistance < maxVerticalDistance) {
      setIsSwiping(true);
      // Prevent default scrolling behavior during horizontal swipe
      e.preventDefault();
      e.stopPropagation();
    }
  };

  const onTouchEnd = (e: React.TouchEvent) => {
    if (!touchStart || !touchEnd) {
      // Reset states even if no valid swipe
      setTouchStart(null);
      setTouchEnd(null);
      setIsSwiping(false);
      return;
    }

    const horizontalDistance = touchStart.x - touchEnd.x;
    const verticalDistance = Math.abs(touchStart.y - touchEnd.y);

    // Only process swipe if vertical movement is minimal
    if (verticalDistance < maxVerticalDistance) {
      const isLeftSwipe = horizontalDistance > minSwipeDistance;
      const isRightSwipe = horizontalDistance < -minSwipeDistance;

      if (isLeftSwipe && selectedGallery?.images && selectedGallery.images.length > 1) {
        e.preventDefault();
        e.stopPropagation();
        nextImage();
      } else if (isRightSwipe && selectedGallery?.images && selectedGallery.images.length > 1) {
        e.preventDefault();
        e.stopPropagation();
        prevImage();
      }
    }

    // Reset touch states
    setTouchStart(null);
    setTouchEnd(null);
    setIsSwiping(false);
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
      <section className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white mobile-section">
        <div className="mobile-container">
          <div className="text-center space-y-3 sm:space-y-4">
            <div className="flex items-center justify-center space-x-2 mb-3 sm:mb-4">
              <Camera className="h-6 w-6 sm:h-8 sm:w-8 text-ghana-gold" />
              <h1 className="mobile-heading font-bold">Media Gallery</h1>
            </div>
            <p className="mobile-text text-gray-200 max-w-3xl mx-auto">
              Discover the breathtaking beauty of Ghana through our curated collection of photos and videos.
              From historic castles to pristine nature reserves, experience Ghana's diverse landscapes and rich culture.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-4 lg:gap-6 mt-6 sm:mt-8">
              <div className="flex items-center space-x-1 sm:space-x-2">
                <MapPin className="h-3 w-3 sm:h-4 sm:w-4 lg:h-5 lg:w-5" />
                <span className="text-xs sm:text-sm lg:text-base">15+ Destinations</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Camera className="h-3 w-3 sm:h-4 sm:w-4 lg:h-5 lg:w-5" />
                <span className="text-xs sm:text-sm lg:text-base">{loading ? '...' : imageCount} Photos</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Video className="h-3 w-3 sm:h-4 sm:w-4 lg:h-5 lg:w-5" />
                <span className="text-xs sm:text-sm lg:text-base">{loading ? '...' : videos.length} Videos</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2">
                <Calendar className="h-3 w-3 sm:h-4 sm:w-4 lg:h-5 lg:w-5" />
                <span className="text-xs sm:text-sm lg:text-base">Updated Daily</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Filter Categories */}
      <section className="py-4 sm:py-6 lg:py-8 bg-gray-50 border-b">
        <div className="mobile-container">
          <div className="flex items-center space-x-2 sm:space-x-4 mb-4 sm:mb-6">
            <Filter className="h-4 w-4 sm:h-5 sm:w-5 text-gray-600" />
            <span className="font-medium text-gray-700 text-sm sm:text-base">Filter by Category:</span>
          </div>
          <div className="flex flex-wrap gap-2 sm:gap-3">
            {loading ? (
              <div className="flex flex-wrap gap-2">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-8 w-16 sm:h-10 sm:w-20 bg-gray-200 rounded animate-pulse"></div>
                ))}
              </div>
            ) : (
              categoryOptions.map((category) => (
                <Button
                  key={category.key}
                  variant={selectedCategory === category.key ? "default" : "outline"}
                  onClick={() => setSelectedCategory(category.key)}
                  size="sm"
                  className={`${selectedCategory === category.key
                    ? "bg-ghana-green hover:bg-ghana-green/90 text-white"
                    : "border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white"
                    } transition-colors text-xs sm:text-sm px-3 py-1.5 sm:px-4 sm:py-2`}
                >
                  {category.label}
                </Button>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Tabs for Photos and Videos */}
      <section className="mobile-section">
        <div className="mobile-container">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 max-w-[95%] xs:max-w-sm sm:max-w-md mx-auto mb-6 sm:mb-8 h-auto">
              <TabsTrigger value="photos" className="flex items-center justify-center space-x-1 sm:space-x-2 text-xs sm:text-sm py-2.5 sm:py-3 px-2 sm:px-4">
                <Camera className="h-3.5 w-3.5 sm:h-4 sm:w-4 flex-shrink-0" />
                <span className="whitespace-nowrap">Photos ({imageCount})</span>
              </TabsTrigger>
              <TabsTrigger value="videos" className="flex items-center justify-center space-x-1 sm:space-x-2 text-xs sm:text-sm py-2.5 sm:py-3 px-2 sm:px-4">
                <Video className="h-3.5 w-3.5 sm:h-4 sm:w-4 flex-shrink-0" />
                <span className="whitespace-nowrap">Videos ({videoCount})</span>
              </TabsTrigger>
            </TabsList>

            {/* Photos Tab */}
            <TabsContent value="photos" className="space-y-8">
              <div className="text-center">
                <h2 className="mobile-subheading font-bold text-gray-900 mb-2">Photo Gallery</h2>
                <p className="text-gray-600 text-sm sm:text-base">{imageCount} photo{imageCount !== 1 ? 's' : ''} found</p>
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
                  <div className="mobile-grid">
                    {galleries.map((gallery) => (
                      <Card
                        key={gallery.id}
                        className="gallery-card group"
                        onClick={() => handleGalleryClick(gallery)}
                      >
                        <div className="relative">
                          <img
                            src={gallery.main_image_url}
                            alt={gallery.title}
                            className="w-full h-48 sm:h-56 lg:h-64 object-cover group-hover:scale-110 transition-transform duration-300"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800';
                            }}
                          />
                          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300"></div>
                          <div className="absolute top-2 left-2 sm:top-3 sm:left-3">
                            <Badge className="bg-ghana-gold text-black font-semibold text-xs sm:text-sm">
                              {gallery.category_name || 'Uncategorized'}
                            </Badge>
                          </div>
                          {gallery.is_featured && (
                            <div className="absolute top-2 right-2 sm:top-3 sm:right-3">
                              <Badge className="bg-red-500 text-white text-xs sm:text-sm">
                                Featured
                              </Badge>
                            </div>
                          )}
                          <div className="absolute bottom-2 right-2 sm:bottom-3 sm:right-3 bg-black/70 text-white px-2 py-1 rounded text-xs sm:text-sm">
                            {gallery.image_count} photos
                          </div>
                        </div>
                        <CardContent className="gallery-card-content">
                          <div className="space-y-2">
                            <h3 className="gallery-card-title line-clamp-2">
                              {gallery.title}
                            </h3>
                            <div className="flex items-start text-gray-600 gap-1.5">
                              <MapPin className="h-3 w-3 sm:h-4 sm:w-4 flex-shrink-0 mt-0.5" />
                              <span className="gallery-card-location">
                                {gallery.location}
                              </span>
                            </div>
                          </div>
                          <p className="gallery-card-description line-clamp-2">
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
                <h2 className="mobile-subheading font-bold text-gray-900 mb-2">Video Gallery</h2>
                <p className="text-gray-600 text-sm sm:text-base">{videoCount} video{videoCount !== 1 ? 's' : ''} found</p>
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
                  <div className="mobile-grid">
                    {videos.map((video) => (
                      <Card key={video.id} className="overflow-hidden hover:shadow-xl transition-all duration-300 group">
                        <div className="relative cursor-pointer">
                          <img
                            src={video.thumbnail_url}
                            alt={video.title}
                            className="w-full h-40 sm:h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600';
                            }}
                          />
                          <div className="absolute inset-0 bg-black/20 sm:bg-black/0 sm:group-hover:bg-black/30 transition-all duration-300 flex items-center justify-center">
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button
                                  size="sm"
                                  className="sm:opacity-0 sm:group-hover:opacity-100 transition-opacity duration-300 bg-ghana-gold hover:bg-ghana-gold/90 text-black text-xs sm:text-sm"
                                >
                                  <Play className="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-2" />
                                  Play
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="max-w-4xl max-h-[90vh] w-[95vw] sm:w-full p-0">
                                <VisuallyHidden>
                                  <DialogTitle>{video.title}</DialogTitle>
                                </VisuallyHidden>
                                <div className="relative">
                                  {video.video_url ? (
                                    <video
                                      controls
                                      autoPlay
                                      className="w-full h-auto max-h-[60vh] sm:max-h-[80vh]"
                                      poster={video.thumbnail_url}
                                    >
                                      <source src={video.video_url} type="video/mp4" />
                                      Your browser does not support the video tag.
                                    </video>
                                  ) : (
                                    <div className="w-full h-48 sm:h-64 bg-gray-200 flex items-center justify-center">
                                      <p className="text-gray-500 text-sm sm:text-base">Video not available</p>
                                    </div>
                                  )}
                                  <div className="p-4 sm:p-6 bg-white">
                                    <h3 className="text-lg sm:text-2xl font-bold text-gray-900 mb-2 line-clamp-2">{video.title}</h3>
                                    <div className="flex flex-wrap items-center text-gray-600 mb-3 gap-2 sm:gap-4 text-sm sm:text-base">
                                      <div className="flex items-center">
                                        <MapPin className="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2 flex-shrink-0" />
                                        <span>{video.location}</span>
                                      </div>
                                      <div className="flex items-center">
                                        <Clock className="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2 flex-shrink-0" />
                                        <span>{video.duration}</span>
                                      </div>
                                      <div className="flex items-center">
                                        <Eye className="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2 flex-shrink-0" />
                                        <span>{video.formatted_views} views</span>
                                      </div>
                                    </div>
                                    <p className="text-gray-700 text-sm sm:text-base leading-relaxed">{video.description}</p>
                                    {video.videographer && (
                                      <p className="text-xs sm:text-sm text-gray-500 mt-2">Video by: {video.videographer}</p>
                                    )}
                                  </div>
                                </div>
                              </DialogContent>
                            </Dialog>
                          </div>
                          <div className="absolute top-2 left-2 sm:top-3 sm:left-3">
                            <Badge className="bg-ghana-gold text-black font-semibold text-xs sm:text-sm">
                              {video.category?.name || 'Uncategorized'}
                            </Badge>
                          </div>
                          {video.is_featured && (
                            <div className="absolute top-2 right-2 sm:top-3 sm:right-3">
                              <Badge className="bg-red-500 text-white text-xs sm:text-sm">
                                Featured
                              </Badge>
                            </div>
                          )}
                          <div className="absolute bottom-2 right-2 sm:bottom-3 sm:right-3 bg-black/70 text-white px-2 py-1 rounded text-xs sm:text-sm">
                            {video.duration}
                          </div>
                        </div>

                        <CardHeader className="pb-2 p-3 sm:p-6 sm:pb-2">
                          <CardTitle className="text-base sm:text-lg leading-tight group-hover:text-ghana-green transition-colors line-clamp-1">
                            {video.title}
                          </CardTitle>
                          <div className="flex items-center text-gray-600 text-xs sm:text-sm">
                            <MapPin className="h-3 w-3 sm:h-4 sm:w-4 mr-1 flex-shrink-0" />
                            <span className="mr-2 sm:mr-3 truncate">{video.location}</span>
                            <Eye className="h-3 w-3 sm:h-4 sm:w-4 mr-1 flex-shrink-0" />
                            <span className="truncate">{video.formatted_views} views</span>
                          </div>
                        </CardHeader>

                        <CardContent className="pt-0 p-3 sm:p-6 sm:pt-0">
                          <CardDescription className="text-xs sm:text-sm leading-relaxed line-clamp-2">
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
            <DialogContent className="max-w-7xl max-h-[98vh] w-[98vw] xs:w-[96vw] sm:w-full p-0 overflow-hidden">
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
                  <div className="p-3 xs:p-4 sm:p-6 bg-white border-b">
                    <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 xs:gap-3">
                      <div className="flex-1">
                        <h3 className="text-base xs:text-lg sm:text-2xl font-bold text-gray-900 mb-1 xs:mb-2 line-clamp-2">{selectedGallery.title}</h3>
                        <div className="flex flex-wrap items-center text-gray-600 mb-2 xs:mb-3 gap-1.5 xs:gap-2 sm:gap-4">
                          <div className="flex items-center">
                            <MapPin className="h-3 w-3 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 flex-shrink-0" />
                            <span className="text-xs xs:text-sm sm:text-lg">{selectedGallery.location}</span>
                          </div>
                          <div className="flex items-center">
                            <Camera className="h-3 w-3 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 flex-shrink-0" />
                            <span className="text-xs xs:text-sm sm:text-base">{selectedGallery.image_count} photos</span>
                          </div>
                        </div>
                        <p className="text-xs xs:text-sm sm:text-base text-gray-700 leading-relaxed line-clamp-2 xs:line-clamp-3 sm:line-clamp-none">{selectedGallery.description}</p>
                        {selectedGallery.photographer && (
                          <p className="text-xs text-gray-500 mt-1 xs:mt-2">Photos by: {selectedGallery.photographer}</p>
                        )}
                      </div>
                      <Badge className="bg-ghana-gold text-black font-semibold text-xs self-start sm:ml-4">
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
                          className="gallery-slider h-[40vh] xs:h-[42vh] sm:h-[55vh] md:h-[65vh] bg-black flex items-center justify-center"
                          onTouchStart={onTouchStart}
                          onTouchMove={onTouchMove}
                          onTouchEnd={onTouchEnd}
                          style={{
                            touchAction: 'pan-y pinch-zoom',
                            WebkitTouchCallout: 'none',
                            WebkitUserSelect: 'none',
                            userSelect: 'none',
                            minHeight: '280px',
                            maxHeight: '400px'
                          }}
                        >
                          {/* Main Image - Base Layer (z-0) */}
                          <img
                            key={currentImageIndex} // Force re-render for transition
                            src={selectedGallery.images[currentImageIndex]?.image_url}
                            alt={selectedGallery.images[currentImageIndex]?.caption || `Image ${currentImageIndex + 1}`}
                            className={`gallery-slider-image max-h-full max-w-full object-contain select-none relative z-0 ${isSwiping ? 'pointer-events-none scale-95' : 'scale-100'
                              }`}
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800';
                            }}
                            draggable={false}
                            onContextMenu={(e) => e.preventDefault()}
                            loading="lazy"
                          />

                          {/* Loading indicator for image transitions - Overlay Layer (z-10) */}
                          <div className={`absolute inset-0 bg-black/20 flex items-center justify-center transition-opacity duration-200 z-10 ${isSwiping ? 'opacity-100' : 'opacity-0 pointer-events-none'
                            }`}>
                            <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                          </div>

                          {/* Navigation Arrows - Control Layer (z-30) */}
                          {selectedGallery.images.length > 1 && (
                            <>
                              <button
                                onClick={prevImage}
                                className="gallery-slider-nav left-0.5 xs:left-1 sm:left-3 md:left-4 top-1/2 -translate-y-1/2 p-1.5 xs:p-2 sm:p-2.5 md:p-3 active:bg-black/90 z-30"
                                aria-label="Previous image"
                                style={{ minWidth: '40px', minHeight: '40px' }}
                              >
                                <ChevronLeft className="h-4 w-4 xs:h-5 xs:w-5 sm:h-6 sm:w-6 md:h-7 md:w-7" />
                              </button>
                              <button
                                onClick={nextImage}
                                className="gallery-slider-nav right-0.5 xs:right-1 sm:right-3 md:right-4 top-1/2 -translate-y-1/2 p-1.5 xs:p-2 sm:p-2.5 md:p-3 active:bg-black/90 z-30"
                                aria-label="Next image"
                                style={{ minWidth: '40px', minHeight: '40px' }}
                              >
                                <ChevronRight className="h-4 w-4 xs:h-5 xs:w-5 sm:h-6 sm:w-6 md:h-7 md:w-7" />
                              </button>
                            </>
                          )}

                          {/* Image Counter - Info Layer (z-20) */}
                          <div className="absolute top-2 xs:top-3 sm:top-4 right-2 xs:right-3 sm:right-4 bg-black/80 text-white px-2 xs:px-3 py-1 xs:py-1.5 rounded-full text-xs font-medium backdrop-blur-sm shadow-lg z-20">
                            {currentImageIndex + 1} / {selectedGallery.images.length}
                          </div>

                          {/* Progress Dots for Mobile - Info Layer (z-20) */}
                          {selectedGallery.images.length > 1 && selectedGallery.images.length <= 8 && (
                            <div className="gallery-dots absolute bottom-3 xs:bottom-4 left-1/2 -translate-x-1/2 sm:hidden z-20 gap-1 xs:gap-1.5">
                              {selectedGallery.images.map((_, index) => (
                                <button
                                  key={index}
                                  onClick={() => goToImage(index)}
                                  className={`w-1.5 h-1.5 xs:w-2 xs:h-2 rounded-full transition-all duration-200 touch-manipulation ${index === currentImageIndex
                                    ? 'bg-white scale-125'
                                    : 'bg-white/50 hover:bg-white/70'
                                    }`}
                                  aria-label={`Go to image ${index + 1}`}
                                  style={{ minWidth: '20px', minHeight: '20px' }}
                                />
                              ))}
                            </div>
                          )}

                          {/* Navigation Instructions - Info Layer (z-20) */}
                          {selectedGallery.images.length > 1 && (
                            <div className="absolute bottom-3 sm:bottom-4 left-1/2 -translate-x-1/2 bg-black/70 text-white px-3 py-1 rounded-full text-xs hidden sm:block backdrop-blur-sm z-20">
                              Use ← → keys or swipe to navigate
                            </div>
                          )}

                          {/* Mobile Navigation Instructions - Info Layer (z-20) */}
                          {selectedGallery.images.length > 1 && selectedGallery.images.length > 8 && (
                            <div className="absolute bottom-2 xs:bottom-3 left-1/2 -translate-x-1/2 bg-black/70 text-white px-2 xs:px-3 py-0.5 xs:py-1 rounded-full text-xs sm:hidden backdrop-blur-sm z-20">
                              {isSwiping ? 'Swiping...' : 'Swipe'}
                            </div>
                          )}

                          {/* Enhanced Swipe Progress Indicator - Top Layer (z-40) */}
                          {isSwiping && touchStart && touchEnd && selectedGallery?.images && selectedGallery.images.length > 1 && (
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none z-40">
                              <div className={`w-16 h-16 xs:w-18 xs:h-18 sm:w-16 sm:h-16 rounded-full border-3 xs:border-4 border-white/40 flex items-center justify-center transition-all duration-200 backdrop-blur-sm ${Math.abs(touchStart.x - touchEnd.x) > minSwipeDistance
                                ? 'bg-ghana-green/90 scale-110 shadow-2xl'
                                : 'bg-black/60 scale-100'
                                }`}>
                                {touchStart.x - touchEnd.x > minSwipeDistance ? (
                                  <div className="flex flex-col items-center">
                                    <ChevronRight className="h-6 w-6 xs:h-7 xs:w-7 sm:h-8 sm:w-8 text-white" />
                                    <div className="text-xs text-white font-medium mt-0.5 xs:mt-1 hidden xs:block">Next</div>
                                  </div>
                                ) : touchEnd.x - touchStart.x > minSwipeDistance ? (
                                  <div className="flex flex-col items-center">
                                    <ChevronLeft className="h-6 w-6 xs:h-7 xs:w-7 sm:h-8 sm:w-8 text-white" />
                                    <div className="text-xs text-white font-medium mt-0.5 xs:mt-1 hidden xs:block">Prev</div>
                                  </div>
                                ) : (
                                  <div className="flex flex-col items-center">
                                    <div className="w-2 h-2 xs:w-3 xs:h-3 bg-white rounded-full animate-pulse" />
                                    <div className="text-xs text-white/70 font-medium mt-0.5 xs:mt-1 hidden xs:block">Swipe</div>
                                  </div>
                                )}
                              </div>

                              {/* Swipe progress bar */}
                              <div className="absolute -bottom-6 xs:-bottom-8 left-1/2 -translate-x-1/2 w-20 xs:w-24 h-0.5 xs:h-1 bg-white/20 rounded-full overflow-hidden">
                                <div
                                  className="h-full bg-ghana-green transition-all duration-100 ease-out"
                                  style={{
                                    width: `${Math.min(100, (Math.abs(touchStart.x - touchEnd.x) / minSwipeDistance) * 100)}%`
                                  }}
                                />
                              </div>
                            </div>
                          )}

                          {/* Main Image Badge - Info Layer (z-20) */}
                          {selectedGallery.images[currentImageIndex]?.is_main && (
                            <div className="absolute top-2 xs:top-2 sm:top-4 left-2 xs:left-2 sm:left-4 z-20">
                              <Badge className="bg-blue-500 text-white text-xs">
                                Main
                              </Badge>
                            </div>
                          )}
                        </div>

                        {/* Image Caption */}
                        {selectedGallery.images[currentImageIndex]?.caption && (
                          <div className="bg-gray-50 px-4 sm:px-6 py-3 sm:py-4 border-t">
                            <p className="text-gray-700 text-center text-sm sm:text-base">
                              {selectedGallery.images[currentImageIndex].caption}
                            </p>
                          </div>
                        )}

                        {/* Enhanced Thumbnail Navigation */}
                        {selectedGallery.images.length > 1 && (
                          <div className="p-2 xs:p-3 sm:p-4 bg-gray-50 border-t">
                            <div className="relative">
                              {/* Thumbnail scroll container */}
                              <div className="gallery-thumbnails gap-1.5 xs:gap-2 sm:gap-3">
                                {selectedGallery.images.map((image, index) => (
                                  <button
                                    key={image.id}
                                    onClick={() => goToImage(index)}
                                    className={`gallery-thumbnail w-12 h-12 xs:w-14 xs:h-14 sm:w-16 sm:h-16 md:w-18 md:h-18 ${index === currentImageIndex ? 'active' : ''
                                      } hover:scale-102`}
                                  >
                                    <img
                                      src={image.thumbnail_url || image.image_url}
                                      alt={`Thumbnail ${index + 1}`}
                                      className="w-full h-full object-cover"
                                      loading="lazy"
                                    />
                                    {/* Active indicator */}
                                    {index === currentImageIndex && (
                                      <div className="absolute inset-0 bg-ghana-green/20 flex items-center justify-center">
                                        <div className="w-3 h-3 bg-ghana-green rounded-full shadow-lg"></div>
                                      </div>
                                    )}
                                    {/* Image number for mobile */}
                                    <div className="absolute bottom-0 right-0 bg-black/70 text-white text-xs px-0.5 xs:px-1 py-0.5 rounded-tl text-center min-w-[14px] xs:min-w-[16px] sm:hidden">
                                      {index + 1}
                                    </div>
                                  </button>
                                ))}
                              </div>

                              {/* Scroll indicators for mobile */}
                              {selectedGallery.images.length > 3 && (
                                <>
                                  <div className="absolute left-0 top-0 bottom-2 w-6 xs:w-8 bg-gradient-to-r from-gray-50 to-transparent pointer-events-none sm:hidden" />
                                  <div className="absolute right-0 top-0 bottom-2 w-6 xs:w-8 bg-gradient-to-l from-gray-50 to-transparent pointer-events-none sm:hidden" />
                                </>
                              )}
                            </div>

                            {/* Thumbnail navigation hint */}
                            {selectedGallery.images.length > 3 && (
                              <div className="text-center mt-1 xs:mt-2 sm:hidden">
                                <p className="text-xs text-gray-500">Scroll for more</p>
                              </div>
                            )}
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
      <section className="bg-ghana-green text-white mobile-section">
        <div className="mobile-container text-center space-y-3 sm:space-y-4 lg:space-y-6 max-w-4xl">
          <h2 className="mobile-subheading font-bold">Ready to Experience These Places?</h2>
          <p className="mobile-text text-gray-200 leading-relaxed">
            These stunning destinations are waiting for you. Book your Ghana adventure today and create your own unforgettable memories.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center max-w-md sm:max-w-none mx-auto">
            <Link to="/destinations" className="w-full sm:w-auto">
              <Button className="mobile-button bg-ghana-gold hover:bg-ghana-gold/90 text-black w-full sm:w-auto">
                Book a Tour
              </Button>
            </Link>
            <Link to="/destinations" className="w-full sm:w-auto">
              <Button variant="outline" className="mobile-button border-white text-white hover:bg-white hover:text-ghana-green w-full sm:w-auto">
                View Destinations
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
