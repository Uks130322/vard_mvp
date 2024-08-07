"""
Django settings for vard project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = 'django-insecure-u(wb%zucp82-c%gx!4a^+akbs=-%g50dw^06t*9w%ayt9auxym'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [
#     '0.0.0.0',
#     '127.0.0.1',
#     '192.168.0.12',
#     '81.200.151.85',
#     '95.163.185.57',
#     'google.com',
#     'github.com',
#     'localhost',
#     'natalietkachuk.pythonanywhere.com',
# ]
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # users apps
    'appchat',
    'appuser',
    'appcomment',
    'appchart_DB',
    'appfeedback',
    'appfile',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_yasg",

    # for CORS
    'corsheaders',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

]


CLIENT_ID = 'SOCIALACCOUNT_PROVIDERS'
# GITHUB_SECRET_KEY = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
# GOOGLE_SECRET_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_SECRET')

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_GITHUB_KEY'),
            'secret': os.getenv('SOCIAL_AUTH_GITHUB_SECRET'),
            'key': ''
         }
    },
    'google': {
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_GOOGLE_KEY'),
            'secret': os.getenv('SOCIAL_AUTH_GOOGLE_SECRET'),
            'key': ''
        },

    }
}

# SOCIALACCOUNT_QUERY_EMAIL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # 'allauth.account.middleware.AccountMiddleware', # not for this django version
    'appchart_DB.middleware.Process500',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ROOT_URLCONF = 'vard.urls'
CSRF_COOKIE_SECURE = False

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # add for allauth
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'vard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'admin',
        # 'USER': 'postgres',
        'PASSWORD': 'prod',
        #'HOST': 'localhost',
        'HOST': 'db',
        'PORT': '5432',
    }
}
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },

# 'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'baza_test1',
#     'USER': 'root',
#     'PASSWORD': os.getenv("MYSQLPWD"),
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     'OPTIONS': {
#         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#     }
# }


AUTH_USER_MODEL = 'appuser.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

### статика #######################################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/usr/src/app/staticfiles'
SITE_URL = 'http://127.0.0.1:8000'
MEDIA_URL = ''  # TODO clarify details
MEDIA_ROOT = os.path.join('files')
### статика #######################################################################

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1


### allauth #######################################################################
LOGIN_URL = '/api/auth/login/'
LOGOUT_URL = '/api/auth/logout/'
LOGIN_REDIRECT_URL = '/api/auth/logout/'
LOGOUT_REDIRECT_URL = '/api/auth/login/'

#api/auth/logout/
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'name'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}
ACCOUNT_USERNAME_BLACKLIST = ["admin", "administrator", "moderator"]
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'

#### описание библиотеки
# #https://docs-allauth-org.translate.goog/en/latest/account/configuration.html?_x_tr_sl=en&_x_tr_tl=ru&_x_tr_hl=ru&_x_tr_pto=wapp
# ACCOUNT_AUTHENTICATION_METHOD = 'email' #'username'
# ACCOUNT_CHANGE_EMAIL = False
# #ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
# ACCOUNT_EMAIL_CONFIRMATION_HMAC = False #поставить True для отпавки ссылки на подтверждение
# ACCOUNT_EMAIL_NOTIFICATIONS = False #поставить True когда заработает почта
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'none' #'mandatory'
# ACCOUNT_EMAIL_SUBJECT_PREFIX = 'tbc-spb.ru'
# ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
# ACCOUNT_USERNAME_MIN_LENGTH = 4
# ACCOUNT_USERNAME_MAX_LENGTH = 30
# ACCOUNT_MAX_EMAIL_ADDRESSES = 1
#
# # ACCOUNT_FORMS = {
# #     'add_email': 'allauth.account.forms.AddEmailForm',
# #     'change_password': 'allauth.account.forms.ChangePasswordForm',
# #     'confirm_login_code': 'allauth.account.forms.ConfirmLoginCodeForm',
# #     'login': 'allauth.account.forms.LoginForm',
# #     'request_login_code': 'allauth.account.forms.RequestLoginCodeForm',
# #     'reset_password': 'allauth.account.forms.ResetPasswordForm',
# #     'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
# #     'set_password': 'allauth.account.forms.SetPasswordForm',
# #     'signup': 'allauth.account.forms.SignupForm',
# #     'user_token': 'allauth.account.forms.UserTokenForm',
# # }
# ACCOUNT_LOGIN_BY_CODE_ENABLED = False #True - пользователь вводит только адрес электронной почты.
# # Затем на этот адрес электронной почты отправляется одноразовый код,
# # который позволяет пользователю войти в систему
# #ACCOUNT_LOGIN_BY_CODE_TIMEOUT = 180 #Код, отправленный по электронной почте, имеет ограниченный срок действия.
# # Срок его действия истекает через столько секунд, после которых он был отправлен.
# ACCOUNT_SESSION_REMEMBER = None #Управляет временем существования сеанса.
# # Установите значение None, чтобы спрашивать пользователя («Помнишь меня?»), False не запоминать и Trueвсегда помнить.
# ACCOUNT_USERNAME_BLACKLIST = ["admin", "administrator", "moderator"] #Список имен пользователей, которые не могут быть использованы пользователем
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email' #по умолчанию: "email" Имя поля, содержащего email, если таковое имеется. См. пользовательские модели пользователей
# ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
# #ACCOUNT_USERNAME_MIN_LENGTH = 5
# ACCOUNT_USERNAME_REQUIRED = False

### allauth #######################################################################


### мыло #######################################################################
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'
MANAGERS = [("n1", "stds58@gmail.com")]
ADMINS = [("n2", "stds58@yandex.ru")]
SERVER_EMAIL = 'stds58@yandex.ru'
### мыло #######################################################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "rest_framework.authentication.TokenAuthentication",
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
