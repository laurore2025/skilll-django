# Patrons de sortie

Utilisez ces patrons lorsque des skills doivent produire un résultat cohérent et de grande qualité.

## Patron de gabarit

Fournissez des gabarits pour le format de sortie. Adaptez le niveau de rigueur à vos besoins.

**Pour des exigences strictes (comme des réponses d'API ou des formats de données) :**

```markdown
## Structure du rapport

Utilisez TOUJOURS exactement cette structure de gabarit :

# [Titre de l'analyse]

## Synthèse
[Vue d'ensemble des principaux constats en un paragraphe]

## Principaux constats
- Constat 1 avec données à l'appui
- Constat 2 avec données à l'appui
- Constat 3 avec données à l'appui

## Recommandations
1. Recommandation précise et applicable
2. Recommandation précise et applicable
```

**Pour des consignes souples (quand une adaptation est utile) :**

```markdown
## Structure du rapport

Voici un format par défaut raisonnable, mais faites preuve de discernement :

# [Titre de l'analyse]

## Synthèse
[Vue d'ensemble]

## Principaux constats
[Adaptez les sections en fonction de ce que vous découvrez]

## Recommandations
[Adaptez au contexte précis]

Ajustez les sections selon le type d'analyse.
```

## Patron d'exemples

Pour les skills dont la qualité du résultat dépend d'exemples, fournissez des paires entrée/sortie :

```markdown
## Format des messages de commit

Générez les messages de commit en suivant ces exemples :

**Exemple 1 :**
Entrée : ajout de l'authentification des utilisateurs avec des jetons JWT
Sortie :
```
feat(auth): implémenter l'authentification par JWT

Ajouter un endpoint de connexion et un middleware de validation des jetons
```

**Exemple 2 :**
Entrée : correction d'un bug qui affichait des dates incorrectes dans les rapports
Sortie :
```
fix(reports): corriger le formatage des dates lors de la conversion de fuseau horaire

Utiliser des horodatages UTC de façon cohérente dans toute la génération des rapports
```

Suivez ce style : type(scope): brève description, puis explication détaillée.
```

Les exemples aident Claude à comprendre le style et le niveau de détail souhaités plus clairement que de simples descriptions.
