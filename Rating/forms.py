from django import forms
from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['price_rating', 'source_rating', 'speed_rating', 'comment']
        widgets = {
            'price_rating': forms.HiddenInput(attrs={'id': "price-rating"}),
            'source_rating': forms.HiddenInput(attrs={'id': "store-rating"}),
            'speed_rating': forms.HiddenInput(attrs={'id': "delivery-rating"}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'placeholder': '寫下你的評論......'})
        }


class RatingUpdateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['price_rating', 'source_rating', 'speed_rating', 'comment']
        widgets = {
            'price_rating': forms.HiddenInput(attrs={'id': "price-rating"}),
            'source_rating': forms.HiddenInput(attrs={'id': "store-rating"}),
            'speed_rating': forms.HiddenInput(attrs={'id': "delivery-rating"}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'placeholder': '寫下你的評論......'})
        }
