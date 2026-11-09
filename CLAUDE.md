# Projet Django

> Configuration Claude Code pour projets Django avec HTMX et un outillage Python moderne.

## L'essentiel

- **Pile** : Django, PostgreSQL, HTMX
- **Gestionnaire de paquets** : uv
- **Commande de test** : `uv run pytest`
- **Commande de lint** : `uv run ruff check .`
- **Commande de formatage** : `uv run ruff format .`
- **Vérification des types** : `uv run pyright`

## Répertoires clés

- `apps/` — applications Django
- `config/` — settings Django et URLconf racine
- `templates/` — gabarits Django/Jinja2
- `static/` — CSS, JavaScript, images
- `tests/` — fichiers de test
- `tasks/` — tâches Celery

## Style de code

- Python 3.12+ avec annotations de type obligatoires
- Ruff pour le lint et le formatage (remplace black, isort, flake8)
- Mode strict de pyright activé
- Pas de type `Any` : utilisez des annotations précises ou `object`
- Utilisez les retours anticipés, évitez les conditions imbriquées
- Préférez la composition à l'héritage

## Conventions Git

- **Nom des branches** : `{initiales}/{description}` (ex. `jd/fix-login`)
- **Format des commits** : Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **Titres de PR** : même format que les commits

## Règles essentielles

### Gestion des erreurs
- Ne JAMAIS avaler une erreur en silence
- Toujours informer l'utilisateur en cas d'erreur (messages Django, en-têtes de réponse HTMX)
- Journaliser les erreurs avec le contexte utile au débogage

### Vues
- Préférez les vues fonctionnelles (Function-Based Views)
- Validez toujours explicitement `request.method`
- Renvoyez les bons codes de statut HTTP
- Utilisez `select_related()` / `prefetch_related()` pour éviter les requêtes N+1

### Gabarits et HTMX
- Utilisez l'héritage de gabarits (`{% extends %}`, `{% block %}`)
- Créez des gabarits partiels pour les réponses HTMX (nommage `_partial.html`)
- Incluez toujours `hx-indicator` pour les états de chargement
- Tenez compte de l'en-tête `HX-Request` pour renvoyer un partiel ou la page complète

### Formulaires
- Utilisez ModelForm pour les formulaires liés à un modèle
- Validez dans les méthodes `clean()` et `clean_<champ>()`
- Gérez toujours les erreurs de formulaire dans les gabarits
- Désactivez les boutons de soumission pendant les requêtes HTMX

### Tâches Celery
- Les tâches doivent être idempotentes
- Utilisez des stratégies de nouvelle tentative avec temporisation exponentielle
- Journalisez toujours le début, la fin et l'échec d'une tâche
- Ne passez que des arguments sérialisables (pas d'instances de modèle)

## Tests

- Écrivez d'abord le test qui échoue (TDD)
- Utilisez Factory Boy : `UserFactory.create(is_admin=True)`
- Utilisez des fixtures pytest dans `conftest.py`
- Testez le comportement, pas l'implémentation
- Lancez les tests avant de commiter

## Activation des skills

Avant d'implémenter QUOI QUE CE SOIT, vérifiez si des skills s'appliquent :

- Débogage d'un problème → skill `systematic-debugging`
- Exploration d'un projet Django (modèles, URL, settings) → skill `django-extensions`
- Création de nouveaux skills → skill `skill-creator`
- Démarrage d'une nouvelle tâche → skill `onboard`
- Traitement d'un ticket → skill `ticket`
- Revue d'une PR → skill `pr-review`
- Résumé des changements d'une branche → skill `pr-summary`
- Contrôles de qualité → skill `code-quality`
- Vérification de l'exactitude de la documentation → skill `docs-sync`
- Commit des changements d'un worktree et fusion dans master/main → skill `worktree-commit-merge`

## Commandes courantes

```bash
# Développement
uv run python manage.py runserver     # Démarrer le serveur de développement
uv run pytest                         # Lancer les tests
uv run pytest -x --lf                 # Relancer les derniers échecs, arrêt au premier échec
uv run ruff check .                   # Lint du code
uv run ruff format .                  # Formatage du code
uv run pyright                        # Vérification des types

# Django
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py shell_plus    # Shell amélioré (django-extensions)
uv run python manage.py createsuperuser

# Celery
uv run celery -A config worker -l info
uv run celery -A config beat -l info

# Dépendances
uv sync                               # Installer depuis pyproject.toml
uv add <paquet>                       # Ajouter une dépendance
uv add --dev <paquet>                 # Ajouter une dépendance de développement

# Git
gh pr create                          # Créer une PR
```
