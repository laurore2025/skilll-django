---
name: pytest-django-patterns
description: Patrons de test pytest-django, Factory Boy, fixtures et workflow TDD. À utiliser pour écrire des tests, créer des factories de test ou suivre le cycle TDD rouge-vert-refactorisation (red-green-refactor).
---

# Patrons de test pytest-django

## Workflow TDD (ROUGE-VERT-REFACTORISATION)

**Suivez toujours ce cycle :**

1. **ROUGE** : écrivez d'abord un test qui échoue et qui décrit le comportement souhaité
2. **VERT** : écrivez le code minimal pour faire passer le test
3. **REFACTORISER** : nettoyez le code tout en gardant les tests au vert
4. **RECOMMENCER** : n'écrivez jamais de code de production sans un test qui échoue

**Règle critique** : pour implémenter une fonctionnalité ou corriger un bug, écrivez le test AVANT de toucher au code de production.

## Patrons pytest-django essentiels

### Accès à la base de données

- Utilisez `@pytest.mark.django_db` sur tout test qui accède à la base de données
- Pour l'appliquer à tout un module : `pytestmark = pytest.mark.django_db`
- Les transactions sont annulées (rollback) automatiquement après chaque test

### Fixtures pour les données de test

**Utilisez Factory Boy pour les modèles et les fixtures pytest pour la mise en place :**

- **Factories** : créent des instances de modèle avec des données réalistes (`UserFactory()`)
  - Utilisez `factory.Sequence()` pour les champs uniques
  - Utilisez `factory.Faker()` pour des données factices réalistes
  - Utilisez `factory.SubFactory()` pour les clés étrangères
  - Utilisez `@factory.post_generation` pour les relations M2M

- **Fixtures** : mettent en place les clients, l'état d'authentification ou les ressources partagées
  - Fixture `client` : client de test Django
  - Créez une fixture `auth_client` : `client.force_login(user)` pour les requêtes authentifiées
  - Définissez-les dans `conftest.py` pour les réutiliser dans tous les fichiers de test

### Organisation des tests

**Structurez les tests à l'image de la structure des applications :**
```
tests/
├── apps/
│   └── posts/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_forms.py
├── factories.py
└── conftest.py
```

**Regroupez les tests liés dans des classes :**
- Nommez les classes `TestComponentName` (par ex. `TestPostListView`)
- Donnez aux méthodes de test des noms descriptifs : `test_<action>_<expected_outcome>`
- Utilisez `@pytest.mark.parametrize` pour tester plusieurs scénarios

## Que tester

### Vues
- **Codes de statut** : réponses HTTP correctes (200, 404, 302)
- **Authentification** : comportement en mode authentifié ou anonyme
- **Autorisation** : l'utilisateur n'accède qu'à ses propres données
- **Données de contexte** : les bons objets sont transmis au gabarit
- **Effets de bord** : modifications en base, e-mails envoyés, tâches mises en file d'attente
- **HTMX** : vérifiez que l'en-tête `HTTP_HX_REQUEST` renvoie le gabarit partiel

### Formulaires
- **Validation** : les données valides passent, les données invalides échouent avec les bonnes erreurs
- **Cas limites** : champs vides, longueurs maximales, contraintes d'unicité
- **Méthodes clean** : la logique de validation personnalisée fonctionne
- **Comportement à l'enregistrement** : les objets sont créés/mis à jour correctement

### Modèles
- **Méthodes** : `__str__` et les méthodes personnalisées renvoient les valeurs attendues
- **Managers/QuerySets** : le filtrage personnalisé fonctionne correctement
- **Contraintes** : la validation au niveau de la base de données est appliquée
- **Signaux** : les hooks pre/post save s'exécutent correctement

### Tâches Celery
- **Simulez (mock) les appels externes** : patchez les requêtes HTTP, l'envoi d'e-mails, etc.
- **Testez uniquement la logique** : ne testez pas l'exécution asynchrone réelle
- **Idempotence** : exécuter la tâche plusieurs fois est sans risque

## Patrons de test propres à Django

### Tester les réponses HTMX

Vérifiez que le gabarit partiel est rendu quand l'en-tête `HX-Request` est présent :
- Passez `HTTP_HX_REQUEST="true"` à la requête du client
- Vérifiez par une assertion que `response.templates` contient le nom du gabarit partiel

### Tester les permissions

Créez des fixtures de client authentifié et de client anonyme :
- Testez la redirection/le 403 en cas d'accès non autorisé
- Testez la réussite en cas d'accès autorisé

### Tester les QuerySets

Vérifiez que les requêtes sont efficaces :
- Créez les données de test avec des factories
- Exécutez la requête
- Vérifiez par une assertion que les bons objets sont renvoyés/exclus
- Vérifiez que les objets liés sont chargés avec `select_related()`/`prefetch_related()`

### Tester les formulaires avec des instances de modèle

Passez l'instance au formulaire pour les mises à jour :
- `form = MyForm(data=new_data, instance=existing_obj)`
- Vérifiez que `form.save()` met à jour l'objet et n'en crée pas un nouveau

## Patrons courants

**Paramétrez plusieurs scénarios :**
Utilisez `@pytest.mark.parametrize("input,expected", [...])` pour tester diverses entrées

**Simulez (mock) les services externes :**
Utilisez `mocker.patch()` pour éviter les vrais appels HTTP, envois d'e-mails et opérations sur les fichiers

**Vérifiez les modifications en base :**
- Vérifiez `Model.objects.filter(...).exists()` après une création
- Vérifiez `Model.objects.count() == expected` pour les suppressions
- Utilisez `refresh_from_db()` pour vérifier les mises à jour

**Testez la gestion des erreurs :**
- Des données de formulaire invalides produisent les bonnes erreurs
- Les opérations en échec renvoient des réponses d'erreur
- L'utilisateur voit des messages d'erreur appropriés

## Lancer les tests

```bash
uv run pytest                    # Tous les tests
uv run pytest -x                 # S'arrêter au premier échec
uv run pytest --lf               # Relancer les derniers tests en échec
uv run pytest -x --lf            # Derniers échecs uniquement, arrêt au premier
uv run pytest -k "test_name"     # Tests correspondant au motif
uv run pytest tests/apps/posts/  # Répertoire précis
uv run pytest --cov=apps         # Avec rapport de couverture
```

## Pièges courants

- **Oublier `@pytest.mark.django_db`** : provoque des erreurs « Database access not allowed »
- **Ne pas utiliser de factories** : créer les instances à la main est verbeux et fragile
- **Tester l'implémentation** : testez le comportement et les résultats, pas les détails internes d'implémentation
- **Sauter le TDD** : écrire les tests après le code revient à calquer les tests sur l'implémentation et à manquer des cas limites
- **Abuser des mocks** : simulez les dépendances externes, pas votre propre code
- **Tester le code du framework** : ne testez pas l'ORM de Django, la validation des formulaires, etc. Testez VOTRE logique

## Configuration requise

**Dans `pyproject.toml` :**
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = ["--reuse-db", "-ra"]
```

**Dans `conftest.py` :**
Définissez les fixtures partagées (auth_client, factories communes, etc.)

## Intégration avec les autres skills

- **systematic-debugging** : pour corriger un bug, écrivez d'abord un test qui échoue afin de le reproduire
- **django-models** : testez les managers personnalisés, les QuerySets et les méthodes de modèle
- **django-forms** : testez la validation des formulaires, les méthodes clean et le comportement à l'enregistrement
- **celery-patterns** : testez la logique des tâches avec des dépendances externes simulées (mocks)
