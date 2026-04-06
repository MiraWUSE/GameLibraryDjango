from pathlib import Path

# === БАЗОВЫЕ ПУТИ ===
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'django-insecure-change-this-in-production-!!!'

# === УСТАНОВЛЕННЫЕ ПРИЛОЖЕНИЯ ===
INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Наши приложения
    'core',  # ← Приложение с играми и 3D-персонажами
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URL-КОНФИГУРАЦИЯ ===
ROOT_URLCONF = 'config.urls'

# === ШАБЛОНЫ ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Папка для глобальных шаблонов
        'APP_DIRS': True,  # ← Искать шаблоны внутри приложений (core/templates/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# === WSGI/ASGI ===
WSGI_APPLICATION = 'config.wsgi.application'
# ASGI_APPLICATION = 'config.asgi.application'  # Раскомментируй, если будешь использовать WebSockets

# === БАЗА ДАННЫХ ===
# По умолчанию SQLite для разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'  

TIME_ZONE = 'Europe/Moscow' 

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert--info',
    messages.INFO: 'alert--info',
    messages.SUCCESS: 'alert--success',
    messages.WARNING: 'alert--warning',
    messages.ERROR: 'alert--error',
}

PAGINATE_BY = 9

