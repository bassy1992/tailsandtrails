from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    # Categories
    path('categories/', views.GalleryCategoryListView.as_view(), name='category-list'),
    
    # Images
    path('images/', views.GalleryImageListView.as_view(), name='image-list'),
    path('images/<slug:slug>/', views.GalleryImageDetailView.as_view(), name='image-detail'),
    
    # Videos
    path('videos/', views.GalleryVideoListView.as_view(), name='video-list'),
    path('videos/<slug:slug>/', views.GalleryVideoDetailView.as_view(), name='video-detail'),
    
    # Mixed feed and stats
    path('feed/', views.gallery_mixed_feed, name='mixed-feed'),
    path('stats/', views.gallery_stats, name='stats'),
]