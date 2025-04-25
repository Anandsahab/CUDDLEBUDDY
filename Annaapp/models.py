from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class signupmodel(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    confirmpassword=models.CharField(max_length=100)

    def __str__(self):
        return self.username


class PetListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('adopted', 'Adopted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    vaccinated = models.BooleanField(default=False)
    health_details = models.TextField(blank=True)
    personality = models.TextField(blank=True)
    image = models.ImageField(upload_to='pet_uploads/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    persons = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"
    
from django.db import models
from django.contrib.auth.models import User

class PetBooking(models.Model):
    PET_TYPES = [
        ('dogs', 'Dogs'),
        ('cats', 'Cats'),
        ('bird', 'Birds'),
        ('fish', 'Fish'),
        ('rabbits', 'Rabbits'),
        ('horses', 'Horses'),
    ]
    
    PAYMENT_METHODS = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('upi', 'UPI'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pet_name = models.CharField(max_length=100)
    email = models.EmailField()
    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    booking_date = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.pet_name} - {self.pet_type} ({self.email})"
    
from django.db import models

class Pet(models.Model):
    BREED_TYPES = [
        ('SHIH-TZU', 'Shih-Tzu'),
        ('LABRADOR', 'Labrador'),
        ('MALTESE', 'Maltese'),
        ('GOLDEN_RETRIEVER', 'Golden Retriever'),
        ('BEAGLE', 'Beagle'),
        ('SIBERIAN_HUSKY', 'Siberian Husky'),
        ('GERMAN_SHEPHERD', 'German Shepherd'),
        ('BULLDOG', 'Bulldog'),
        ('POODLE', 'Poodle'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, choices=BREED_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/')
    view_count = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.breed}"
    
from django.contrib import admin
from .models import Pet, PetBooking

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'available', 'view_count', 'date_added')
    list_filter = ('breed', 'available')
    search_fields = ('name', 'breed', 'description')
    readonly_fields = ('view_count',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'breed', 'description', 'image')
        }),
        ('Status', {
            'fields': ('available', 'view_count')
        }),
    )

class PetBookingAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'pet_type', 'email', 'booking_date')
    list_filter = ('pet_type', 'booking_date', 'payment_method')
    search_fields = ('pet_name', 'email', 'breed', 'address')
    readonly_fields = ('booking_date',)

admin.site.register(Pet, PetAdmin)
admin.site.register(PetBooking, PetBookingAdmin)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100,default='')
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    persons = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"
