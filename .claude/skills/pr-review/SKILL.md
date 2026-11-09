---
name: pr-review
description: "Fait la revue d'une pull request selon les standards du projet. À utiliser lorsque l'utilisateur veut faire relire une PR, vérifier la qualité du code ou obtenir un retour structuré sur des modifications. Accepte un numéro ou une URL de PR en argument. Se déclenche sur des demandes comme « fais une revue de la PR 123 », « vérifie cette pull request », « /pr-review 123 »."
---

# Revue de PR

Faites la revue de la pull request fournie par l'utilisateur (numéro ou URL de PR).

## Instructions

1. **Récupérez les informations de la PR** :
   - Exécutez `gh pr view <PR>` pour obtenir les détails de la PR
   - Exécutez `gh pr diff <PR>` pour voir les modifications

2. **Lisez les standards de revue** :
   - Lisez `.claude/agents/code-reviewer.md` pour connaître la liste de vérification de la revue

3. **Appliquez la liste de vérification** à tous les fichiers modifiés :
   - Respect des annotations de type (pas de `Any`)
   - Patrons de gestion des erreurs (pas d'exceptions silencieuses)
   - Requêtes N+1 évitées (select_related/prefetch_related)
   - États de chargement, d'erreur et vides dans les gabarits
   - Couverture de tests
   - Mises à jour de la documentation

4. **Fournissez un retour structuré** :
   - **Critique** : à corriger avant la fusion (merge)
   - **Avertissement** : à corriger de préférence
   - **Suggestion** : souhaitable

5. **Publiez les commentaires de revue** avec `gh pr comment`
