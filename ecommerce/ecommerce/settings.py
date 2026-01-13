import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- STATIC & STORAGE CONFIGURATION (Moved Up to Prevent AttributeError) ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Diagnostic prints for Railway logs
print(f"--- DIAGNOSTIC ---")
print(f"BASE_DIR: {BASE_DIR}")
print(f"STATIC_ROOT: {STATIC_ROOT}")
print(f"STATICFILES_STORAGE: {STATICFILES_STORAGE}")
print(f"--- END DIAGNOSTIC ---")
# --------------------------------------------------------------------------



INSTALLED_APPS = [
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'model_utils',  # For model tracking
    'shop.apps.ShopConfig',  # Use AppConfig for signal registration
    'accounts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

if not DATABASES['default']:
    # Fallback to local postgres settings if provided, otherwise use SQLite for portability
    db_name = os.environ.get('DB_NAME')
    if db_name:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': os.environ.get('DB_USER', 'postgres'),
                'PASSWORD': os.environ.get('DB_PASSWORD', 'Siva5107'),
                'HOST': os.environ.get('DB_HOST', 'localhost'),
                'PORT': os.environ.get('DB_PORT', '5432'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dtx4z5wik'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cart settings
CART_SESSION_ID = 'cart'

# Email settings
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
if DEBUG and not os.environ.get('EMAIL_BACKEND'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')  # Change in production

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

