from django import forms

from .models import Review

class ReviewForm(forms.Form):
    rating: forms.IntegerField(
        max_value=5,
        min_value=1,
        required=True
    )
    description: forms.TextInput()
    class Meta:
        model = Review

