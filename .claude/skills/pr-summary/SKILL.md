---
name: pr-summary
description: "Génère un résumé de pull request pour les modifications de la branche courante. À utiliser lorsque l'utilisateur veut créer une description de PR, résumer les modifications d'une branche ou préparer le corps d'une PR. Se déclenche sur des demandes comme « résume mes modifications », « rédige une description de PR », « qu'est-ce qui a changé sur cette branche ? », « /pr-summary »."
---

# Résumé de PR

Générez un résumé de pull request pour la branche courante.

## Instructions

1. **Analysez les modifications** :
   ```bash
   git log main..HEAD --oneline
   git diff main...HEAD --stat
   ```

2. **Générez un résumé** comprenant :
   - Une brève description de ce qui a changé
   - La liste des fichiers modifiés
   - Les changements incompatibles (le cas échéant)
   - Des notes sur les tests

3. **Mettez-le en forme comme corps de PR** :
   ```markdown
   ## Résumé
   [1 à 3 puces décrivant les modifications]

   ## Modifications
   - [Liste des modifications significatives]

   ## Plan de test
   - [ ] [Éléments de la liste de vérification des tests]
   ```
