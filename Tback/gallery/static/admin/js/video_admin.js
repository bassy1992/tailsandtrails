// Admin JavaScript for video URL handling
(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Add help text and validation for video fields
        var videoFileField = $('#id_video_file');
        var videoUrlField = $('#id_video_url');
        
        if (videoFileField.length && videoUrlField.length) {
            // Add change handlers to show/hide fields based on selection
            function toggleVideoFields() {
                var hasFile = videoFileField.val();
                var hasUrl = videoUrlField.val();
                
                if (hasFile) {
                    videoUrlField.closest('.form-row').hide();
                    videoUrlField.val('');
                } else if (hasUrl) {
                    videoFileField.closest('.form-row').hide();
                } else {
                    videoFileField.closest('.form-row').show();
                    videoUrlField.closest('.form-row').show();
                }
            }
            
            // Add event listeners
            videoFileField.on('change', toggleVideoFields);
            videoUrlField.on('input', toggleVideoFields);
            
            // Initial toggle
            toggleVideoFields();
            
            // Add helpful placeholder text
            videoUrlField.attr('placeholder', 'https://example.com/video.mp4 or https://videos.pexels.com/...');
            
            // Add URL validation
            videoUrlField.on('blur', function() {
                var url = $(this).val();
                if (url && !url.match(/^https?:\/\/.+\.(mp4|webm|ogg|mov)(\?.*)?$/i)) {
                    if (!url.match(/^https?:\/\/(videos\.pexels\.com|player\.vimeo\.com|www\.youtube\.com)/i)) {
                        alert('Please enter a valid video URL (MP4, WebM, OGG, MOV) or a supported video platform URL.');
                    }
                }
            });
        }
        
        // Auto-fill duration from common video platforms
        videoUrlField.on('input', function() {
            var url = $(this).val();
            var durationField = $('#id_duration');
            
            // Suggest common durations for demo videos
            if (url.includes('pexels.com') && !durationField.val()) {
                durationField.attr('placeholder', 'e.g., 0:30, 2:15, 10:45');
            }
        });
    });
})(django.jQuery);