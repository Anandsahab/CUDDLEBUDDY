from django.contrib import admin
from .models import signupmodel, PetListing
from .models import ContactMessage
from .models import Appointment

class signupadmin(admin.ModelAdmin):
    list_display=['username','password','email']
# Register your models here.

admin.site.register(signupmodel,signupadmin)

@admin.register(PetListing)
class PetListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'user', 'status', 'date_posted')
    list_filter = ('status', 'species', 'date_posted')
    search_fields = ('name', 'breed', 'user__username')
    list_editable = ('status',)  # Optional: lets you approve/reject directly from the list view


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'time', 'persons')
    list_filter = ('date',)
    search_fields = ('name', 'email', 'phone')


