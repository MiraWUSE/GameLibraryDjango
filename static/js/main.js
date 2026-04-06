/**
 * AJAX-фильтрация игр без перезагрузки страницы
 */
function initAjaxFilter() {
    const filterForm = document.getElementById('filter-form');
    const gamesContainer = document.getElementById('games-container');
    const loadingIndicator = document.getElementById('loading');
    const resetButton = document.getElementById('reset-filters');

    if (!filterForm || !gamesContainer) return;

    // Функция отправки запроса
    function fetchFilteredGames(params) {
        // Показываем индикатор загрузки
        loadingIndicator.classList.remove('hidden');
        
        // Отправляем AJAX-запрос
        fetch(`/ajax/filter-games/?${params}`)
            .then(response => response.json())
            .then(data => {
                // Обновляем список игр
                gamesContainer.innerHTML = data.html;
                
                // Обновляем счётчик (если нужно)
                const countElement = document.querySelector('.text-muted');
                if (countElement && data.count !== undefined) {
                    countElement.textContent = `Найдено: ${data.count}`;
                }
            })
            .catch(error => {
                console.error('Ошибка фильтрации:', error);
                gamesContainer.innerHTML = '<p class="no-results">Ошибка загрузки данных 😔</p>';
            })
            .finally(() => {
                // Скрываем индикатор
                loadingIndicator.classList.add('hidden');
            });
    }

    // Обработчик изменений в форме (с задержкой для поиска)
    let searchTimeout;
    filterForm.addEventListener('input', (e) => {
        if (e.target.name === 'search') {
            // Debounce для поиска: ждём 300мс после последнего ввода
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const params = new URLSearchParams(new FormData(filterForm)).toString();
                fetchFilteredGames(params);
            }, 300);
        }
    });

    // Мгновенная фильтрация для select и number
    filterForm.addEventListener('change', (e) => {
        if (e.target.name !== 'search') {
            const params = new URLSearchParams(new FormData(filterForm)).toString();
            fetchFilteredGames(params);
        }
    });

    // Сброс фильтров
    if (resetButton) {
        resetButton.addEventListener('click', () => {
            filterForm.reset();
            // Перезагружаем страницу для полного сброса
            window.location.href = filterForm.action;
        });
    }

    // Поддержка навигации с клавиатуры
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && loadingIndicator.classList.contains('hidden')) {
            const searchInput = filterForm.querySelector('[name="search"]');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.blur();
            }
        }
    });
}

/**
 * Закрытие сообщений об успехе по клику
 */
document.addEventListener('DOMContentLoaded', function() {
    // Автозакрытие сообщений через 5 секунд
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Инициализация фильтрации, если мы на странице списка
    if (document.getElementById('games-container')) {
        initAjaxFilter();
    }

    // Подтверждение удаления (дополнительная защита)
    document.querySelectorAll('a[href*="delete"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены? Это действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
});