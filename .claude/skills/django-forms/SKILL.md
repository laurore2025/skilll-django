---
name: django-forms
description: "Patrons de gestion des formulaires Django : ModelForm, validation, méthodes clean et soumission de formulaires avec HTMX. À utiliser pour créer des formulaires, implémenter une validation ou gérer la soumission de formulaires."
---

# Formulaires Django

## Philosophie

- Préférez ModelForm pour les formulaires adossés à un modèle
- Gardez la logique de validation dans les formulaires, pas dans les vues
- Gérez et affichez toujours les erreurs de formulaire
- Utilisez `commit=False` lorsque vous devez modifier l'instance avant l'enregistrement

## Validation

**Au niveau du champ** (`clean_<field>`) :
- Validez et transformez un seul champ
- Renvoyez la valeur nettoyée ou levez `ValidationError`
- À utiliser pour : contrôles de format, unicité, normalisation

**Entre plusieurs champs** (`clean`) :
- Appelez d'abord `super().clean()`
- Accédez à plusieurs champs via `cleaned_data`
- Utilisez `self.add_error(field, message)` pour les erreurs propres à un champ
- À utiliser pour : confirmation du mot de passe, exigences conditionnelles

## Intégration aux vues

- Vérifiez explicitement `request.method`
- Instanciez le formulaire avec `request.POST` pour un POST, sans données pour un GET
- Utilisez `form.save(commit=False)` pour renseigner des champs supplémentaires (par ex. l'auteur)
- Redirigez en cas de succès, réaffichez le formulaire en cas d'erreur

**Gestion HTMX :**
- Vérifiez `request.headers.get("HX-Request")` pour détecter les requêtes HTMX
- Renvoyez un gabarit partiel en cas de succès ou d'erreur pour HTMX
- Utilisez l'en-tête `HX-Trigger` pour notifier les autres composants

## Gabarits

- Affichez `form.non_field_errors` pour les erreurs portant sur plusieurs champs
- Affichez `field.errors` pour chaque champ
- Utilisez des gabarits partiels (`_form.html`) pour les réponses HTMX
- Incluez un indicateur de chargement avec `hx-indicator`

## Widgets

- Surchargez-les dans le dictionnaire `Meta.widgets`
- Définissez les attributs HTML via le paramètre `attrs`
- Courants : `Textarea(attrs={"rows": 5})`, `DateTimeInput(attrs={"type": "datetime-local"})`

## Formsets

- Utilisez `inlineformset_factory` pour les collections de modèles liés
- Validez à la fois le formulaire et le formset : `form.is_valid() and formset.is_valid()`
- Passez `instance` pour modifier des objets parents existants

## Pièges

- Valider dans les vues au lieu des formulaires
- Rediriger silencieusement sans vérifier `is_valid()`
- Oublier `commit=False` lors du renseignement des champs liés
- Ne pas afficher les erreurs de formulaire aux utilisateurs
