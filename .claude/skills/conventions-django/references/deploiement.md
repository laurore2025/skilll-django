# Déploiement Docker (Ubuntu)

Démarche suivie pour Carte Sanitaire (audit `AUDIT_DEPLOIEMENT_DOCKER_CARTE_SANITAIRE.md`).
Principe : **le projet reste indépendant des autres applications du serveur** (DHIS2, etc.).

## Avant de dockeriser : points à vérifier dans le code

- `gunicorn` et **toutes** les bibliothèques importées sont dans `requirements.txt`.
- `DB_HOST` ne vaut pas `127.0.0.1` dans un conteneur ; `DB_ENGINE=postgresql` est imposé.
- `LOGGING` vers la console est défini (sinon les erreurs 500 sont invisibles avec `DEBUG=False`).
- Les fichiers de `MEDIA_ROOT` sont servis autrement qu'avec `DEBUG=True` (vue `serve` limitée à un
  sous-dossier, puis Nginx).
- Aucune synchronisation longue ne se déclenche dans une requête HTTP.
- Tables héritées `managed = False` : prévoir la **restauration d'un dump**, aucune migration ne les crée.
- Version de PostgreSQL compatible avec la version de Django (Django 5.2 : PostgreSQL ≥ 14).

## Fichiers

- `<projet>/Dockerfile` : contexte de build = `<projet>/` (exclut d'office `.git`, `.env`, `base/`…).
- `<projet>/.dockerignore` : `__pycache__`, `.env`, `db.sqlite3`, `*.log`, `media/`, `staticfiles/`,
  `docs/`, `http/`.
- `compose.yaml` à la racine du dépôt ; `.env` du serveur à la racine, ignoré par git, `chmod 600`.

```dockerfile
FROM python:3.14-slim-trixie
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 DJANGO_SETTINGS_MODULE=<projet>.settings
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app
WORKDIR /app/<projet>
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p media staticfiles \
 && DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput \
 && chown -R app:app media
USER app
EXPOSE 8000
CMD ["gunicorn", "<projet>.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", \
     "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
```

Aucun `apt-get` n'est nécessaire tant que le projet n'utilise pas GeoDjango : `psycopg-binary`
embarque libpq et Pillow ses bibliothèques.

```yaml
name: <projet>

x-app: &app
  image: <projet>-web:${IMAGE_TAG:-latest}
  env_file: .env
  environment:
    DB_ENGINE: postgresql
    DB_HOST: db
    DB_PORT: "5432"
  restart: unless-stopped
  logging: {driver: json-file, options: {max-size: "10m", max-file: "5"}}
  depends_on: {db: {condition: service_healthy}}

services:
  db:
    image: postgis/postgis:16-3.5
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: ${PG_SUPERUSER_PASSWORD:?manquant}
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: {test: ["CMD-SHELL", "pg_isready -U postgres"], interval: 10s, retries: 10}
    # aucun port publié

  web:
    <<: *app
    build: {context: ./<projet>}
    ports: ["${BIND_IP:?manquant}:${PORT:-8070}:8000"]   # IP privée, jamais 0.0.0.0
    volumes: [media:/app/<projet>/media]
    healthcheck:
      test: ["CMD", "python", "-c", "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/', timeout=10).status == 200 else 1)"]
      interval: 30s
      timeout: 15s
      retries: 3
      start_period: 40s

  sync:
    <<: *app
    command: ["python", "manage.py", "sync_external", "--loop", "--interval", "300"]

volumes:
  pgdata:
  media:
```

`ALLOWED_HOSTS` doit contenir l'hôte d'accès **et** `127.0.0.1` (healthcheck interne).
Docker contourne UFW pour les ports publiés : toujours publier sur une IP précise.

## Premier déploiement (ordre)

1. Contrôles serveur en lecture seule : versions de Docker, ports occupés, réseaux, ressources ;
   tester qu'une image Debian récente tourne (`docker run --rm python:3.14-slim-trixie python -c "import threading; …"`).
2. `.env` du serveur (`DEBUG=False`, nouvelle clé, hôtes autorisés).
3. Base dédiée : rôle applicatif, base `OWNER` ce rôle, `CREATE EXTENSION postgis` par le superutilisateur.
4. Restauration du dump **avec le rôle applicatif** ; relire les erreurs ; compter les lignes.
5. `docker compose build web`.
6. Sauvegarde, puis `migrate --plan`, puis `migrate` (validé).
7. Commandes de données (import, reconstruction, première synchronisation), `createsuperuser`.
8. `docker compose up -d web sync`, puis vérifications (`ps`, journaux, requêtes `.http`).

## Mise à jour

```bash
git fetch origin dev && git log --oneline HEAD..origin/dev && git diff --stat HEAD origin/dev
git diff --name-only HEAD origin/dev -- '<projet>/apps/*/migrations/*'   # nouvelles migrations ?
git merge --ff-only origin/dev
docker compose build web
# si nouvelles migrations : pg_dump, migrate --plan, validation, migrate
docker compose up -d --no-deps web sync
```

Retour arrière : image précédente (étiquetée par commit) + `git reset --keep <commit>` ;
restauration de la sauvegarde seulement si des migrations ont été appliquées.

## À ne jamais faire sur un serveur partagé

`docker system prune`, `docker volume prune`, `docker compose down -v` (supprime la base),
redémarrage du démon Docker sans fenêtre de maintenance, `git clean -fdx` (supprime `.env`),
`migrate --fake`, `migrate <app> zero`, `makemigrations` sur le serveur.
