/**
 * Поиск игр по названию без перезагрузки страницы
 */
function initAjaxSearch() {
    const searchForm = document.getElementById('header-search');
    const gamesContainer = document.getElementById('games-container');
    const loadingIndicator = document.getElementById('loading');

    if (!searchForm || !gamesContainer) return;

    // Запрос новых результатов с сервера
    function fetchFilteredGames(params) {
        loadingIndicator.classList.remove('hidden');
        
        fetch(`/ajax/filter-games/?${params}`)
            .then(response => response.json())
            .then(data => {
                gamesContainer.innerHTML = data.html;
            })
            .catch(error => {
                console.error('Ошибка поиска:', error);
                gamesContainer.innerHTML = '<p class="no-results">Ошибка загрузки</p>';
            })
            .finally(() => {
                loadingIndicator.classList.add('hidden');
            });
    }

    // Debounce: ждём 300мс после последнего ввода, чтобы не спамить запросами
    let searchTimeout;
    searchForm.addEventListener('input', (e) => {
        if (e.target.name === 'search') {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const params = new URLSearchParams(new FormData(searchForm)).toString();
                fetchFilteredGames(params);
            }, 300);
        }
    });

    // Обработка отправки формы (Enter или кнопка)
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const params = new URLSearchParams(new FormData(searchForm)).toString();
        fetchFilteredGames(params);
    });
}

/**
 * Инициализация после загрузки DOM
 */
document.addEventListener('DOMContentLoaded', function() {
    // Автозакрытие сообщений через 5 секунд
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Кнопка закрытия сообщений вручную
    document.querySelectorAll('.alert__close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    // Включаем поиск, если мы на странице со списком игр
    if (document.getElementById('games-container')) {
        initAjaxSearch();
    }

    // Подтверждение перед удалением
    document.querySelectorAll('a[href*="delete"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены? Это действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
});