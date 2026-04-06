from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class EngineChoices(models.TextChoices):
    UNITY = 'Unity', 'Unity'
    UNREAL = 'Unreal Engine', 'Unreal Engine'
    GODOT = 'Godot', 'Godot'
    CUSTOM = 'Custom', 'Другой/Кастомный'


class RoleChoices(models.TextChoices):
    PROTAGONIST = 'protagonist', 'Главный герой'
    COMPANION = 'companion', 'Напарник'
    ENEMY = 'enemy', 'Противник'
    BOSS = 'boss', 'Босс'
    NPC = 'npc', 'NPC'


class TextureChoices(models.TextChoices):
    K1 = '1K', '1024x1024'
    K2 = '2K', '2048x2048'
    K4 = '4K', '4096x4096'
    K8 = '8K', '8192x8192'


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


class Character3D(models.Model):
    name = models.CharField('Имя персонажа', max_length=100)
    game = models.ForeignKey(LibraryGame, on_delete=models.CASCADE, related_name='characters',
                             verbose_name='Игра')
    role = models.CharField('Роль', max_length=20, choices=RoleChoices.choices)
    polygon_count = models.PositiveIntegerField('Количество полигонов')
    has_rig = models.BooleanField('Есть риг (скелет)', default=False)
    texture_resolution = models.CharField('Разрешение текстур', max_length=10, choices=TextureChoices.choices)
    created_date = models.DateField('Дата создания/добавления', auto_now_add=True)
    thumbnail = models.ImageField('Превью модели', upload_to='characters/thumbnails/', blank=True, null=True)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = '3D-персонаж'
        verbose_name_plural = '3D-персонажи'
        ordering = ['-created_date', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"