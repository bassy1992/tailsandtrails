import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { VisuallyHidden } from "@/components/ui/visually-hidden";
import { Play, MapPin, Clock, Eye } from "lucide-react";
import { Link } from "react-router-dom";

interface Video {
  id: number;
  title: string;
  description: string;
  thumbnail: string;
  videoUrl: string;
  duration: string;
  views: string;
  category: string;
  location: string;
}

interface VideoSectionProps {
  title: string;
  subtitle?: string;
  videos: Video[];
  showAllLink?: boolean;
  maxVideos?: number;
  layout?: "grid" | "featured";
}

export default function VideoSection({ 
  title, 
  subtitle, 
  videos, 
  showAllLink = true, 
  maxVideos = 3,
  layout = "grid" 
}: VideoSectionProps) {
  const displayVideos = videos.slice(0, maxVideos);

  if (layout === "featured" && videos.length > 0) {
    const featuredVideo = videos[0];
    return (
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">{title}</h2>
            {subtitle && <p className="text-xl text-gray-600 max-w-2xl mx-auto">{subtitle}</p>}
          </div>
          
          <div className="max-w-4xl mx-auto">
            <Card className="overflow-hidden">
              <div className="relative group cursor-pointer">
                <img
                  src={featuredVideo.thumbnail}
                  alt={featuredVideo.title}
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
                        <DialogTitle>{featuredVideo.title}</DialogTitle>
                      </VisuallyHidden>
                      <div className="relative">
                        <video
                          controls
                          autoPlay
                          className="w-full h-auto max-h-[80vh]"
                          poster={featuredVideo.thumbnail}
                        >
                          <source src={featuredVideo.videoUrl} type="video/mp4" />
                          Your browser does not support the video tag.
                        </video>
                        <div className="p-6 bg-white">
                          <h3 className="text-2xl font-bold text-gray-900 mb-2">{featuredVideo.title}</h3>
                          <div className="flex items-center text-gray-600 mb-3">
                            <MapPin className="h-5 w-5 mr-2" />
                            <span className="mr-4">{featuredVideo.location}</span>
                            <Clock className="h-5 w-5 mr-2" />
                            <span className="mr-4">{featuredVideo.duration}</span>
                            <Eye className="h-5 w-5 mr-2" />
                            <span>{featuredVideo.views} views</span>
                          </div>
                          <p className="text-gray-700">{featuredVideo.description}</p>
                        </div>
                      </div>
                    </DialogContent>
                  </Dialog>
                </div>
                <Badge className="absolute top-4 left-4 bg-ghana-gold text-black">
                  Featured
                </Badge>
                <div className="absolute bottom-4 right-4 bg-black/70 text-white px-2 py-1 rounded text-sm">
                  {featuredVideo.duration}
                </div>
              </div>
              <CardContent className="p-6">
                <h3 className="text-2xl font-bold mb-2">{featuredVideo.title}</h3>
                <div className="flex items-center text-gray-600 mb-3">
                  <MapPin className="h-4 w-4 mr-1" />
                  <span className="mr-4">{featuredVideo.location}</span>
                  <Eye className="h-4 w-4 mr-1" />
                  <span>{featuredVideo.views} views</span>
                </div>
                <p className="text-gray-700">{featuredVideo.description}</p>
              </CardContent>
            </Card>
          </div>

          {showAllLink && (
            <div className="text-center mt-12">
              <Link to="/videos">
                <Button variant="outline" size="lg" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                  View All Videos
                </Button>
              </Link>
            </div>
          )}
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">{title}</h2>
          {subtitle && <p className="text-xl text-gray-600 max-w-2xl mx-auto">{subtitle}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {displayVideos.map((video) => (
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

        {showAllLink && (
          <div className="text-center mt-12">
            <Link to="/videos">
              <Button variant="outline" size="lg" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                View All Videos
              </Button>
            </Link>
          </div>
        )}
      </div>
    </section>
  );
}
