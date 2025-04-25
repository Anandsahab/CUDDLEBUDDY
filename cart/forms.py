from django import forms
from django.forms import widgets

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=widgets.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 5rem;',
            'min': '1',
            'max': '20'
        })
    )
    override = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput) 