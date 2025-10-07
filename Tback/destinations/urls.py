from django.urls import path
from . import views, dashboard_views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Destinations
    path('destinations/', views.DestinationListView.as_view(), name='destination-list'),
    path('destinations/<slug:slug>/', views.DestinationDetailView.as_view(), name='destination-detail'),
    path('destinations/<int:destination_id>/reviews/', views.DestinationReviewsView.as_view(), name='destination-reviews'),
    
    # Statistics
    path('stats/', views.destination_stats, name='destination-stats'),
    
    # Bookings (authenticated users only)
    path('bookings/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    
    # Dashboard endpoints
    path('dashboard/overview/', dashboard_views.dashboard_overview, name='dashboard-overview'),
    path('dashboard/bookings/', dashboard_views.dashboard_bookings, name='dashboard-bookings'),
    path('dashboard/activity/', dashboard_views.dashboard_activity, name='dashboard-activity'),
]