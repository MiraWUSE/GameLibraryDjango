/**
 * AJAX-поиск игр по названию без перезагрузки
 */
function initAjaxSearch() {
    const searchForm = document.getElementById('header-search');
    const gamesContainer = document.getElementById('games-container');
    const loadingIndicator = document.getElementById('loading');

    if (!searchForm || !gamesContainer) return;

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

    // Debounce: ждём 300мс после последнего ввода
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

    // Отправка формы по нажатию Enter или клику на кнопку
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const params = new URLSearchParams(new FormData(searchForm)).toString();
        fetchFilteredGames(params);
    });
}

/**
 * Автозакрытие сообщений и инициализация
 */
document.addEventListener('DOMContentLoaded', function() {
    // Автозакрытие сообщений через 5 секунд
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Кнопка закрытия сообщений
    document.querySelectorAll('.alert__close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    // Инициализация поиска, если мы на странице списка
    if (document.getElementById('games-container')) {
        initAjaxSearch();
    }

    // Подтверждение удаления
    document.querySelectorAll('a[href*="delete"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены? Это действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
});