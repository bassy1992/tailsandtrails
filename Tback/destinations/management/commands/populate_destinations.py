from django.core.management.base import BaseCommand
from destinations.models import Category, Destination, DestinationHighlight, DestinationInclude

class Command(BaseCommand):
    help = 'Populate destinations with sample data from the frontend'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            {'name': 'Heritage', 'description': 'Historical and cultural heritage sites'},
            {'name': 'Nature', 'description': 'Natural landscapes and outdoor experiences'},
            {'name': 'Culture', 'description': 'Cultural immersion and traditional experiences'},
            {'name': 'Adventure', 'description': 'Thrilling and adventurous activities'},
            {'name': 'Urban', 'description': 'City tours and urban experiences'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        self.stdout.write('Creating destinations...')
        
        # Sample destinations data from the frontend
        destinations_data = [
            {
                'name': 'Cape Coast Castle Heritage Tour',
                'location': 'Cape Coast',
                'image': 'https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 450,
                'duration': '2_days',
                'max_group_size': 15,
                'rating': 4.8,
                'reviews_count': 124,
                'category': 'Heritage',
                'description': 'Explore the historic Cape Coast Castle, learn about the transatlantic slave trade, and visit local fishing communities.',
                'highlights': ['UNESCO World Heritage Site', 'Guided Historical Tour', 'Local Culture Experience', 'Coastal Views'],
                'includes': ['Transport', 'Accommodation', 'Meals', 'Professional Guide', 'Entry Fees']
            },  
          {
                'name': 'Aburi Gardens Nature Escape',
                'location': 'Aburi',
                'image': 'https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 280,
                'duration': '1_day',
                'max_group_size': 20,
                'rating': 4.6,
                'reviews_count': 89,
                'category': 'Nature',
                'description': 'Relax in the beautiful botanical gardens with stunning mountain views and exotic plant species.',
                'highlights': ['Botanical Gardens', 'Mountain Views', 'Photography', 'Fresh Air'],
                'includes': ['Transport', 'Lunch', 'Garden Entry', 'Guide']
            },
            {
                'name': 'Manhyia Palace Cultural Tour',
                'location': 'Kumasi',
                'image': 'https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 350,
                'duration': '1_day',
                'max_group_size': 12,
                'rating': 4.7,
                'reviews_count': 156,
                'category': 'Culture',
                'description': 'Visit the seat of the Asantehene, explore Ashanti culture, and witness traditional crafts.',
                'highlights': ['Royal Palace Visit', 'Ashanti Culture', 'Traditional Crafts', 'Royal Museum'],
                'includes': ['Transport', 'Cultural Guide', 'Palace Entry', 'Lunch', 'Craft Workshop']
            },
            {
                'name': 'Kakum Canopy Walk Adventure',
                'location': 'Kakum National Park',
                'image': 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 520,
                'duration': '3_days',
                'max_group_size': 10,
                'rating': 4.9,
                'reviews_count': 203,
                'category': 'Adventure',
                'description': 'Experience the thrilling canopy walk 40 meters above the forest floor and explore pristine rainforest.',
                'highlights': ['Canopy Walk', 'Rainforest Exploration', 'Wildlife Spotting', 'Nature Photography'],
                'includes': ['Transport', 'Accommodation', 'All Meals', 'Park Fees', 'Professional Guide', 'Safety Equipment']
            },         
   {
                'name': 'Volta Region Waterfalls Tour',
                'location': 'Volta Region',
                'image': 'https://images.pexels.com/photos/12190172/pexels-photo-12190172.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 680,
                'duration': '4_days',
                'max_group_size': 8,
                'rating': 4.5,
                'reviews_count': 78,
                'category': 'Nature',
                'description': 'Discover the breathtaking Wli Waterfalls and explore the mountainous Volta Region.',
                'highlights': ['Wli Waterfalls', 'Mountain Hiking', 'Local Villages', 'Cultural Exchange'],
                'includes': ['Transport', 'Accommodation', 'All Meals', 'Hiking Guide', 'Village Visits']
            },
            {
                'name': 'Elmina Castle & Beach Resort',
                'location': 'Elmina',
                'image': 'https://images.pexels.com/photos/3561167/pexels-photo-3561167.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 420,
                'duration': '2_days',
                'max_group_size': 18,
                'rating': 4.4,
                'reviews_count': 92,
                'category': 'Heritage',
                'description': 'Explore Elmina Castle and enjoy beautiful beaches with fishing village experiences.',
                'highlights': ['Historic Castle', 'Beach Relaxation', 'Fishing Village', 'Local Seafood'],
                'includes': ['Transport', 'Beach Resort Stay', 'Meals', 'Castle Tour', 'Beach Activities']
            },
            {
                'name': 'Northern Ghana Cultural Safari',
                'location': 'Tamale',
                'image': 'https://images.pexels.com/photos/20261457/pexels-photo-20261457.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 950,
                'duration': '7_days',
                'max_group_size': 6,
                'rating': 4.9,
                'reviews_count': 45,
                'category': 'Culture',
                'description': 'Immerse yourself in Northern Ghana\'s rich culture, visit traditional villages, and experience authentic hospitality.',
                'highlights': ['Traditional Villages', 'Cultural Immersion', 'Local Festivals', 'Authentic Cuisine'],
                'includes': ['Transport', 'Accommodation', 'All Meals', 'Cultural Guide', 'Village Experiences', 'Traditional Performances']
            },           
 {
                'name': 'Accra City & Nightlife Tour',
                'location': 'Accra',
                'image': 'https://images.pexels.com/photos/1422408/pexels-photo-1422408.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 180,
                'duration': '1_day',
                'max_group_size': 25,
                'rating': 4.3,
                'reviews_count': 167,
                'category': 'Urban',
                'description': 'Explore Ghana\'s capital city, visit markets, museums, and experience vibrant nightlife.',
                'highlights': ['City Landmarks', 'Local Markets', 'Nightlife', 'Modern Ghana'],
                'includes': ['Transport', 'City Guide', 'Market Tour', 'Lunch', 'Museum Entries']
            },
            {
                'name': 'Akosombo Dodi Island Boat Cruise',
                'location': 'Akosombo',
                'image': 'https://images.pexels.com/photos/1354234/pexels-photo-1354234.jpeg?auto=compress&cs=tinysrgb&w=800',
                'price': 390,
                'duration': '2_days',
                'max_group_size': 16,
                'rating': 4.6,
                'reviews_count': 89,
                'category': 'Nature',
                'description': 'Enjoy a relaxing boat cruise on Lake Volta, visit the beautiful Dodi Island, and experience serene waters and lush landscapes.',
                'highlights': ['Lake Volta Cruise', 'Dodi Island Visit', 'Scenic Landscapes', 'Water Activities', 'Peaceful Retreat'],
                'includes': ['Boat Transport', 'Island Accommodation', 'All Meals', 'Professional Captain', 'Life Jackets', 'Island Tour Guide']
            }
        ]

        # Create destinations
        for dest_data in destinations_data:
            category = categories[dest_data['category']]
            
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                defaults={
                    'location': dest_data['location'],
                    'image': dest_data['image'],
                    'price': dest_data['price'],
                    'duration': dest_data['duration'],
                    'max_group_size': dest_data['max_group_size'],
                    'rating': dest_data['rating'],
                    'reviews_count': dest_data['reviews_count'],
                    'category': category,
                    'description': dest_data['description'],
                    'is_active': True,
                    'is_featured': dest_data['rating'] >= 4.7,
                }
            )
            
            if created:
                self.stdout.write(f'Created destination: {destination.name}')
                
                # Add highlights
                for i, highlight in enumerate(dest_data['highlights']):
                    DestinationHighlight.objects.create(
                        destination=destination,
                        highlight=highlight,
                        order=i
                    )
                
                # Add includes
                for i, include in enumerate(dest_data['includes']):
                    DestinationInclude.objects.create(
                        destination=destination,
                        item=include,
                        order=i
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated destinations database!')
        )