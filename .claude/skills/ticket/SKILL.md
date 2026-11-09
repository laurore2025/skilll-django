---
name: ticket
description: "Traite un ticket JIRA/Linear de bout en bout : lire les détails du ticket, explorer la base de code, créer une branche, implémenter en TDD, lancer les contrôles qualité, mettre à jour le statut du ticket et créer une PR. À utiliser lorsque l'utilisateur fournit un identifiant de ticket à implémenter. Se déclenche sur des demandes comme « /ticket PROJ-123 », « travaille sur ce ticket », « implémente PROJ-123 »."
---

# Flux de travail d'un ticket

Traitez le ticket dont l'identifiant est fourni par l'utilisateur.

## Instructions

### 1. Lisez le ticket

Récupérez et comprenez le ticket à l'aide des outils MCP JIRA/Linear :
- Obtenez les détails du ticket (titre, description, critères d'acceptation)
- Vérifiez les tickets ou epics liés
- Passez en revue les éventuels commentaires ou pièces jointes

Résumez : ce qui doit être fait, les critères d'acceptation, les blocages ou dépendances.

### 2. Explorez la base de code

Avant de coder, appliquez le skill `conventions-django` (structure, langue, sécurité, git), puis :
- Recherchez le code associé
- Comprenez l'implémentation actuelle
- Identifiez les fichiers à modifier

### 3. Placez-vous sur la bonne branche

Dans les projets maison, le travail se fait sur `dev` ; une branche dédiée, issue de `dev`, seulement si
l'utilisateur la demande :

```bash
git switch dev
# ou, sur demande : git switch -c {ticket-id}-{brief-description} dev
```

### 4. Implémentez les modifications

- Suivez les patrons du projet (consultez les skills pertinents, `conventions-django` en premier)
- Ajoutez ou complétez les requêtes REST Client (`<projet>/http/NN_sujet.http`) ; si le projet a des
  tests automatisés, écrivez d'abord le test (TDD)
- Faites des commits incrémentaux, en français, sans attribution Claude

### 5. Lancez les contrôles qualité

Depuis `<projet>/` (sous Linux : `../venv/bin/python`) :

```bash
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
..\venv\Scripts\python.exe manage.py test          # si le projet a des tests
```

Puis passez les requêtes `.http` concernées (voir le skill `code-quality`).

### 6. Mettez à jour le ticket

Au fil du travail :
- Ajoutez des commentaires pour signaler l'avancement
- Mettez à jour le statut (In Progress → In Review)
- Consignez les éventuels blocages ou questions

### 7. Créez la PR et liez-la

Quand c'est prêt :
- Créez la PR avec `gh pr create`
- Liez la PR au ticket
- Ajoutez l'identifiant du ticket au titre de la PR, en français : `PROJ-123 — Sujet : précisions`
- Aucune attribution Claude dans la PR ; ne poussez la branche que si l'utilisateur le demande

### 8. Si vous trouvez un bug

Si vous découvrez un bug sans rapport avec la tâche en cours de travail :
1. Créez un nouveau ticket avec les détails
2. Liez-le au ticket en cours s'il y est lié
3. Mentionnez-le dans la description de la PR
4. Poursuivez la tâche initiale
