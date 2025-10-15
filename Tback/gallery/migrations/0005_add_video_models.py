# Generated manually to add video models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_alter_imagegallery_id'),
        ('destinations', '0006_alter_destination_image_alter_destinationimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('video_file', models.FileField(upload_to='gallery/videos/%Y/%m/', null=True, blank=True)),
                ('thumbnail', models.URLField(help_text='Video thumbnail URL', max_length=500)),
                ('duration', models.CharField(help_text='Format: MM:SS or HH:MM:SS', max_length=10)),
                ('file_size', models.PositiveIntegerField(blank=True, help_text='File size in bytes', null=True)),
                ('resolution', models.CharField(blank=True, help_text='e.g., 1920x1080', max_length=20)),
                ('location', models.CharField(max_length=200)),
                ('videographer', models.CharField(blank=True, max_length=100)),
                ('date_recorded', models.DateField(blank=True, null=True)),
                ('equipment_info', models.CharField(blank=True, max_length=200)),
                ('views', models.PositiveIntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='gallery.gallerycategory')),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gallery_videos', to='destinations.destination')),
            ],
            options={
                'verbose_name': 'Gallery Video',
                'verbose_name_plural': 'Gallery Videos',
                'ordering': ['-is_featured', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.gallerytag')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.galleryvideo')),
            ],
            options={
                'unique_together': {('video', 'tag')},
            },
        ),
    ]