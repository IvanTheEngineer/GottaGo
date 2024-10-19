import os
import secrets
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4e%b606a&s9#z97jc8vv@2n4z1f2jyb3__okmp-q1!1d-2!=6i'

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", "0.0.0.0", "travel-planner-cs3240-b-25-7745206e8d01.herokuapp.com"]


SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True

LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_OAUTH_ID'),
            'secret': os.environ.get('GOOGLE_OAUTH_SECRET'),
            'key': ''  # Leave blank
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
        }
    }
}


# AWS Stuff
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# Prevents file overwrites even if you upload the same file
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

if IS_HEROKU_APP:
    # In production on Heroku the database configuration is derived from the DATABASE_URL
    # environment variable by the dj-database-url package. DATABASE_URL will be set
    # automatically by Heroku when a database addon is attached to your Heroku app. See:
    # https://devcenter.heroku.com/articles/provisioning-heroku-postgres
    # https://github.com/jazzband/dj-database-url
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    # When running locally in development or in CI, a sqlite database file will be used instead
    # to simplify initial setup. Longer term it's recommended to use Postgres locally too.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }