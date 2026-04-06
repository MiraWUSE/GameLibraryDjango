from django.contrib import admin
from .models import LibraryGame, Character3D


@admin.register(LibraryGame)
class LibraryGameAdmin(admin.ModelAdmin):
    list_display = ('title', 'engine', 'release_year', 'rating', 'save_progress', 'logo_preview')
    list_filter = ('engine', 'release_year', 'purchase_date')
    search_fields = ('title', 'developer')
    readonly_fields = ('logo_preview',)
    ordering = ('-release_year',)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" width="50" height="50" style="object-fit:cover; border-radius:4px;">'
        return '—'
    logo_preview.short_description = 'Обложка'
    logo_preview.allow_tags = True


class CharacterInline(admin.TabularInline):
    model = Character3D
    extra = 1
    fields = ('name', 'role', 'polygon_count', 'has_rig', 'texture_resolution')


@admin.register(Character3D)
class Character3DAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'role', 'polygon_count', 'has_rig', 'texture_resolution', 'thumbnail_preview')
    list_filter = ('role', 'has_rig', 'texture_resolution', 'created_date')
    search_fields = ('name', 'game__title')
    ordering = ('-created_date',)

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return f'<img src="{obj.thumbnail.url}" width="50" height="50" style="object-fit:cover; border-radius:4px;">'
        return '—'
    thumbnail_preview.short_description = 'Превью'
    thumbnail_preview.allow_tags = True

# Отобразим персонажей прямо в карточке игры
LibraryGameAdmin.inlines = [CharacterInline]