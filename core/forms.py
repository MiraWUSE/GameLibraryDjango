from django import forms
from .models import LibraryGame, Character3D


class LibraryGameForm(forms.ModelForm):
    class Meta:
        model = LibraryGame
        fields = ['title', 'developer', 'engine', 'release_year', 'rating', 
                  'purchase_date', 'save_progress', 'logo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название игры'}),
            'developer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Разработчик'}),
            'engine': forms.Select(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '8.5'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'save_progress': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 0 or rating > 10):
            raise forms.ValidationError('Оценка должна быть от 0 до 10')
        return rating

    def clean_release_year(self):
        year = self.cleaned_data.get('release_year')
        if year and (year < 1970 or year > 2030):
            raise forms.ValidationError('Некорректный год выпуска')
        return year


class Character3DForm(forms.ModelForm):
    class Meta:
        model = Character3D
        fields = ['name', 'game', 'role', 'polygon_count', 'has_rig', 
                  'texture_resolution', 'thumbnail', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя персонажа'}),
            'game': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'polygon_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50000'}),
            'has_rig': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'texture_resolution': forms.Select(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Заметки...'}),
        }