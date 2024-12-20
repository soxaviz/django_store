from django import forms
from .models import Review, Category, Subcategory


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'content',
            'rating'
        ]
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
            }),

        }


class SearchForm(forms.Form):
    q = forms.CharField(label='Поиск', max_length=255, required=False)