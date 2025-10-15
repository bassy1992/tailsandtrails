"""
Admin helper functions for gallery management
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import ImageGallery, GalleryImage, GalleryCategory
from destinations.models import Destination

class MultiImageUploadMixin:
    """Mixin to add multi-image upload functionality to admin"""
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='gallery_bulk_upload'),
        ]
        return custom_urls + urls
    
    def bulk_upload_view(self, request):
        """View for bulk uploading images"""
        if request.method == 'POST':
            return self.handle_bulk_upload(request)
        
        # Get categories and destinations for the form
        categories = GalleryCategory.objects.all()
        destinations = Destination.objects.all()
        
        context = {
            'title': 'Bulk Upload Images',
            'categories': categories,
            'destinations': destinations,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        
        return render(request, 'admin/gallery/bulk_upload.html', context)
    
    def handle_bulk_upload(self, request):
        """Handle the bulk upload form submission"""
        try:
            gallery_title = request.POST.get('gallery_title', '').strip()
            location = request.POST.get('location', '').strip()
            description = request.POST.get('description', '').strip()
            category_id = request.POST.get('category_id')
            destination_id = request.POST.get('destination_id')
            photographer = request.POST.get('photographer', '').strip()
            is_featured = request.POST.get('is_featured') == 'on'
            image_urls = request.POST.get('image_urls', '').strip()
            
            # Validation
            if not gallery_title or not location or not category_id or not image_urls:
                messages.error(request, 'Gallery title, location, category, and image URLs are required.')
                return redirect('admin:gallery_bulk_upload')
            
            # Parse image URLs
            urls = [url.strip() for url in image_urls.split('\n') if url.strip()]
            if not urls:
                messages.error(request, 'Please provide at least one image URL.')
                return redirect('admin:gallery_bulk_upload')
            
            # Get category and destination
            try:
                category = GalleryCategory.objects.get(id=category_id)
            except GalleryCategory.DoesNotExist:
                messages.error(request, 'Selected category does not exist.')
                return redirect('admin:gallery_bulk_upload')
            
            destination = None
            if destination_id:
                try:
                    destination = Destination.objects.get(id=destination_id)
                except Destination.DoesNotExist:
                    messages.error(request, 'Selected destination does not exist.')
                    return redirect('admin:gallery_bulk_upload')
            
            # Create the gallery
            gallery = ImageGallery.objects.create(
                title=gallery_title,
                description=description,
                location=location,
                category=category,
                destination=destination,
                photographer=photographer,
                is_featured=is_featured,
                is_active=True
            )
            
            # Add images
            created_count = 0
            errors = []
            
            for i, url in enumerate(urls):
                try:
                    if not url.startswith(('http://', 'https://')):
                        errors.append(f"Invalid URL format: {url}")
                        continue
                    
                    GalleryImage.objects.create(
                        gallery=gallery,
                        image=url,
                        caption=f"Image {i + 1} from {location}",
                        is_main=i == 0,  # First image is main
                        order=i
                    )
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Error adding {url}: {str(e)}")
            
            # Show results
            if created_count > 0:
                messages.success(
                    request, 
                    f'Successfully created gallery "{gallery.title}" with {created_count} images.'
                )
            
            if errors:
                for error in errors:
                    messages.warning(request, error)
            
            return redirect('admin:gallery_imagegallery_change', gallery.id)
            
        except Exception as e:
            messages.error(request, f'Error creating gallery: {str(e)}')
            return redirect('admin:gallery_bulk_upload')

def add_bulk_upload_button(modeladmin, request, queryset):
    """Admin action to redirect to bulk upload"""
    return redirect('admin:gallery_bulk_upload')

add_bulk_upload_button.short_description = "Bulk upload images to new gallery"