# Projet Django — <nom du projet>

> Configuration Claude Code des projets Django de Laurore. Les conventions détaillées sont dans le
> skill `conventions-django` : l'appliquer avant toute modification. Adapter les `<…>` à chaque projet.

## L'essentiel

- **Pile** : Django 5.2 LTS, Python 3.14, PostgreSQL 14+ avec PostGIS 3 (en SQL brut, sans GeoDjango),
  WhiteNoise ; interface en gabarits Django + JavaScript natif (`fetch`), Leaflet pour les cartes
- **Environnement** : un seul venv à la racine du dépôt ; `pip` + `<projet>/requirements.txt` aux versions figées
- **Projet Django** : sous-dossier `<projet>/` (contient `manage.py`) ; applications sous `<projet>/apps/`
- **Configuration** : `.env` à la racine du dépôt (jamais affiché ni commité), modèle `.env.example`
- **Langue** : français partout (code métier, interface, documentation, commits) ; créole haïtien pour l'interface
- **Vérifications** : `manage.py check`, requêtes REST Client `<projet>/http/*.http`
- **Branches** : travail sur `dev`, version stable sur `main` (fusion faite par l'utilisateur)

## Répertoires clés

- `<projet>/<projet>/` — `settings.py` unique piloté par `.env`, `urls.py`, `wsgi.py`
- `<projet>/apps/<app>/` — applications (`name = "apps.<app>"`), services à côté des vues
- `<projet>/templates/` — `base.html`, gabarits par application, surcharges `admin/`
- `<projet>/static/` — `css/charte.css`, `js/`, `js/traductions/*.ht.js`, `legacy/`
- `<projet>/data/` — données lues par le serveur (KML, référentiels)
- `<projet>/docs/` — documentation technique en français
- `<projet>/http/` — requêtes de test REST Client numérotées
- `scripts/` — scripts d'exploitation (PowerShell en ASCII)

## Règles essentielles

### Secrets et sécurité
- Ne JAMAIS afficher, lire ni recopier `.env` : pour un diagnostic, lister seulement les noms de variables
- Toute nouvelle variable : dans `settings.py` (défaut sûr) **et** dans `.env.example` (sans valeur)
- `DEBUG` faux par défaut ; CSRF actif ; SQL toujours paramétré ; limites anti-abus sur les formulaires publics

### Code
- Vues fonctionnelles minces ; logique dans `services.py`, `api.py`, `sync.py`… ; docstrings en français
- Formulaires `ModelForm` validés dans `clean_<champ>()` ; réponse JSON pour `fetch`, page complète sinon
- `log = logging.getLogger(__name__)` ; aucune erreur avalée sans être journalisée
- Toute bibliothèque importée figure dans `requirements.txt` (version figée)

### Base de données
- Tables héritées : `managed = False` (jamais recréées par une migration : elles viennent d'un dump)
- Tables PostGIS : `migrations.RunSQL` avec SQL inverse, SRID 4326, index GIST
- Sauvegarde avant tout `migrate` sur une base partagée ; relire `migrate --plan`

### Intégrations externes
- Le serveur appelle l'API (jamais le navigateur avec des identifiants), garde une copie locale en base
- Synchronisation par commande de gestion (`sync_<source>`, `--loop`), jamais dans une requête HTTP

### Gabarits
- Après modification d'un gabarit, redémarrer le serveur de vérification lancé avec `--noreload`
- Textes en français, clés `data-i18n` pour les traductions créoles

### Git
- Messages en français, format « Sujet : précisions, précisions »
- **Aucune trace de Claude** : pas de `Co-Authored-By`, pas de « Generated with Claude Code »
- **Pas de `git push` sans demande explicite** : préparer le commit et donner la commande
- Indexer les fichiers nommément ; ne jamais commiter `.env`, `venv/`, `base/`, `media/`, `db.sqlite3`

## Activation des skills

Avant d'implémenter QUOI QUE CE SOIT, vérifiez si des skills s'appliquent :

- Toute tâche dans ce projet → `conventions-django` (en premier ; il prime sur les autres skills)
- Modèles, migrations, requêtes → `django-models`
- Formulaires → `django-forms` ; gabarits → `django-templates`
- Débogage d'un problème → `systematic-debugging`
- Exploration du projet (modèles, URL, settings) → `django-extensions`
- Démarrage d'une nouvelle tâche → `onboard` ; ticket → `ticket`
- Revue d'une PR → `pr-review` ; résumé de branche → `pr-summary`
- Contrôles de qualité → `code-quality` ; exactitude de la documentation → `docs-sync`
- Création d'un skill → `skill-creator`
- Seulement si le projet les a adoptés : `pytest-django-patterns`, `htmx-patterns`, `celery-patterns`

## Commandes courantes

Depuis `<projet>/` (Windows ; sous Linux, remplacer `..\venv\Scripts\python.exe` par `../venv/bin/python`) :

```powershell
..\venv\Scripts\python.exe manage.py runserver                    # serveur de l'utilisateur (port 8000)
..\venv\Scripts\python.exe manage.py runserver 8010 --noreload    # vérifications de Claude
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
..\venv\Scripts\python.exe manage.py makemigrations <app>
..\venv\Scripts\python.exe manage.py migrate --plan
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py createsuperuser
..\venv\Scripts\python.exe manage.py test                         # si des tests Django existent
..\venv\Scripts\python.exe -m pip install -r requirements.txt
..\venv\Scripts\python.exe -m pip freeze                          # relever la version à figer
```

Déploiement Docker : voir `conventions-django` → `references/deploiement.md`.
