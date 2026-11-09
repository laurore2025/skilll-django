# Patrons de workflow

## Workflows séquentiels

Pour les tâches complexes, découpez les opérations en étapes claires et séquentielles. Il est souvent utile de donner à Claude une vue d'ensemble du processus vers le début de SKILL.md :

```markdown
Remplir un formulaire PDF comporte les étapes suivantes :

1. Analyser le formulaire (lancer analyze_form.py)
2. Créer la correspondance des champs (modifier fields.json)
3. Valider la correspondance (lancer validate_fields.py)
4. Remplir le formulaire (lancer fill_form.py)
5. Vérifier le résultat (lancer verify_output.py)
```

## Workflows conditionnels

Pour les tâches comportant des embranchements, guidez Claude à travers les points de décision :

```markdown
1. Déterminez le type de modification :
   **Création de nouveau contenu ?** → Suivez le « Workflow de création » ci-dessous
   **Modification de contenu existant ?** → Suivez le « Workflow de modification » ci-dessous

2. Workflow de création : [étapes]
3. Workflow de modification : [étapes]
```
