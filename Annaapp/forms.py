# rehome/forms.py
from django import forms
from .models import PetListing

class PetListingForm(forms.ModelForm):
    class Meta:
        model = PetListing
        exclude = ['user', 'status', 'date_posted', 'reason_for_rehoming']
