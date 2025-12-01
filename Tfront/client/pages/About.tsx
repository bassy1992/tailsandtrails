import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  MapPin, Users, Award, Heart, Shield, Globe, 
  Star, CheckCircle, Camera, Compass, Clock, Phone 
} from "lucide-react";
import { Link } from "react-router-dom";

export default function About() {
  const teamMembers = [
    {
      name: "Kwame Asante",
      role: "Founder & CEO",
      image: "https://images.pexels.com/photos/1040880/pexels-photo-1040880.jpeg?auto=compress&cs=tinysrgb&w=300",
      bio: "With over 15 years in Ghana's tourism industry, Kwame founded Tales and Trails Ghana to share his passion for Ghana's rich culture and heritage with the world."
    },
    {
      name: "Akosua Mensah",
      role: "Head of Operations",
      image: "https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=300",
      bio: "Akosua ensures every tour runs smoothly. Her attention to detail and customer service excellence makes every Ghana adventure unforgettable."
    },
    {
      name: "Kofi Boateng",
      role: "Senior Tour Guide",
      image: "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=300",
      bio: "A certified guide with deep knowledge of Ghana's history and culture. Kofi brings stories to life with his engaging storytelling and warm personality."
    },
    {
      name: "Ama Darko",
      role: "Cultural Heritage Specialist",
      image: "https://images.pexels.com/photos/7803877/pexels-photo-7803877.jpeg?auto=compress&cs=tinysrgb&w=300",
      bio: "Ama specializes in cultural immersion experiences, connecting visitors with local communities and authentic Ghanaian traditions."
    }
  ];

  const achievements = [
    {
      icon: Users,
      number: "500+",
      title: "Happy Travelers",
      description: "Satisfied customers from around the world"
    },
    {
      icon: MapPin,
      number: "15+",
      title: "Destinations",
      description: "Carefully curated locations across Ghana"
    },
    {
      icon: Award,
      number: "50+",
      title: "Tour Packages",
      description: "Diverse experiences for every traveler"
    },
    {
      icon: Star,
      number: "4.8",
      title: "Average Rating",
      description: "Consistently excellent customer reviews"
    }
  ];

  const values = [
    {
      icon: Heart,
      title: "Authentic Experiences",
      description: "We provide genuine cultural immersion and real connections with local communities."
    },
    {
      icon: Shield,
      title: "Safety First",
      description: "Your safety and comfort are our top priorities in every tour we organize."
    },
    {
      icon: Globe,
      title: "Sustainable Tourism",
      description: "We promote responsible tourism that benefits local communities and preserves heritage."
    },
    {
      icon: Users,
      title: "Personalized Service",
      description: "Every traveler is unique, and we tailor experiences to match your interests and preferences."
    }
  ];

  return (
    <Layout>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-ghana-green to-ghana-blue text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold">About Tales and Trails Ghana</h1>
            <p className="text-xl text-gray-200 max-w-3xl mx-auto">
              Your trusted partner in discovering the beauty, culture, and heritage of Ghana. 
              We're passionate about creating unforgettable experiences that connect you with the heart of West Africa.
            </p>
          </div>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">Our Story</h2>
              <div className="space-y-4 text-gray-700 leading-relaxed">
                <p>
                  Tales and Trails Ghana was born from a simple dream: to share the incredible beauty and rich heritage of Ghana
                  with travelers from around the world. Founded in 2018 by Kwame Asante, a passionate Ghanaian with 
                  deep roots in the tourism industry, our company has grown from humble beginnings to become one of 
                  Ghana's most trusted tour operators.
                </p>
                <p>
                  What started as a small local guiding service has evolved into a comprehensive tourism company 
                  offering everything from day trips to extended cultural immersion experiences. We believe that 
                  travel is more than just visiting places – it's about creating connections, understanding cultures, 
                  and building bridges between people.
                </p>
                <p>
                  Today, we're proud to have facilitated incredible journeys for over 500 travelers, each leaving 
                  with not just memories, but a deeper appreciation for Ghana's vibrant culture, complex history, 
                  and warm hospitality.
                </p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <img
                src="https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=400"
                alt="Cape Coast Castle"
                className="rounded-lg shadow-lg"
              />
              <img
                src="https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=400"
                alt="Aburi Gardens"
                className="rounded-lg shadow-lg mt-8"
              />
              <img
                src="https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=400"
                alt="Local Culture"
                className="rounded-lg shadow-lg"
              />
              <img
                src="https://images.pexels.com/photos/30211750/pexels-photo-30211750.jpeg?auto=compress&cs=tinysrgb&w=400"
                alt="Ghana Coast"
                className="rounded-lg shadow-lg mt-8"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Our Mission & Vision</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Driving positive change through responsible and authentic tourism experiences
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="border-0 shadow-lg">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Compass className="h-8 w-8 text-ghana-green" />
                </div>
                <CardTitle className="text-2xl text-ghana-green">Our Mission</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed text-center">
                  To provide authentic, safe, and enriching travel experiences that showcase Ghana's natural beauty, 
                  cultural heritage, and warm hospitality while supporting local communities and promoting sustainable tourism practices.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-ghana-gold/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Globe className="h-8 w-8 text-ghana-gold" />
                </div>
                <CardTitle className="text-2xl text-ghana-gold">Our Vision</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed text-center">
                  To become West Africa's leading tour operator, recognized for excellence in customer service, 
                  cultural authenticity, and positive impact on local communities while making Ghana a must-visit destination for global travelers.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Our Values</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <value.icon className="h-8 w-8 text-ghana-green" />
                  </div>
                  <CardTitle className="text-lg">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-sm leading-relaxed">{value.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Achievements */}
      <section className="py-16 bg-ghana-green text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Achievements</h2>
            <p className="text-xl text-gray-200 max-w-2xl mx-auto">
              Numbers that reflect our commitment to excellence
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {achievements.map((achievement, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <achievement.icon className="h-8 w-8 text-ghana-gold" />
                </div>
                <div className="text-3xl md:text-4xl font-bold text-ghana-gold mb-2">{achievement.number}</div>
                <div className="text-lg font-semibold mb-1">{achievement.title}</div>
                <div className="text-sm text-gray-200">{achievement.description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Our Team */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The passionate professionals who make your Ghana adventure possible
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <Card key={index} className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <img
                    src={member.image}
                    alt={member.name}
                    className="w-24 h-24 rounded-full mx-auto mb-4 object-cover"
                  />
                  <CardTitle className="text-lg">{member.name}</CardTitle>
                  <CardDescription className="text-ghana-green font-medium">{member.role}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-sm leading-relaxed">{member.bio}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Why Choose Tales and Trails Ghana?</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              What sets us apart in Ghana's tourism landscape
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-ghana-green" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Local Expertise</h3>
                <p className="text-gray-600 text-sm">Born and raised in Ghana, we know the hidden gems and authentic experiences that guidebooks miss.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-ghana-green" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Small Group Focus</h3>
                <p className="text-gray-600 text-sm">We keep our groups small to ensure personalized attention and authentic cultural interactions.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-ghana-green" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">24/7 Support</h3>
                <p className="text-gray-600 text-sm">Our team is available around the clock to ensure your safety and comfort throughout your journey.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-ghana-green" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Cultural Immersion</h3>
                <p className="text-gray-600 text-sm">We create opportunities for genuine cultural exchange and meaningful connections with local communities.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-ghana-green" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Flexible Itineraries</h3>
                <p className="text-gray-600 text-sm">Whether you want our popular packages or a custom experience, we adapt to your interests and schedule.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-ghana-green" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Fair Pricing</h3>
                <p className="text-gray-600 text-sm">Transparent pricing with no hidden fees, and excellent value for comprehensive, high-quality experiences.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Certifications & Partnerships</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Recognized excellence in tourism and heritage preservation
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="h-8 w-8 text-ghana-green" />
              </div>
              <div className="font-medium">Ghana Tourism Authority</div>
              <div className="text-sm text-gray-600">Licensed Tour Operator</div>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-ghana-green" />
              </div>
              <div className="font-medium">UNESCO Partnership</div>
              <div className="text-sm text-gray-600">Heritage Site Tours</div>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Globe className="h-8 w-8 text-ghana-green" />
              </div>
              <div className="font-medium">Sustainable Tourism</div>
              <div className="text-sm text-gray-600">Certified Provider</div>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-ghana-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-ghana-green" />
              </div>
              <div className="font-medium">Community Partner</div>
              <div className="text-sm text-gray-600">Local Development</div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-gradient-to-r from-ghana-gold to-amber-400 text-black">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
          <h2 className="text-3xl md:text-4xl font-bold">Ready to Experience Ghana?</h2>
          <p className="text-xl">
            Join hundreds of satisfied travelers who have discovered the magic of Ghana with us. 
            Let's create your perfect adventure together.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/destinations">
              <Button size="lg" className="bg-ghana-green hover:bg-ghana-green/90 text-white">
                Explore Our Tours
              </Button>
            </Link>
            <Link to="/contact">
              <Button size="lg" variant="outline" className="border-ghana-green text-ghana-green hover:bg-ghana-green hover:text-white">
                <Phone className="h-4 w-4 mr-2" />
                Contact Us Today
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}
