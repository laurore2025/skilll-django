---
name: code-quality
description: "Exécute les contrôles de qualité d'un projet Django maison (manage.py check, migrations manquantes, syntaxe Python, check --deploy, requêtes REST Client .http, ruff s'il est installé) sur un répertoire et présente les constats par gravité. À utiliser lorsque l'utilisateur veut auditer la qualité du code, rechercher des erreurs ou lancer des contrôles automatisés sur un chemin. Accepte un chemin de répertoire en argument. Se déclenche sur des demandes comme « vérifie la qualité du code », « lance les contrôles qualité », « /code-quality apps/ »."
---

# Revue de la qualité du code

Examinez la qualité du code dans le répertoire fourni par l'utilisateur, selon le skill `conventions-django`.

## Instructions

1. **Identifiez les fichiers à examiner** :
   - Trouvez les fichiers `.py`, `.html` et `.js` du répertoire
   - Excluez `__pycache__`, `static/legacy/`, `staticfiles/`, `media/` et les fichiers générés
   - Relisez les migrations seulement pour leur sûreté (`RunSQL` avec SQL inverse, `RunPython` idempotent)

2. **Exécutez les contrôles automatisés** depuis `<projet>/` (sous Linux : `../venv/bin/python`) :
   ```bash
   ..\venv\Scripts\python.exe manage.py check
   ..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
   ..\venv\Scripts\python.exe -m compileall -q <répertoire>
   ..\venv\Scripts\python.exe manage.py check --deploy      # avant un déploiement
   ..\venv\Scripts\python.exe manage.py test <app>          # si le projet a des tests
   ..\venv\Scripts\python.exe -m ruff check <répertoire>    # seulement si ruff est installé dans le venv
   ```
   Passez ensuite les requêtes REST Client concernées (`<projet>/http/*.http`, résultat attendu en
   commentaire `# Attendu : …`), serveur de développement lancé.

3. **Liste de vérification manuelle** :
   - [ ] Code métier, messages, docstrings et commentaires en français
   - [ ] Aucun secret dans le code ; toute variable nouvelle présente dans `settings.py` **et** `.env.example`
   - [ ] Toute bibliothèque importée déclarée et figée dans `requirements.txt`
   - [ ] SQL paramétré (`%s`) ; colonnes dynamiques filtrées par liste blanche
   - [ ] Tables héritées en `managed = False` ; aucune migration ne les crée ni ne les modifie
   - [ ] Gestion correcte des erreurs (journalisées, jamais avalées en silence)
   - [ ] Requêtes N+1 évitées (`select_related` / `prefetch_related`)
   - [ ] Formulaires validés (`clean_<champ>()`), pot de miel et limite par IP sur les formulaires publics
   - [ ] Vues : méthode imposée par décorateur, bons codes HTTP (400, 403, 404, 429)
   - [ ] Appels externes avec délai explicite, jamais de synchronisation longue dans une requête HTTP
   - [ ] Gabarits : textes en français, clés `data-i18n` présentes dans les traductions
   - [ ] Requêtes `.http` à jour pour les fonctionnalités modifiées

4. **Présentez les constats** classés par gravité, avec références `chemin:ligne` :
   - Critique (à corriger impérativement)
   - Avertissement (à corriger de préférence)
   - Suggestion (amélioration possible)
