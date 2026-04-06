from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import LibraryGame, Character3D
from .forms import LibraryGameForm, Character3DForm


class GameListView(ListView):
    model = LibraryGame
    template_name = 'core/game_list.html'
    context_object_name = 'games'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        engine = self.request.GET.get('engine', '')
        min_rating = self.request.GET.get('min_rating', '')
        status = self.request.GET.get('status', '')

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(developer__icontains=search))
        if engine:
            queryset = queryset.filter(engine=engine)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if status:
            queryset = queryset.filter(save_progress__gte=status)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['engines'] = LibraryGame._meta.get_field('engine').choices
        context['current_filters'] = self.request.GET.dict()
        return context


class GameDetailView(DetailView):
    model = LibraryGame
    template_name = 'core/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = self.object.characters.all()
        return context


class GameCreateView(CreateView):
    model = LibraryGame
    form_class = LibraryGameForm
    template_name = 'core/game_form.html'
    success_url = reverse_lazy('core:game_list') 

    def form_valid(self, form):
        messages.success(self.request, f'Игра «{form.instance.title}» успешно добавлена!')
        return super().form_valid(form)


class GameUpdateView(UpdateView):
    model = LibraryGame
    form_class = LibraryGameForm
    template_name = 'core/game_form.html'
    success_url = reverse_lazy('core:game_list')  # ← ИСПРАВЛЕНО

    def form_valid(self, form):
        messages.success(self.request, f'Игра «{form.instance.title}» обновлена!')
        return super().form_valid(form)


class GameDeleteView(DeleteView):
    model = LibraryGame
    template_name = 'core/game_confirm_delete.html'
    success_url = reverse_lazy('core:game_list')  # ← ИСПРАВЛЕНО

    def delete(self, request, *args, **kwargs):
        game_name = self.get_object().title
        messages.warning(request, f'Игра «{game_name}» удалена.')
        return super().delete(request, *args, **kwargs)


# === ПЕРСОНАЖИ ===
class CharacterCreateView(CreateView):
    model = Character3D
    form_class = Character3DForm
    template_name = 'core/character_form.html'

    def get_success_url(self):
        messages.success(self.request, f'Персонаж «{self.object.name}» добавлен!')
        return reverse_lazy('core:game_detail', kwargs={'pk': self.object.game_id})


class CharacterUpdateView(UpdateView):
    model = Character3D
    form_class = Character3DForm
    template_name = 'core/character_form.html'

    def get_success_url(self):
        messages.success(self.request, f'Персонаж «{self.object.name}» обновлён!')
        return reverse_lazy('core:game_detail', kwargs={'pk': self.object.game_id}) 


class CharacterDeleteView(DeleteView):
    model = Character3D
    template_name = 'core/character_confirm_delete.html'

    def get_success_url(self):
        messages.warning(self.request, 'Персонаж удалён.')
        return reverse_lazy('core:game_detail', kwargs={'pk': self.object.game_id})  

# === AJAX: Динамический поиск и фильтрация ===
def ajax_filter_games(request):
    """Обработчик AJAX-запросов для фильтрации без перезагрузки"""
    search = request.GET.get('search', '')
    engine = request.GET.get('engine', '')
    min_rating = request.GET.get('min_rating', '')

    games = LibraryGame.objects.all()

    if search:
        games = games.filter(Q(title__icontains=search) | Q(developer__icontains=search))
    if engine:
        games = games.filter(engine=engine)
    if min_rating:
        games = games.filter(rating__gte=min_rating)

    # Формируем HTML-карточки для возврата
    html = ''
    for game in games:
        html += f'''
        <div class="game-card" data-game-id="{game.id}">
            <div class="game-card__image">
                {'<img src="' + game.logo.url + '" alt="' + game.title + '">' if game.logo else '<div class="no-image">Нет обложки</div>'}
            </div>
            <div class="game-card__content">
                <h3><a href="{game.get_absolute_url()}">{game.title}</a></h3>
                <p class="game-card__meta">{game.get_engine_display()} • {game.release_year}</p>
                <p class="game-card__rating">⭐ {game.rating}/10</p>
                <p class="game-card__progress">Прогресс: {game.save_progress}%</p>
            </div>
        </div>
        '''
    
    if not html:
        html = '<p class="no-results">Ничего не найдено 😔</p>'

    return JsonResponse({'html': html, 'count': games.count()})