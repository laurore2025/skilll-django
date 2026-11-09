# Structure d'un projet Django maison

Remplacer `<depot>` par le nom du dépôt et `<projet>` par le nom court du projet Django
(ex. `csanit` pour Carte Sanitaire).

## Arborescence

```
<depot>/
├── .env                        # configuration réelle — ignorée par git
├── .env.example                # modèle sans secret — versionné
├── .gitignore
├── venv/                       # environnement Python unique — ignoré
├── <projet>/
│   ├── manage.py
│   ├── requirements.txt        # versions figées (pip freeze)
│   ├── <projet>/
│   │   ├── settings.py         # fichier unique, piloté par .env
│   │   ├── urls.py             # préfixes d'URL en français, admin sur une URL non standard
│   │   ├── wsgi.py             # module Gunicorn : <projet>.wsgi:application
│   │   └── asgi.py
│   ├── apps/
│   │   ├── __init__.py
│   │   └── <app>/
│   │       ├── apps.py         # name = "apps.<app>", verbose_name en français
│   │       ├── models.py
│   │       ├── admin.py
│   │       ├── forms.py
│   │       ├── urls.py         # app_name = "<app>"
│   │       ├── views.py        # vues fonctionnelles minces
│   │       ├── services.py     # logique métier (ou api.py, sync.py, courriel.py…)
│   │       ├── management/commands/<commande>.py
│   │       ├── migrations/
│   │       └── tests.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── <app>/<page>.html  # gabarits partiels préfixés « _ »
│   │   └── admin/<app>/<modèle>/change_form.html
│   ├── static/
│   │   ├── css/charte.css      # charte commune
│   │   ├── js/                 # scripts de l'application
│   │   ├── js/traductions/     # <page>.ht.js (créole haïtien)
│   │   ├── img/
│   │   └── legacy/             # thème de l'ancien site, conservé tel quel
│   ├── data/                   # données lues par le serveur (KML, référentiels)
│   ├── docs/                   # documentation technique versionnée
│   ├── http/                   # requêtes REST Client NN_sujet.http + README.md
│   ├── media/                  # fichiers générés — ignoré
│   └── staticfiles/            # cible de collectstatic — ignoré
├── scripts/                    # restauration, planification (PowerShell en ASCII)
└── base/                       # dumps SQL réels — ignoré, jamais versionné
```

Créer une application :

```powershell
cd <depot>\<projet>
mkdir apps\<app>
..\venv\Scripts\python.exe manage.py startapp <app> apps\<app>
# puis dans apps\<app>\apps.py : name = "apps.<app>" et verbose_name en français
# et dans settings.py : INSTALLED_APPS += ["apps.<app>"]
```

## `settings.py` (squelette)

```python
"""Settings du projet <projet> : un seul fichier, piloté par le fichier .env de la racine du dépôt."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent          # racine du dépôt : c'est là que vit le fichier .env
load_dotenv(REPO_DIR / ".env")      # n'écrase pas les variables déjà définies (Docker)


def _liste(nom, defaut=""):
    return [v.strip() for v in os.environ.get(nom, defaut).split(",") if v.strip()]


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-dev-key-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")
ALLOWED_HOSTS = _liste("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
CSRF_TRUSTED_ORIGINS = _liste("DJANGO_CSRF_TRUSTED_ORIGINS")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")   # derrière Nginx / tunnel TLS

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "<projet>.urls"
WSGI_APPLICATION = "<projet>.wsgi.application"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

# Base de données : PostgreSQL si DB_ENGINE=postgresql, sinon SQLite (attention : repli silencieux)
if os.environ.get("DB_ENGINE", "sqlite").lower() == "postgresql":
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "<projet>"),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

LANGUAGE_CODE = "fr"
TIME_ZONE = "America/Port-au-Prince"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
WHITENOISE_USE_FINDERS = True                      # collectstatic facultatif en développement
WHITENOISE_MAX_AGE = 0 if DEBUG else 3600
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DATA_DIR = BASE_DIR / "data"

X_FRAME_OPTIONS = "SAMEORIGIN"

# Journaux vers la console (indispensable avec DEBUG=False, en particulier dans Docker)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "{asctime} {levelname} {name} {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
    "loggers": {"django": {"handlers": ["console"], "level": "INFO", "propagate": False}},
}

# Courriel : console en développement, SMTP en production (ou configuration dans l'admin)
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "<projet>@localhost")
```

`urls.py` racine :

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("kon/", admin.site.urls),                     # admin sur une URL non standard
    path("", include("apps.core.urls")),
    path("cartographie/", include("apps.cartography.urls")),   # préfixes en français
]
```

## `.env.example`

```
# Modèle de configuration — copier vers .env et compléter (aucun secret ici)

# Django
DJANGO_SECRET_KEY=remplacer-par-une-cle-longue-et-aleatoire
DJANGO_DEBUG=True
# Hôtes acceptés, séparés par des virgules
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
# Origines HTTPS de confiance pour les formulaires derrière un proxy ou un tunnel
DJANGO_CSRF_TRUSTED_ORIGINS=

# Base de données — DB_ENGINE : postgresql ou sqlite (sqlite ignore les autres DB_*)
DB_ENGINE=postgresql
DB_NAME=<projet>
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=5432

# Courriel sortant : console par défaut, ou SMTP
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=<projet>@localhost
```

Pour les secrets destinés à Docker Compose, éviter `$`, `#`, guillemets et espaces ; générer avec
`python -c "import secrets; print(secrets.token_urlsafe(50))"`.

## `.gitignore`

```
# Python / Django
venv/
.venv/   # variante possible du nom du venv
__pycache__/
*.pyc
*.sqlite3
<projet>/staticfiles/
<projet>/media/
.env

# IDE / OS
.idea/
.vscode/
.DS_Store
Thumbs.db

# Données réelles et documents internes
base/
*.log
```
