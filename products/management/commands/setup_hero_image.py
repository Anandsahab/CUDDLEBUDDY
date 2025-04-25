import os
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from pathlib import Path

class Command(BaseCommand):
    help = 'Downloads and sets up the hero image'

    def handle(self, *args, **kwargs):
        # Create the directory if it doesn't exist
        image_dir = Path(settings.STATIC_ROOT) / 'products' / 'images'
        image_dir.mkdir(parents=True, exist_ok=True)

        # URL of a pet-related hero image
        image_url = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg"
        
        # Path to save the image
        image_path = image_dir / 'puppies-basket.jpg'
        
        try:
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Save the image
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully downloaded hero image to {image_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image: {e}')) 