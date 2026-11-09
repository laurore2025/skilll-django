---
name: code-quality
description: "Exécute les contrôles de qualité du code (ruff lint, ruff format, pyright, pytest) sur un répertoire et présente les constats par gravité. À utiliser lorsque l'utilisateur veut auditer la qualité du code, rechercher des erreurs de type ou des problèmes de lint, ou lancer des contrôles automatisés sur un chemin. Accepte un chemin de répertoire en argument. Se déclenche sur des demandes comme « vérifie la qualité du code », « lance les contrôles qualité », « /code-quality apps/ »."
---

# Revue de la qualité du code

Examinez la qualité du code dans le répertoire fourni par l'utilisateur.

## Instructions

1. **Identifiez les fichiers à examiner** :
   - Trouvez tous les fichiers `.py` du répertoire
   - Excluez les migrations, `__pycache__` et les fichiers générés

2. **Exécutez les contrôles automatisés** :
   ```bash
   uv run ruff check <directory>
   uv run ruff format --check <directory>
   uv run pyright <directory>
   uv run pytest <directory> -v
   ```

3. **Liste de vérification manuelle** :
   - [ ] Pas de types `Any` sans justification
   - [ ] Gestion correcte des erreurs (pas d'exceptions silencieuses)
   - [ ] Requêtes N+1 évitées (select_related/prefetch_related)
   - [ ] Les formulaires ont une validation appropriée
   - [ ] Les vues renvoient les bons codes de statut HTTP
   - [ ] Les gabarits partiels HTMX gèrent l'en-tête HX-Request
   - [ ] Les tâches Celery sont idempotentes
   - [ ] Les tests utilisent des factories, pas la création brute d'objets

4. **Présentez les constats** classés par gravité :
   - Critique (à corriger impérativement)
   - Avertissement (à corriger de préférence)
   - Suggestion (amélioration possible)
