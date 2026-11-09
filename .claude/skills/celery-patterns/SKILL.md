---
name: celery-patterns
description: "Patrons de tâches Celery : définition des tâches, stratégies de nouvelle tentative (retry), tâches périodiques et bonnes pratiques. À utiliser pour implémenter des tâches d'arrière-plan, des tâches planifiées ou des traitements asynchrones."
---

# Patrons Celery pour Django

> **Dans les projets maison** : Celery n'est pas utilisé par défaut. Les traitements hors requête passent par des commandes de gestion (`sync_<source> --loop`) lancées par un service Docker, cron ou une tâche planifiée Windows.
> Appliquez d'abord le skill `conventions-django` ; ce skill ne sert que si le projet a adopté cet outil.


## Philosophie de base

- **Tâches idempotentes** : exécuter une tâche deux fois doit produire le même résultat
- **Passez des identifiants, pas des objets** : les arguments doivent être sérialisables en JSON
- **Gérez toujours les échecs** : journalisez les erreurs, n'avalez jamais les exceptions silencieusement
- **Stratégies de nouvelle tentative adaptées** : utilisez un backoff exponentiel pour les services externes

## Conception des tâches

### Structure
- Placez les tâches dans `apps/<app>/tasks.py`
- Utilisez `@shared_task` pour les tâches réutilisables d'un projet à l'autre
- Utilisez `bind=True` lorsque vous avez besoin d'accéder à l'instance de la tâche (nouvelles tentatives, ID de tâche, mises à jour d'état)
- Ajoutez des annotations de type aux signatures des tâches
- Journalisez le démarrage, la fin et les échecs des tâches

### Arguments
- Passez les clés primaires des modèles, pas les instances de modèles
- Gardez des arguments simples et sérialisables (str, int, dict, list)
- Vérifiez que les objets référencés existent au démarrage de la tâche

## Stratégies de nouvelle tentative

### Quand utiliser chaque approche
- **Délai fixe** : opérations internes dont la reprise est prévisible (verrous de base de données)
- **Backoff exponentiel** : API externes susceptibles d'appliquer une limitation de débit ou dont la reprise est variable
- **Aucune nouvelle tentative** : erreurs de validation, échecs de logique métier, erreurs permanentes

### Configuration
- Définissez `max_retries` en fonction du temps d'attente total acceptable
- Utilisez `retry_jitter=True` pour éviter l'effet de ruée (thundering herd)
- Définissez `retry_backoff_max` pour plafonner le temps d'attente maximal
- Utilisez le tuple `autoretry_for` pour une nouvelle tentative automatique sur des exceptions spécifiques

## Patrons d'idempotence

### Vérifier avant de traiter
Interrogez l'état courant avant le traitement ; ignorez l'opération si elle est déjà terminée

### Suivi par champ de statut
Utilisez des transitions de statut (pending → processing → complete/failed) avec `select_for_update()` pour vous prémunir contre les situations de concurrence

### Contraintes d'unicité
Utilisez des contraintes de base de données pour éviter les traitements en double

## Tâches périodiques (Beat)

- Configurez les planifications dans `config/celery.py` via `beat_schedule`
- Utilisez `crontab()` pour les planifications basées sur l'heure
- Utilisez des valeurs flottantes pour les planifications par intervalle (en secondes)
- Gardez les tâches périodiques légères ; lancez des sous-tâches pour les traitements lourds

## Anti-patrons à éviter

- Passer des instances de modèles au lieu d'identifiants
- Opérations non idempotentes (incrémenter sans vérification)
- Gestion silencieuse des exceptions (`except: pass` nu)
- Absence de journalisation du cycle de vie des tâches
- Tâches longues sans mises à jour de progression
- Nouvelle tentative sur des échecs permanents (validation, erreurs de logique métier)

## Commandes

Depuis `<projet>/`, avec le venv du dépôt (`<projet>` = paquet de configuration Django) :

- Worker : `..\venv\Scripts\python.exe -m celery -A <projet> worker -l info`
- Beat : `..\venv\Scripts\python.exe -m celery -A <projet> beat -l info`
- Supervision : `..\venv\Scripts\python.exe -m celery -A <projet> flower`
