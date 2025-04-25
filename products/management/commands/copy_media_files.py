import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Copy media files from original project to integrated project'

    def handle(self, *args, **options):
        # Define paths
        original_project_root = Path('C:/Desktop/Project3')
        integrated_project_root = Path('C:/Desktop/Project3/Annaproject/Annaproject/Annaproject')
        
        # Product images
        original_products_path = original_project_root / 'media' / 'products'
        target_products_path = integrated_project_root / 'media' / 'products'
        
        # Category images
        original_categories_path = original_project_root / 'media' / 'categories'
        target_categories_path = integrated_project_root / 'media' / 'categories'
        
        # Ensure target directories exist
        os.makedirs(target_products_path, exist_ok=True)
        os.makedirs(target_categories_path, exist_ok=True)
        
        # Copy product images
        if original_products_path.exists():
            self.stdout.write(f"Copying product images from {original_products_path} to {target_products_path}")
            self._copy_directory(original_products_path, target_products_path)
        else:
            self.stdout.write(self.style.WARNING(f"Original products path {original_products_path} does not exist"))
        
        # Copy category images
        if original_categories_path.exists():
            self.stdout.write(f"Copying category images from {original_categories_path} to {target_categories_path}")
            self._copy_directory(original_categories_path, target_categories_path)
        else:
            self.stdout.write(self.style.WARNING(f"Original categories path {original_categories_path} does not exist"))
        
        self.stdout.write(self.style.SUCCESS('Successfully copied media files'))
    
    def _copy_directory(self, source, destination):
        """Copy all contents from source to destination directory."""
        if not os.path.exists(source):
            return
        
        # Walk through the source directory
        for root, dirs, files in os.walk(source):
            # Calculate the relative path from source to current directory
            rel_path = os.path.relpath(root, source)
            
            # Create the same directory structure in destination
            if rel_path != '.':
                os.makedirs(os.path.join(destination, rel_path), exist_ok=True)
            
            # Copy all files
            for file in files:
                source_file = os.path.join(root, file)
                # If we're in the root directory, place files directly in destination
                if rel_path == '.':
                    dest_file = os.path.join(destination, file)
                else:
                    dest_file = os.path.join(destination, rel_path, file)
                
                if not os.path.exists(dest_file) or os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                    self.stdout.write(f"  Copying {source_file} to {dest_file}")
                    shutil.copy2(source_file, dest_file)
                else:
                    self.stdout.write(f"  Skipping {source_file} (already exists and is up to date)") 