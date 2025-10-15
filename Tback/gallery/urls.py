from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    # Categories
    path('categories/', views.GalleryCategoryListView.as_view(), name='category-list'),
    
    # Image Galleries
    path('galleries/', views.ImageGalleryListView.as_view(), name='gallery-list'),
    path('galleries/bulk-add/', views.bulk_add_gallery_images, name='galleries-bulk-add'),
    path('galleries/<slug:slug>/', views.ImageGalleryDetailView.as_view(), name='gallery-detail'),
    
    # Videos
    path('videos/', views.GalleryVideoListView.as_view(), name='video-list'),
    path('videos/<slug:slug>/', views.GalleryVideoDetailView.as_view(), name='video-detail'),
    
    # Mixed feed and stats
    path('feed/', views.gallery_mixed_feed, name='mixed-feed'),
    path('stats/', views.gallery_stats, name='stats'),
]