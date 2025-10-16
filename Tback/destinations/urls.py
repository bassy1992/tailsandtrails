from django.urls import path
from . import views, dashboard_views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Destinations
    path('destinations/', views.DestinationListView.as_view(), name='destination-list'),
    path('destinations/<int:pk>/', views.DestinationDetailView.as_view(), name='destination-detail-by-id'),
    path('destinations/<slug:slug>/', views.DestinationDetailView.as_view(), name='destination-detail'),
    path('destinations/<int:destination_id>/reviews/', views.DestinationReviewsView.as_view(), name='destination-reviews'),
    path('destinations/<int:destination_id>/pricing/', views.destination_pricing, name='destination-pricing'),
    
    # Statistics
    path('stats/', views.destination_stats, name='destination-stats'),
    
    # Bookings (authenticated users only)
    path('bookings/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    
    # Image Upload endpoints (admin only)
    path('destinations/<int:pk>/upload-image/', views.DestinationImageUploadView.as_view(), name='destination-image-upload'),
    path('destinations/<int:destination_id>/gallery/', views.DestinationGalleryListView.as_view(), name='destination-gallery-list'),
    path('destinations/<int:destination_id>/gallery/bulk-add/', views.bulk_add_destination_images, name='destination-gallery-bulk-add'),
    path('destinations/gallery/upload/', views.DestinationGalleryUploadView.as_view(), name='destination-gallery-upload'),
    path('destinations/gallery/<int:pk>/delete/', views.DestinationGalleryDeleteView.as_view(), name='destination-gallery-delete'),
    
    # Dashboard endpoints
    path('dashboard/overview/', dashboard_views.dashboard_overview, name='dashboard-overview'),
    path('dashboard/bookings/', dashboard_views.dashboard_bookings, name='dashboard-bookings'),
    path('dashboard/activity/', dashboard_views.dashboard_activity, name='dashboard-activity'),
]