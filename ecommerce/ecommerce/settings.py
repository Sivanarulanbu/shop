## 1. settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'model_utils',  # For model tracking
    'shop.apps.ShopConfig',  # Use AppConfig for signal registration
    'accounts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'shop.context_processors.cart',

            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop01',
        'USER':'postgres',
        'PASSWORD':'Siva5107',
        'HOST':'localhost',
        'PORT':'5432',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cart settings
CART_SESSION_ID = 'cart'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'krishnananbu99@gmail.com'
EMAIL_HOST_PASSWORD = 'osyo xyua uvfq ggow'  # Your app password
DEFAULT_FROM_EMAIL = 'Swiftbuy <krishnananbu99@gmail.com>'
EMAIL_TIMEOUT = 30  # Increased timeout
EMAIL_USE_SSL = False

# Additional email settings
EMAIL_USE_LOCALTIME = True
EMAIL_SUBJECT_PREFIX = '[Swiftbuy] '  # Prefix for email subjects
ADMIN_EMAIL = 'krishnananbu99@gmail.com'  # Email for admin notifications

# Email notification settings
EMAIL_NOTIFICATIONS = {
    'ORDER_STATUS_CHANGE': True,  # Send emails when order status changes
    'LOW_STOCK_ALERT': True,      # Send emails when product stock is low
    'NEW_ORDER': True,            # Send emails when new orders are placed
    'ORDER_CONFIRMATION': True,   # Send order confirmation emails
    'FAILED_PAYMENT': True,       # Send emails when payments fail
}

# Low stock threshold for notifications
LOW_STOCK_THRESHOLD = 5  # Send alert when stock falls below this number

# Site URL for email links
SITE_URL = 'http://localhost:8000'  # Change in production

# Store name and contact info for emails
STORE_NAME = 'Swiftbuy'
STORE_ADDRESS = 'Your Store Address'
STORE_PHONE = 'Your Store Phone'
STORE_SUPPORT_EMAIL = 'krishnananbu99@gmail.com'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'debug.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'shop': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

