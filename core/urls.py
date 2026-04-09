from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    # Игры
    path('', views.GameListView.as_view(), name='game_list'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('game/create/', views.GameCreateView.as_view(), name='game_create'),
    path('game/<int:pk>/update/', views.GameUpdateView.as_view(), name='game_update'),
    path('game/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    
    # Персонажи
    path('character/create/', views.CharacterCreateView.as_view(), name='character_create'),
    path('character/<int:pk>/update/', views.CharacterUpdateView.as_view(), name='character_update'),
    path('character/<int:pk>/delete/', views.CharacterDeleteView.as_view(), name='character_delete'),
    
    # AJAX
    path('ajax/filter-games/', views.ajax_filter_games, name='ajax_filter_games'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)