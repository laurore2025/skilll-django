---
name: django-extensions
description: "Commandes de gestion de django-extensions pour l'introspection du projet, le débogage et le développement. À utiliser pour explorer les URL, les modèles, les réglages (settings), le schéma de la base de données, exécuter des scripts ou profiler les performances. Se déclenche sur des questions portant sur la structure du projet Django, les champs des modèles, les routes d'URL, ou sur des demandes de lancement des serveurs de développement."
---

# Django Extensions

Ce projet dispose de django-extensions. Utilisez ces commandes pour comprendre le projet Django et interagir avec lui.

## Introspection

### Afficher les routes d'URL
```bash
python manage.py show_urls
```

### Lister les informations des modèles
```bash
# Tous les modèles
python manage.py list_model_info

# Modèle spécifique avec signatures et classes de champs
python manage.py list_model_info --model <app.Model> --signature --field-class

# Toutes les méthodes, y compris privées
python manage.py list_model_info --model <app.Model> --all-methods --signature
```

### Afficher les réglages
```bash
# Tous les réglages
python manage.py print_settings --format=pprint

# Caractères génériques pris en charge
python manage.py print_settings AUTH*
python manage.py print_settings DATABASE*
python manage.py print_settings *_DIRS
```

### Afficher les permissions
```bash
python manage.py show_permissions
python manage.py show_permissions <app_label>
```

### Afficher les balises de gabarit
```bash
python manage.py show_template_tags
```

## Développement

### Shell amélioré (shell_plus)
```bash
python manage.py shell_plus
python manage.py shell_plus --print-sql
```
Importe automatiquement tous les modèles. Utilisez `--dont-load app1` pour ignorer des applications.

### Serveur de développement amélioré (runserver_plus)
```bash
python manage.py runserver_plus
python manage.py runserver_plus --print-sql
```
Inclut le débogueur Werkzeug pour le débogage interactif.

## Base de données

### SQL Diff (comparer les modèles au schéma)
```bash
python manage.py sqldiff -a        # Différences SQL
python manage.py sqldiff -a -t     # Différences en texte (lisibles)
```

## Exécution de scripts

### Exécuter des scripts dans le contexte Django
```bash
python manage.py runscript <script_name>
python manage.py runscript <script_name> --script-args arg1 arg2
python manage.py runscript <script_name> --traceback
```
Les scripts du répertoire `scripts/` doivent définir une fonction `run()`.

## Profilage

### Profiler les requêtes du serveur
```bash
python manage.py runprofileserver --prof-path=/tmp/profiles
python manage.py runprofileserver --use-cprofile --prof-path=/tmp/profiles
python manage.py runprofileserver --kcachegrind --prof-path=/tmp/profiles
```

## Remarques

- Notation des modèles : `app.ModelName` (par ex. `core.EmailAccount`, `metabox.Thread`)
- Caractères génériques dans les réglages : `AUTH*`, `*_DIRS`, `DATABASE*`
- Les commandes s'exécutent depuis la racine du projet
