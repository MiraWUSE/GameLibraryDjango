from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class EngineChoices(models.TextChoices):
    UNITY = 'Unity', 'Unity'
    UNREAL = 'Unreal Engine', 'Unreal Engine'
    GODOT = 'Godot', 'Godot'
    CUSTOM = 'Custom', 'Другой/Кастомный'


class LibraryGame(models.Model):
    title = models.CharField('Название игры', max_length=150)
    developer = models.CharField('Разработчик', max_length=100, blank=True)
    engine = models.CharField('Движок', max_length=20, choices=EngineChoices.choices)
    release_year = models.PositiveIntegerField('Год выхода')
    rating = models.DecimalField('Оценка', max_digits=3, decimal_places=1, 
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    purchase_date = models.DateField('Дата покупки', blank=True, null=True)
    save_progress = models.PositiveIntegerField('Прогресс прохождения %', default=0,
                                                validators=[MaxValueValidator(100)])
    logo = models.ImageField('Логотип/Обложка', upload_to='games/logos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Игра в коллекции'
        verbose_name_plural = 'Игры в коллекции'
        ordering = ['-release_year', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:game_detail', kwargs={'pk': self.pk})


class Character3D(models.Model):
    name = models.CharField('Имя персонажа', max_length=100)
    game = models.ForeignKey(LibraryGame, on_delete=models.CASCADE, related_name='characters', verbose_name='Игра')
    created_date = models.DateField('Дата создания/добавления', auto_now_add=True)
    thumbnail = models.ImageField('Превью модели', upload_to='characters/thumbnails/', blank=True, null=True)
    model_file = models.FileField('3D модель', upload_to='characters/models/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = '3D-персонаж'
        verbose_name_plural = '3D-персонажи'
        ordering = ['-created_date', 'name']

    def __str__(self):
        return self.name