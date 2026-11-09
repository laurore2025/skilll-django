---
name: systematic-debugging
description: Méthode de débogage en quatre phases avec analyse de la cause racine pour Django. À utiliser pour enquêter sur un bug, corriger des tests qui échouent ou comprendre un comportement inattendu. Insiste sur la règle AUCUN CORRECTIF AVANT D'AVOIR TROUVÉ LA CAUSE RACINE.
---

# Débogage systématique pour Django

## Principe fondamental

**AUCUN CORRECTIF AVANT D'AVOIR TROUVÉ LA CAUSE RACINE**

N'appliquez jamais de rustines qui masquent les problèmes sous-jacents. Comprenez POURQUOI quelque chose échoue avant de tenter de le corriger.

## Cadre en quatre phases

### Phase 1 : reproduire et enquêter

Avant de toucher au moindre code :

1. **Écrivez un test qui échoue** - il capture le comportement du bug
2. **Lisez attentivement les messages d'erreur** - chaque mot compte
3. **Examinez les modifications récentes** - `git diff`, `git log`
4. **Suivez le flux de données** - remontez la chaîne d'appels pour trouver d'où viennent les valeurs erronées

```python
# Écrivez d'abord un test qui échoue
@pytest.mark.django_db
def test_bug_reproduction():
    """Reproduit le ticket #123."""
    user = UserFactory()
    response = Client().post("/profile/", {"bio": "New"})
    assert response.status_code == 200  # Échoue actuellement
```

### Phase 2 : isoler

Circonscrivez le problème :

```python
# Ajoutez des logs à des endroits stratégiques
import logging
logger = logging.getLogger(__name__)

def problematic_view(request):
    logger.debug(f"Method: {request.method}")
    logger.debug(f"POST: {request.POST}")
    logger.debug(f"User: {request.user}")

    form = MyForm(request.POST)
    logger.debug(f"Valid: {form.is_valid()}")
    logger.debug(f"Errors: {form.errors}")
```

### Phase 3 : identifier la cause racine

- Lisez la pile d'appels (stack trace) en entier
- Utilisez le débogueur pour inspecter l'état
- Vérifiez quelles hypothèses ne sont pas respectées

### Phase 4 : corriger et vérifier

1. Appliquez le correctif au niveau de la cause racine
2. Lancez le test de reproduction (il doit passer)
3. Lancez la suite de tests complète
4. Vérifiez manuellement si nécessaire

## Outils de débogage Django

### Django Debug Toolbar

```python
# settings/dev.py
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]
```

Consultez le panneau SQL pour repérer les requêtes N+1 et les requêtes lentes (> 10 ms).

### Débogueur Python

```python
def problematic_view(request):
    breakpoint()  # L'exécution s'arrête ici

    # Commandes : n(ext), s(tep), c(ontinue), p var, q(uit)
```

```bash
# Ouvrir le débogueur lorsqu'un test échoue (projet sous pytest ; sinon manage.py test --pdb)
..\venv\Scripts\python.exe -m pytest --pdb -x
```

### Débogage des requêtes

```python
# Journaliser toutes les requêtes SQL
LOGGING = {
    "loggers": {
        "django.db.backends": {"level": "DEBUG", "handlers": ["console"]},
    },
}

# Compter les requêtes dans les tests
from django.test.utils import CaptureQueriesContext
from django.db import connection

def test_no_n_plus_one():
    with CaptureQueriesContext(connection) as ctx:
        list(Post.objects.select_related("author"))
    assert len(ctx) <= 2
```

## Problèmes Django courants

### Requêtes N+1

```python
# Problème
for post in Post.objects.all():
    print(post.author.email)  # Une requête par article !

# Correctif
for post in Post.objects.select_related("author"):
    print(post.author.email)  # Une seule requête
```

### Le formulaire n'enregistre rien

```python
# Vérifiez ces points :
# 1. form.is_valid() renvoie-t-il True ?
# 2. form.save() est-il appelé ?
# 3. Avec commit=False, avez-vous appelé .save() sur l'instance ?

def debug_form(request):
    form = MyForm(request.POST)
    print(f"Valid: {form.is_valid()}")
    print(f"Errors: {form.errors}")
```

### Erreurs 403 CSRF

```html
<!-- Vérifiez : csrf_token présent dans le formulaire -->
<form method="post">
    {% csrf_token %}
</form>
```

### Problèmes de migration

```bash
..\venv\Scripts\python.exe manage.py showmigrations
..\venv\Scripts\python.exe manage.py migrate --plan
# --fake seulement en local, après sauvegarde et accord explicite de l'utilisateur ;
# jamais sur une base partagée ou de production (les tables managed = False ne sont pas concernées)
..\venv\Scripts\python.exe manage.py migrate app_name 0001 --fake
```

## Déboguer Celery

```python
# Exécuter de façon synchrone pour déboguer
my_task(arg)  # Appel direct, pas .delay()

# Ou le définir dans les settings
CELERY_TASK_ALWAYS_EAGER = True
```

## Déboguer HTMX

```html
<script>htmx.logAll();</script>
```

```python
def view(request):
    print(f"HTMX: {request.headers.get('HX-Request')}")
```

## Liste de vérification

Avant d'affirmer que c'est corrigé :

- [ ] Cause racine identifiée
- [ ] Le test de reproduction passe
- [ ] `manage.py check` sans erreur
- [ ] Les requêtes REST Client (`.http`) concernées passent
- [ ] Les tests du projet passent (`manage.py test`, ou pytest si le projet l'utilise)

## Signaux d'alerte

Arrêtez-vous si vous pensez :
- « Correctif rapide maintenant, on enquêtera plus tard »
- « Encore une tentative » (après 3 échecs ou plus)
- « Ça devrait marcher » (sans comprendre pourquoi)

Trois correctifs consécutifs en échec = problème d'architecture. Arrêtez-vous et discutez-en.

## Intégration avec les autres skills

- **pytest-django-patterns** : écrivez des tests de reproduction
- **django-models** : déboguez les problèmes de QuerySet
- **celery-patterns** : déboguez les échecs de tâches asynchrones
- **htmx-alpine-patterns** : déboguez les requêtes HTMX
- **django-extensions** : utilisez `show_urls`, `list_model_info` et `shell_plus` pour l'introspection du projet
- **skill-creator** : créez des skills de débogage dédiés aux problèmes récurrents
