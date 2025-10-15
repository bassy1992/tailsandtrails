from django import forms
from django.core.exceptions import ValidationError
from .models import GalleryVideo

class GalleryVideoAdminForm(forms.ModelForm):
    """Custom form for GalleryVideo admin with better URL handling"""
    
    class Meta:
        model = GalleryVideo
        fields = '__all__'
        widgets = {
            'video_url': forms.URLInput(attrs={
                'placeholder': 'https://videos.pexels.com/video-files/...',
                'class': 'vURLField',
                'size': 80
            }),
            'thumbnail': forms.URLInput(attrs={
                'placeholder': 'https://images.pexels.com/photos/...',
                'class': 'vURLField',
                'size': 80
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'cols': 80
            }),
            'duration': forms.TextInput(attrs={
                'placeholder': 'e.g., 2:30, 10:15',
                'size': 10
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        video_url = cleaned_data.get('video_url')
        
        # Ensure either video_file or video_url is provided, but not both
        if not video_file and not video_url:
            raise ValidationError("Please provide either a video file or a video URL.")
        
        if video_file and video_url:
            raise ValidationError("Please provide either a video file OR a video URL, not both.")
        
        # Validate video URL format if provided
        if video_url:
            valid_extensions = ['.mp4', '.webm', '.ogg', '.mov']
            valid_domains = ['videos.pexels.com', 'player.vimeo.com', 'www.youtube.com', 'youtu.be']
            
            is_valid_extension = any(video_url.lower().endswith(ext) for ext in valid_extensions)
            is_valid_domain = any(domain in video_url.lower() for domain in valid_domains)
            
            if not (is_valid_extension or is_valid_domain):
                raise ValidationError(
                    "Video URL should be a direct link to a video file (MP4, WebM, OGG, MOV) "
                    "or from a supported platform (Pexels, Vimeo, YouTube)."
                )
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add help text
        self.fields['video_file'].help_text = "Upload a video file (optional if using video URL)"
        self.fields['video_url'].help_text = "External video URL - use this for Pexels, Vimeo, or direct video links"
        self.fields['thumbnail'].help_text = "Thumbnail image URL (required)"
        self.fields['duration'].help_text = "Video duration in MM:SS or HH:MM:SS format"