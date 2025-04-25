from django.core.management.base import BaseCommand
import os
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Download pet tip images for the carousel'

    def handle(self, *args, **options):
        # Create images directory if it doesn't exist
        images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        os.makedirs(images_dir, exist_ok=True)

        # List of images to download with their URLs and filenames
        images = [
            {
                'url': 'https://images.pexels.com/photos/6646917/pexels-photo-6646917.jpeg',
                'filename': 'pet-grooming-tip.jpg',
                'description': 'Dog grooming image showing a small dog being brushed'
            },
            {
                'url': 'https://images.pexels.com/photos/7725950/pexels-photo-7725950.jpeg',
                'filename': 'aquarium-care-tip.jpg',
                'description': 'Aquarium with colorful fish and plants'
            },
            {
                'url': 'https://images.pexels.com/photos/2317904/pexels-photo-2317904.jpeg',
                'filename': 'bird-care-tip.jpg',
                'description': 'Colorful parrot perched on a branch'
            }
        ]

        # Download each image
        for image in images:
            file_path = os.path.join(images_dir, image['filename'])
            
            # Skip if file already exists
            if os.path.exists(file_path):
                self.stdout.write(self.style.SUCCESS(f"Image already exists: {image['filename']}"))
                continue
                
            try:
                response = requests.get(image['url'], stream=True)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                self.stdout.write(self.style.SUCCESS(
                    f"Downloaded {image['filename']} - {image['description']}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error downloading {image['filename']}: {str(e)}"
                ))
        
        self.stdout.write(self.style.SUCCESS("All pet tip images downloaded successfully!")) 