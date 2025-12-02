# Generated migration for gallery models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0004_pricingtier'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Gallery Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='GalleryVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('video_url', models.URLField(help_text='YouTube, Vimeo, or direct video URL', max_length=500)),
                ('thumbnail_url', models.URLField(blank=True, max_length=500)),
                ('duration', models.CharField(blank=True, help_text='e.g., 2:30', max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='destinations.gallerycategory')),
            ],
            options={
                'verbose_name': 'Gallery Video',
                'verbose_name_plural': 'Gallery Videos',
                'ordering': ['-is_featured', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(max_length=500)),
                ('thumbnail_url', models.URLField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('photographer', models.CharField(blank=True, max_length=100)),
                ('is_featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='destinations.gallerycategory')),
            ],
            options={
                'verbose_name': 'Gallery Image',
                'verbose_name_plural': 'Gallery Images',
                'ordering': ['-is_featured', 'order', '-created_at'],
            },
        ),
    ]
