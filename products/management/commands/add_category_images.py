import os
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category
from django.conf import settings
import shutil
from pathlib import Path

class Command(BaseCommand):
    help = 'Add or update images for existing categories'

    def handle(self, *args, **options):
        # Create the categories directory if it doesn't exist
        media_root = settings.MEDIA_ROOT
        categories_dir = os.path.join(media_root, 'categories')
        os.makedirs(categories_dir, exist_ok=True)
        
        # Category image URLs - using more reliable URLs
        category_images = {
            'bird-supplies': 'https://images.pexels.com/photos/2662438/pexels-photo-2662438.jpeg',
            'cat-food': 'https://images.pexels.com/photos/8473457/pexels-photo-8473457.jpeg',
            'dog-food': 'https://images.pexels.com/photos/6568956/pexels-photo-6568956.jpeg',
            'fish-aquatics': 'https://images.pexels.com/photos/691569/pexels-photo-691569.jpeg',
            'pet-accessories': 'https://images.pexels.com/photos/406152/pexels-photo-406152.jpeg'
        }
        
        # Process each category
        categories = Category.objects.all()
        self.stdout.write(f"Found {categories.count()} categories")
        
        for category in categories:
            self.stdout.write(f"Processing category: {category.name} (slug: {category.slug})")
            
            # Check if we have an image URL for this category
            image_url = category_images.get(category.slug)
            if not image_url:
                self.stdout.write(self.style.WARNING(f"No image URL defined for category: {category.slug}"))
                continue
            
            try:
                # Download the image
                response = requests.get(image_url)
                response.raise_for_status()  # Check for HTTP errors
                
                # Save image to category model
                image_name = f"{category.slug}.jpg"
                
                # First save to a local file
                local_path = os.path.join(categories_dir, image_name)
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                self.stdout.write(f"Saved image to {local_path}")
                
                # Then update the model to point to this file
                category.image = f'categories/{image_name}'
                category.save()
                
                self.stdout.write(self.style.SUCCESS(f"Added image for category: {category.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding image for {category.name}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS("Category image update completed!")) 