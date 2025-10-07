import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Layout from '../components/Layout';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Calendar, MapPin, Phone, Mail, User, CreditCard, Clock, Star, Loader2 } from 'lucide-react';

interface DashboardOverview {
  total_bookings: number;
  destinations_visited: number;
  total_spent: number;
  member_since: string;
  member_level: string;
  member_color: string;
  points: number;
}

interface DashboardBooking {
  id: string;
  type: string;
  destination: string;
  date: string;
  duration: string;
  status: string;
  amount: string;
  image: string | null;
  participants: number;
  created_at: string;
}

interface DashboardActivity {
  id: number;
  type: string;
  title: string;
  date: string;
  status: string;
  status_color: string;
  reference: string;
}

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [bookings, setBookings] = useState<DashboardBooking[]>([]);
  const [activities, setActivities] = useState<DashboardActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      if (!token) {
        setError('No authentication token found');
        return;
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      };

      // Fetch all dashboard data in parallel
      const [overviewRes, bookingsRes, activitiesRes] = await Promise.all([
        fetch('http://localhost:8000/api/dashboard/overview/', { headers }),
        fetch('http://localhost:8000/api/dashboard/bookings/', { headers }),
        fetch('http://localhost:8000/api/dashboard/activity/', { headers })
      ]);

      if (overviewRes.ok) {
        const overviewData = await overviewRes.json();
        setOverview(overviewData);
      }

      if (bookingsRes.ok) {
        const bookingsData = await bookingsRes.json();
        setBookings(bookingsData);
      }

      if (activitiesRes.ok) {
        const activitiesData = await activitiesRes.json();
        setActivities(activitiesData);
      }

    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return null;
  }

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>Loading dashboard...</span>
          </div>
        </div>
      </Layout>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-ghana-green mb-2">Welcome back, {user.name}!</h1>
            <p className="text-gray-600">Manage your bookings and explore new destinations</p>
          </div>
        </div>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="bookings">My Bookings</TabsTrigger>
            <TabsTrigger value="profile">Profile</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Bookings</CardTitle>
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-ghana-green">{overview?.total_bookings || 0}</div>
                  <p className="text-xs text-muted-foreground">All time</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Destinations Visited</CardTitle>
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-ghana-green">{overview?.destinations_visited || 0}</div>
                  <p className="text-xs text-muted-foreground">Completed tours</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
                  <CreditCard className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-ghana-green">GH₵ {overview?.total_spent || 0}</div>
                  <p className="text-xs text-muted-foreground">Lifetime value</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Member Since</CardTitle>
                  <Clock className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-ghana-green">
                    {overview?.member_since ? new Date(overview.member_since).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Member status: {overview?.member_level || 'Bronze'}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Your latest booking activities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {activities.length > 0 ? (
                    activities.slice(0, 5).map((activity) => (
                      <div key={`${activity.type}-${activity.id}`} className="flex items-center space-x-4">
                        <div className={`w-2 h-2 rounded-full ${
                          activity.status_color === 'green' ? 'bg-green-500' :
                          activity.status_color === 'blue' ? 'bg-blue-500' :
                          activity.status_color === 'yellow' ? 'bg-yellow-500' :
                          activity.status_color === 'red' ? 'bg-red-500' :
                          'bg-gray-500'
                        }`}></div>
                        <div className="flex-1">
                          <p className="text-sm font-medium">{activity.title}</p>
                          <p className="text-xs text-gray-500">
                            {new Date(activity.date).toLocaleDateString('en-US', { 
                              month: 'long', 
                              day: 'numeric', 
                              year: 'numeric' 
                            })}
                          </p>
                        </div>
                        <Badge className={`${
                          activity.status_color === 'green' ? 'bg-green-100 text-green-800' :
                          activity.status_color === 'blue' ? 'bg-blue-100 text-blue-800' :
                          activity.status_color === 'yellow' ? 'bg-yellow-100 text-yellow-800' :
                          activity.status_color === 'red' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {activity.status.charAt(0).toUpperCase() + activity.status.slice(1)}
                        </Badge>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <p>No recent activity</p>
                      <p className="text-sm">Start booking destinations or tickets to see activity here</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Bookings Tab */}
          <TabsContent value="bookings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>My Bookings</CardTitle>
                <CardDescription>Manage your current and past tour bookings</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {bookings.length > 0 ? (
                    bookings.map((booking) => (
                      <div key={booking.id} className="flex flex-col md:flex-row gap-4 p-4 border rounded-lg hover:shadow-md transition-shadow">
                        {booking.image ? (
                          <img 
                            src={booking.image} 
                            alt={booking.destination}
                            className="w-full md:w-32 h-32 object-cover rounded-lg"
                          />
                        ) : (
                          <div className="w-full md:w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center">
                            <MapPin className="w-8 h-8 text-gray-400" />
                          </div>
                        )}
                        <div className="flex-1 space-y-2">
                          <div className="flex flex-col md:flex-row md:items-center justify-between">
                            <div>
                              <h3 className="font-semibold text-lg">{booking.destination}</h3>
                              <span className="text-sm text-gray-500 capitalize">
                                {booking.type === 'destination' ? 'Tour Package' : 'Event Ticket'}
                              </span>
                            </div>
                            <Badge className={getStatusColor(booking.status)}>
                              {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                            </Badge>
                          </div>
                          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                            <span className="flex items-center gap-1">
                              <Calendar className="w-4 h-4" />
                              {new Date(booking.date).toLocaleDateString()}
                            </span>
                            <span className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              {booking.duration}
                            </span>
                            <span className="flex items-center gap-1">
                              <User className="w-4 h-4" />
                              {booking.participants} {booking.type === 'destination' ? 'participant' : 'ticket'}{booking.participants > 1 ? 's' : ''}
                            </span>
                          </div>
                          <div className="flex justify-between items-center pt-2">
                            <span className="text-lg font-bold text-ghana-green">{booking.amount}</span>
                            <div className="space-x-2">
                              <Button variant="outline" size="sm">View Details</Button>
                              {booking.status === 'completed' && (
                                <Button variant="outline" size="sm">
                                  <Star className="w-4 h-4 mr-1" />
                                  Review
                                </Button>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-12 text-gray-500">
                      <MapPin className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                      <h3 className="text-lg font-medium mb-2">No bookings yet</h3>
                      <p className="text-sm mb-4">Start exploring our destinations and events</p>
                      <div className="space-x-2">
                        <Button className="bg-ghana-green hover:bg-ghana-green/90">
                          Browse Destinations
                        </Button>
                        <Button variant="outline">
                          View Events
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Profile Tab */}
          <TabsContent value="profile" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Profile Information</CardTitle>
                <CardDescription>Manage your account details and preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center space-x-4">
                  <Avatar className="w-20 h-20">
                    <AvatarImage src={user.avatar} />
                    <AvatarFallback className="text-xl font-semibold bg-ghana-green text-white">
                      {getInitials(user.name)}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <h3 className="text-xl font-semibold">{user.name}</h3>
                    <p className="text-gray-600">
                      {overview?.member_level || 'Bronze'} Member since {overview?.member_since ? new Date(overview.member_since).toLocaleDateString() : 'N/A'}
                    </p>
                    <Button variant="outline" size="sm" className="mt-2">
                      Change Photo
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <Mail className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="text-sm text-gray-600">Email</p>
                        <p className="font-medium">{user.email}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Phone className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="text-sm text-gray-600">Phone</p>
                        <p className="font-medium">{user.phone || 'Not provided'}</p>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <User className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="text-sm text-gray-600">Member Level</p>
                        <div className="flex items-center gap-2">
                          <Badge className={overview?.member_color || "bg-orange-100 text-orange-800"}>
                            {overview?.member_level || 'Bronze'} Member
                          </Badge>
                          <span className="text-sm text-gray-600">{overview?.points || 0} points</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Calendar className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="text-sm text-gray-600">Member Since</p>
                        <p className="font-medium">
                          {overview?.member_since ? new Date(overview.member_since).toLocaleDateString() : 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t">
                  <div className="flex flex-col md:flex-row gap-4">
                    <Button className="bg-ghana-green hover:bg-ghana-green/90">
                      Edit Profile
                    </Button>
                    <Button variant="outline">
                      Change Password
                    </Button>
                    <Button variant="outline">
                      Privacy Settings
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
