---
name: conventions-django
description: "Style de développement et structure des projets Django de Laurore : dépôt avec venv et .env à la racine, projet Django dans un sous-dossier, applications dans son dossier apps, settings unique piloté par .env, PostgreSQL/PostGIS en SQL brut (sans GeoDjango), tables héritées en managed=False, code, interface et documentation en français, vues fonctionnelles, intégrations externes avec copie locale synchronisée, tests REST Client (.http), commits en français sans attribution Claude, déploiement Docker. À appliquer AVANT toute création ou modification dans un projet Django : nouvelle app, modèle, vue, formulaire, gabarit, migration, commande de gestion, settings, intégration d'API, déploiement, commit ou documentation."
---

# Conventions Django (style maison)

Ces conventions décrivent la façon de travailler de Laurore sur ses projets Django
(projet de référence : Carte Sanitaire, migration d'un site PHP vers Django 5.2).
**En cas de conflit avec un autre skill de ce dépôt** (uv, pytest, HTMX, Celery, Conventional
Commits…), **ces conventions priment**. Les autres skills restent utiles pour leurs techniques.

Références détaillées :
- [references/structure-projet.md](references/structure-projet.md) : arborescence, `settings.py`, `.env.example`, `.gitignore`
- [references/modeles-de-code.md](references/modeles-de-code.md) : modèles de code prêts à adapter
- [references/deploiement.md](references/deploiement.md) : déploiement Docker sur Ubuntu

## 1. Principes

1. **Français partout** : réponses, code métier (modèles, champs, fonctions, constantes), `verbose_name`,
   messages d'interface et d'erreur, docstrings, commentaires, documentation, messages de commit.
   Les noms d'applications restent courts (`core`, `reports`… ; l'anglais y est accepté).
2. **Aucun secret dans le dépôt** : `.env` (ignoré) et `.env.example` (versionné, sans valeur).
   Ne jamais afficher, citer ni recopier le contenu de `.env` ; pour le diagnostiquer, n'en lister que
   les noms de variables et si elles sont renseignées.
3. **Défauts sûrs** : `DEBUG` faux par défaut, `ALLOWED_HOSTS` restreint, CSRF actif, limites anti-abus,
   requêtes SQL paramétrées.
4. **Signaler les bonnes pratiques** : l'utilisateur souhaite être prévenu quand une meilleure pratique
   s'applique ; la proposer, l'expliquer en une phrase, sans l'imposer.
5. **Compatibilité d'abord** : vérifier la matrice Python / Django / PostgreSQL / PostGIS avant toute
   montée de version (Django 5.2 LTS tant que PostgreSQL < 15 ; Django 5.2 exige PostgreSQL ≥ 14).
6. **Ne pas inventer** : ce qui ne peut pas être vérifié dans le projet est signalé comme tel.

## 2. Structure du dépôt

```
<depot>/                      racine git
├── .env                      configuration réelle (ignorée) — lue par settings.py
├── .env.example              modèle sans secret (versionné)
├── venv/                     environnement Python unique (ignoré)
├── <projet>/                 projet Django (ex. csanit/)
│   ├── manage.py
│   ├── requirements.txt      versions figées
│   ├── <projet>/             settings.py, urls.py, wsgi.py, asgi.py
│   ├── apps/<app>/           une application par domaine
│   ├── templates/            base.html, <app>/…, admin/<app>/<modèle>/…
│   ├── static/               css/, js/, js/traductions/, img/, legacy/
│   ├── data/                 données lues par le serveur (KML, référentiels)
│   ├── docs/                 documentation technique en français (versionnée)
│   └── http/                 requêtes REST Client NN_sujet.http + README.md
├── scripts/                  scripts d'exploitation (PowerShell en ASCII, shell)
└── base/                     dumps SQL réels (ignorés, jamais versionnés)
```

Détails et fichiers modèles : [references/structure-projet.md](references/structure-projet.md).

## 3. Environnement de développement

- Poste Windows (XAMPP `htdocs`), PowerShell et Git Bash, VS Code.
- Un seul venv à la racine. Les commandes Django se lancent **depuis `<projet>/`** :
  `..\venv\Scripts\python.exe manage.py <commande>` (Windows) ou `../venv/bin/python manage.py …` (Linux).
- Serveur de l'utilisateur : `runserver` sur le port 8000 (rechargement automatique).
  Serveur de vérification de Claude : port **8010 avec `--noreload`** ; ce mode garde les gabarits en
  cache : **redémarrer le serveur après toute modification de gabarit** avant de revérifier.
- PostgreSQL local (14) avec PostGIS 3.x ; bases locales aux noms distincts de la production.
- Scripts PowerShell (`scripts/*.ps1`) **en ASCII uniquement** : PowerShell 5.1 abîme les accents.

## 4. Dépendances

- `pip` + `<projet>/requirements.txt` aux **versions figées** (`pip freeze`) ; pas d'uv ni de poetry
  par défaut.
- Toute bibliothèque importée par le code figure **explicitement** dans `requirements.txt`, même si
  elle est déjà installée comme dépendance d'un autre paquet (sinon : `ImportError` en production).
- Pour HTTP côté serveur, `urllib.request` (bibliothèque standard) suffit souvent ; ajouter `requests`
  seulement si besoin, et alors le déclarer.
- Pas de GeoDjango (GDAL/GEOS indisponibles sur le poste Windows) : PostGIS est exploité en SQL.

## 5. Configuration (`settings.py` unique)

- Un seul fichier, piloté par variables d'environnement : `load_dotenv(REPO_DIR / ".env")`
  (`REPO_DIR = BASE_DIR.parent`). Pas de `settings/dev.py` / `prod.py`.
- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` (faux par défaut), `DJANGO_ALLOWED_HOSTS`,
  `DJANGO_CSRF_TRUSTED_ORIGINS` : listes séparées par des virgules.
- Base : `DB_ENGINE=postgresql|sqlite` + `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` ;
  `CONN_MAX_AGE=60`, `CONN_HEALTH_CHECKS=True`. Attention : sans `DB_ENGINE=postgresql`, repli SQLite.
- `LANGUAGE_CODE = "fr"`, `TIME_ZONE = "America/Port-au-Prince"`, `USE_TZ = True`.
- Statiques : WhiteNoise (`WHITENOISE_USE_FINDERS = True`), `GZipMiddleware` pour les grosses réponses JSON.
- Admin sur une URL non standard (ex. `kon/`), `X_FRAME_OPTIONS = "SAMEORIGIN"` si la page s'ouvre
  elle-même en iframe.
- Journalisation : définir `LOGGING` vers la console (sinon, avec `DEBUG=False`, les traces d'erreurs 500
  ne sont écrites nulle part).
- Chaque nouvelle variable est ajoutée **à la fois** dans `settings.py` (avec un défaut sûr) et dans
  `.env.example` (sans valeur, avec un commentaire en français).

## 6. Applications

- Emplacement `<projet>/apps/<app>/` ; `apps.py` : `name = "apps.<app>"`, `verbose_name` en français.
- `urls.py` avec `app_name = "<app>"` ; préfixes d'URL en français dans l'URLconf racine
  (`cartographie/`, `etablissements/`, `donnees-tabulaires/`).
- Vue mince, logique dans des modules dédiés à côté des vues : `services.py`, `api.py`, `sync.py`,
  `spatial.py`, `courriel.py`, `recherche.py`… (noms explicites en français quand c'est du métier).
- Commandes de gestion dans `apps/<app>/management/commands/` pour tout traitement lancé hors requête
  (import, reconstruction, synchronisation, audit).

## 7. Modèles et base de données

- Champs et modèles nommés en français pour le métier (`MessageContact`, `ConfigurationCourriel`,
  `recu_le`, `envoye_le`), `verbose_name` / `verbose_name_plural` en français, `ordering` explicite.
- **Tables héritées** : `managed = False` + `db_table` ; Django les lit sans les créer ni les modifier.
  Ne jamais supposer qu'une migration les recrée : elles proviennent d'une restauration de dump.
- **Configuration éditable dans l'admin** : modèle à enregistrement unique avec une méthode de classe
  `charger()` ; l'admin interdit ajout et suppression et redirige la liste vers le formulaire.
- **État des traitements** conservé en base : dernière tentative, dernière réussite, dernière erreur,
  nombre d'éléments ; un échec conserve les données précédentes.
- **PostGIS sans GeoDjango** : moteur `django.db.backends.postgresql` ; tables spatiales créées par
  `migrations.RunSQL(CREATE, DROP)` (avec SQL inverse), `CREATE EXTENSION IF NOT EXISTS postgis`,
  SRID 4326, index GIST ; colonne `geom` absente du modèle (`managed = False`) ; requêtes spatiales en SQL
  via `connection.cursor()` ; KML importé avec `ST_GeomFromKML` (pas de GDAL).
- SQL **toujours paramétré** (`%s`) ; un nom de colonne dynamique passe par une **liste blanche**.
- Une migration de données (`RunPython`) est idempotente (`get_or_create` / `update_or_create`) et a
  une fonction inverse.

## 8. Vues, formulaires et API

- Vues fonctionnelles ; méthode imposée par décorateur (`@require_POST`, `@require_GET`) ;
  fonctions d'aide privées préfixées `_` ; docstring d'une ligne en français.
- **Amélioration progressive** : un formulaire fonctionne sans JavaScript (redirection + message) et
  avec `fetch` (en-tête `X-Requested-With: fetch` → `JsonResponse`).
- Codes HTTP justes : 400 (invalide), 403 (CSRF), 404, 429 (limite atteinte).
- Formulaires publics : `ModelForm`, validation dans `clean_<champ>()` avec messages en français,
  **pot de miel** (champ caché qui doit rester vide), **limite par IP** via le cache
  (constante `<SUJET>_MAX_PAR_HEURE`).
- Compatibilité avec un ancien système : conserver le format de réponse attendu par le JavaScript
  historique (même type MIME, mêmes clés) et le documenter.

## 9. Intégrations externes

- Le navigateur n'appelle **jamais** une API tierce avec des identifiants : le serveur appelle, met en
  cache et tient une **copie locale** en base ; l'affichage lit la copie.
- Synchronisation par commande `sync_<source>` et une commande d'ensemble `sync_external`
  (`--loop --interval <s>`), planifiée : tâche planifiée Windows en développement, service Docker
  (ou cron) en production.
- **Pas de synchronisation longue dans une requête HTTP** ; délai (`timeout`) explicite sur chaque appel ;
  erreurs journalisées **et** conservées dans l'état de synchronisation.
- Celery seulement si une vraie file de tâches est nécessaire ; sinon, commande de gestion.

## 10. Gabarits, statiques, traductions

- `templates/base.html` ; gabarits par app dans `templates/<app>/` ; gabarits partiels préfixés `_`
  (`_entete.html`) ; surcharges d'admin dans `templates/admin/<app>/<modèle>/`.
- Charte commune dans `static/css/charte.css`, scripts dans `static/js/`, anciens thèmes conservés dans
  `static/legacy/` (référence visuelle, non modifiés).
- Interface en français ; créole haïtien (`ht`) par fichiers `static/js/traductions/<page>.ht.js` et
  attributs `data-i18n`.
- Bibliothèques front par CDN avec `integrity` (SRI) quand c'est possible (ex. Leaflet).
- Ne pas laisser de mesure d'audience active hors production sans le signaler.

## 11. Admin Django

- Libellés, `fieldsets` et descriptions en français ; badges par `format_html` ; actions et vues
  supplémentaires par `get_urls()` ; messages `messages.success/error` explicites.
- Tables héritées : admin en lecture seule (classe de base `ReadOnlyAdmin`).

## 12. Erreurs et journalisation

- `log = logging.getLogger(__name__)` dans chaque module ; aucune exception avalée sans être journalisée.
- Quand l'utilisateur doit savoir : conserver l'erreur avec la donnée (statut d'envoi, dernière erreur)
  et l'afficher dans l'admin.

## 13. Tests et vérifications

- **Requêtes REST Client** : `<projet>/http/NN_sujet.http` numérotés, `@host` en tête, résultat attendu
  en commentaire `# Attendu : …` au-dessus de chaque requête, tableau récapitulatif dans `http/README.md`.
  Une fonctionnalité nouvelle = un fichier ou une section `.http`.
- Avant de rendre la main : `manage.py check`, `manage.py makemigrations --check --dry-run`,
  requêtes `.http` concernées, vérification visuelle si un gabarit a changé (serveur redémarré).
- Tests Django (`TestCase`, `manage.py test`) bienvenus pour la logique métier ; pytest seulement si le
  projet l'a adopté (voir le skill `pytest-django-patterns`).

## 14. Documentation

- `<projet>/docs/*.md` en français et versionnés : choix techniques, journaux de conversion, tables de
  correspondance, points restant à traiter. Guides internes non versionnés (ajoutés au `.gitignore`).
- Références de code au format `chemin:ligne`.
- Rapports et audits : Markdown en français, sans aucune donnée sensible.

## 15. Git

- Branches : `dev` pour le travail, `main` pour la version stable ; l'utilisateur fusionne lui-même.
- Message en français, au format **« Sujet : précisions, précisions »** ;
  ex. `Nouvelle carte : charte commune, créole, formulaire de contact, satellite hybride`,
  `Étape 3 : modèles en lecture seule, PostGIS (contours, points, audit)`.
- **Aucune trace de Claude** dans l'historique : pas de `Co-Authored-By`, pas de « Generated with
  Claude Code », ni dans les commits ni dans les PR.
- **Ne pas pousser sans demande explicite** : préparer le commit et donner la commande `git push`.
- Indexer les fichiers nommément (pas de `git add -A`) ; ne jamais commiter `.env`, `venv/`, `base/`,
  `media/`, `db.sqlite3`, journaux, `__pycache__/`.

## 16. Déploiement

Docker sur Ubuntu : image `python:<version>-slim`, Gunicorn (workers sync), WhiteNoise, Compose
(`web` + `sync` + base PostGIS dédiée sans port publié), port publié sur une IP privée, aucune
migration automatique au démarrage, sauvegarde `pg_dump` avant tout `migrate`.
Procédure complète : [references/deploiement.md](references/deploiement.md).

## Checklist avant de rendre la main

- [ ] Code, messages et docstrings en français ; aucun secret ni contenu de `.env` affiché.
- [ ] Nouvelle variable : `settings.py` (défaut sûr) **et** `.env.example`.
- [ ] Nouvelle dépendance importée : ajoutée et figée dans `requirements.txt`.
- [ ] Migrations générées et relues (`RunSQL` avec SQL inverse, `RunPython` idempotent).
- [ ] `manage.py check` sans erreur ; requêtes `.http` à jour et passées.
- [ ] Gabarit modifié : serveur de vérification redémarré, rendu contrôlé.
- [ ] Documentation `docs/` mise à jour si un choix technique a changé.
- [ ] Commit en français, sans attribution Claude ; pas de push sans demande.
