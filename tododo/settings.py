"""
Django settings for tododo project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'todolist',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",     #<-- django-allauth middleware
]

ROOT_URLCONF = 'tododo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tododo.context_processors.user_id',  
            ],
        },
    },
]

WSGI_APPLICATION = 'tododo.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom user model
AUTH_USER_MODEL = 'todolist.User'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CUSTOM BACKEND FOR THE --> email login  --> allauth
AUTHENTICATION_BACKENDS = [
      
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend',
    'todolist.auth_backends.EmailBackend',
]

DEFAULT_FROM_EMAIL = 'todolist.service.auth@gmail.com'
SITE_URL = 'http://127.0.0.1:8000/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Redirecting to /login/ from @login required decorator
LOGIN_URL = '/login_view/'

'''CSRF TOKEN'''
#change to True on https
CSRF_COOKIE_SECURE = False 
SESSION_COOKIE_SECURE = False

ALLOWED_REDIRECT_HOSTS = ['*'] # !!!----CHANGE AFTER DEVELOPMENT ----!!!
ALLOWED_HOSTS = ['*']


'''django-allauth'''
#Social account providers
#(the keys are in .env file, use os.getenv to take them out)
#(if you pulled this from github you have to create your own .env)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        
        'EMAIL_AUTHENTICATION': True,   #<-- this was the case about Unique Constraint

        'SCOPES': {
            "profile",
            "email"
        },
        'AUTH_PARAMS': {
            "acces_type": "online"
        },
    },
    'facebook': {
        'LOCALE_FUNC': lambda request: 'en_US'
    }
}


SOCIALACCOUNT_ADAPTER = 'todolist.adapters.CustomSocialAccountAdapter' # <-- READ ABOUT IF IT'S BETTER TO USE SIGNAL THEN THIS.

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT= True
SOCIALACCOUNT_LOGIN_ON_GET=True

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_FORM_CLASS = None


# FOR TESTING HTTPS <--- change after development
CSRF_TRUSTED_ORIGINS = [
    'https://todolist.loca.lt',
]

