from django import forms
from .models import LibraryGame, Character3D


class LibraryGameForm(forms.ModelForm):
    class Meta:
        model = LibraryGame
        fields = ['title', 'developer', 'engine', 'release_year', 'rating', 
                  'purchase_date', 'save_progress', 'logo']
        # Стилизация полей и плейсхолдеры
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название игры'}),
            'developer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Разработчик'}),
            'engine': forms.Select(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '8.5'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'save_progress': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }

    # Валидация оценки (0–10)
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 0 or rating > 10):
            raise forms.ValidationError('Оценка должна быть от 0 до 10')
        return rating

    # Валидация года выпуска
    def clean_release_year(self):
        year = self.cleaned_data.get('release_year')
        if year and (year < 1970 or year > 2030):
            raise forms.ValidationError('Некорректный год выпуска')
        return year


class Character3DForm(forms.ModelForm):
    class Meta:
        model = Character3D
        fields = ['name', 'game', 'model_file', 'thumbnail', 'description']
        # Настройка типов полей и ограничений
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя персонажа'}),
            'game': forms.Select(attrs={'class': 'form-control'}),
            'model_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.gltf,.glb,.obj,.fbx'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Описание персонажа...'
            }),
        }
        # Заголовки полей в форме
        labels = {
            'name': 'Имя персонажа',
            'game': 'Игра',
            'model_file': 'Файл 3D-модели',
            'thumbnail': 'Изображение превью',
            'description': 'Описание', 
        }
        # Подсказки под полями
        help_texts = {
            'model_file': 'Поддерживаемые форматы: GLB, GLTF, OBJ, FBX',
            'thumbnail': 'Рекомендуемый размер: 800×600 px',
            'description': 'Краткое описание персонажа, его особенности и роль в игре',
        }

    # Блокировка поля "Игра" при редактировании существующего персонажа
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('game') or (self.instance.pk and self.instance.game_id):
            self.fields['game'].widget.attrs['disabled'] = True
            self.fields['game'].required = False