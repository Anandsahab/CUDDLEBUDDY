from django.core.management.base import BaseCommand
from django.core.files import File
from products.models import Category, Product
import os
from django.conf import settings
import shutil
import tempfile
import requests

class Command(BaseCommand):
    help = 'Add sample food and grocery products'

    def download_image(self, url, filename):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile()
                # Write the content
                for block in response.iter_content(1024 * 8):
                    if not block:
                        break
                    temp_file.write(block)
                # Reset file pointer
                temp_file.seek(0)
                return temp_file
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image: {e}'))
        return None

    def handle(self, *args, **kwargs):
        # Create categories with images
        categories_data = [
            {
                'name': 'Pet Food',
                'slug': 'pet-food',
                'description': 'High-quality food for your pets',
                'image_url': 'https://m.media-amazon.com/images/I/71nC8hZVTtL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'name': 'Pet Grocery',
                'slug': 'pet-grocery',
                'description': 'Essential grocery items for your pets',
                'image_url': 'https://m.media-amazon.com/images/I/81L8-4NxHAL._AC_UF1000,1000_QL80_.jpg'
            }
        ]

        # Create categories and add images
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': cat_data['slug'],
                    'description': cat_data['description']
                }
            )

            if 'image_url' in cat_data:
                image_name = f"{cat_data['slug']}.jpg"
                temp_file = self.download_image(cat_data['image_url'], image_name)
                if temp_file:
                    try:
                        category.image.save(image_name, File(temp_file), save=True)
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully added image for category "{category.name}"')
                        )
                    finally:
                        temp_file.close()

        # Get categories for products
        food_category = Category.objects.get(slug='pet-food')
        grocery_category = Category.objects.get(slug='pet-grocery')

        # Sample products data with image URLs
        products_data = [
            {
                'category': food_category,
                'name': 'Premium Dog Food',
                'slug': 'premium-dog-food',
                'description': 'High-quality dog food with balanced nutrition',
                'price': 999.99,
                'stock': 50,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/71fwkZg9m6L._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': food_category,
                'name': 'Gourmet Cat Food',
                'slug': 'gourmet-cat-food',
                'description': 'Delicious cat food with premium ingredients',
                'price': 799.99,
                'stock': 40,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/71aqBvbPKEL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': food_category,
                'name': 'Fish Food Flakes',
                'slug': 'fish-food-flakes',
                'description': 'Nutritious flakes for all types of fish',
                'price': 299.99,
                'stock': 60,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/71R8iSuNnfL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': food_category,
                'name': 'Bird Seed Mix',
                'slug': 'bird-seed-mix',
                'description': 'Premium seed mix for pet birds',
                'price': 399.99,
                'stock': 45,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/81Y0VHEg9AL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': grocery_category,
                'name': 'Pet Grooming Kit',
                'slug': 'pet-grooming-kit',
                'description': 'Complete grooming kit for pets',
                'price': 1499.99,
                'stock': 25,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/71cVOgvystL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': grocery_category,
                'name': 'Pet Toys Bundle',
                'slug': 'pet-toys-bundle',
                'description': 'Collection of fun toys for your pets',
                'price': 699.99,
                'stock': 30,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/81gZYJ6F9ML._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': grocery_category,
                'name': 'Pet Bed Deluxe',
                'slug': 'pet-bed-deluxe',
                'description': 'Comfortable and stylish bed for pets',
                'price': 1299.99,
                'stock': 20,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/71RN3u5yYjL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'category': grocery_category,
                'name': 'Pet Carrier',
                'slug': 'pet-carrier',
                'description': 'Safe and comfortable carrier for pets',
                'price': 899.99,
                'stock': 15,
                'featured': True,
                'image_url': 'https://m.media-amazon.com/images/I/71jz42mRYYL._AC_UF1000,1000_QL80_.jpg'
            }
        ]

        # Add products
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': product_data['category'],
                    'slug': product_data['slug'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'featured': product_data['featured']
                }
            )

            # Download and set the product image
            if created and 'image_url' in product_data:
                image_name = f"{product_data['slug']}.jpg"
                temp_file = self.download_image(product_data['image_url'], image_name)
                if temp_file:
                    try:
                        product.image.save(image_name, File(temp_file), save=True)
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully added image for "{product.name}"')
                        )
                    finally:
                        temp_file.close()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created product "{product.name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product "{product.name}" already exists')
                ) 