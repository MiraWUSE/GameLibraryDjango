from django.contrib import admin
from django.utils.html import format_html
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
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:4px;">', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Обложка'


class CharacterInline(admin.TabularInline):
    model = Character3D
    extra = 1
    fields = ('name', 'model_file', 'thumbnail', 'description')


@admin.register(Character3D)
class Character3DAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'created_date', 'model_file', 'thumbnail_preview')
    list_filter = ('game', 'created_date')
    search_fields = ('name', 'game__title', 'description')
    ordering = ('-created_date',)

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:4px;">', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Превью'


# Подключаем инлайн к админке игр
LibraryGameAdmin.inlines = [CharacterInline]