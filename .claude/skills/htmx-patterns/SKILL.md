---
name: htmx-patterns
description: "Patrons HTMX pour Django : gabarits partiels, attributs hx-* et interface dynamique sans JavaScript. À utiliser pour construire une interface interactive, gérer des requêtes AJAX ou créer des composants dynamiques."
---

# Patrons HTMX pour Django

## Philosophie de base

- Le serveur produit du HTML, pas du JSON - les requêtes HTMX renvoient des fragments HTML, pas des données
- Des gabarits partiels pour les mises à jour dynamiques - des fichiers `_partial.html` séparés pour les réponses HTMX
- Amélioration progressive - les pages fonctionnent sans JavaScript, HTMX améliore l'expérience utilisateur
- Complexité minimale côté client - laissez le serveur faire le gros du travail

## Conseils et rappels essentiels

### Bonnes pratiques UX

**Incluez toujours des indicateurs de chargement**
- Utilisez `hx-indicator` pour afficher les états de chargement pendant les requêtes
- Les utilisateurs ne doivent jamais se demander si leur action a fonctionné
- Exemple : `<button hx-get="/data/" hx-indicator="#spinner">Charger</button>`

**Fournissez toujours un retour à l'utilisateur**
- Utilisez le framework de messages de Django pour les retours de succès ou d'erreur
- Renvoyez des messages d'erreur dans les réponses HTMX, pas des échecs silencieux
- Montrez ce qui s'est passé une fois l'action terminée

**Gérez les erreurs proprement**
- Renvoyez les codes de statut HTTP appropriés (400 pour les erreurs de validation, 500 pour les erreurs serveur)
- Affichez les erreurs de formulaire dans les gabarits partiels
- N'avalez pas les exceptions - journalisez-les et affichez des messages compréhensibles par l'utilisateur

### Patrons propres à Django

**Détectez toujours les requêtes HTMX**
- Vérifiez `request.headers.get("HX-Request")` pour détecter les requêtes HTMX
- Renvoyez des gabarits partiels pour HTMX, des gabarits de page complète sinon
- Patron : `if request.headers.get("HX-Request"): return render(request, "_partial.html", context)`

**Renvoyez toujours des gabarits partiels pour HTMX**
- Les requêtes HTMX doivent renvoyer des gabarits `_partial.html`, pas des pages complètes avec `base.html`
- Des réponses en page complète à des requêtes HTMX dégradent l'expérience utilisateur et envoient du HTML en double
- Les gabarits partiels doivent être des fragments HTML autonomes

**Validez toujours request.method**
- Vérifiez `request.method == "POST"` avant de traiter les données du formulaire
- Renvoyez les codes de statut appropriés (405 Method Not Allowed pour les mauvaises méthodes)

**Le CSRF est déjà configuré globalement**
- Le gabarit de base place `hx-headers` sur `<body>` - inutile d'ajouter des jetons CSRF à chaque formulaire
- Toutes les requêtes HTMX incluent automatiquement le jeton CSRF

### Organisation des gabarits

**Convention de nommage**
- Gabarits partiels : `_partial.html` (préfixe tiret bas)
- Pages complètes : `page.html` (sans préfixe)
- Exemple : `posts/list.html` (page complète) inclut `posts/_list.html` (gabarit partiel)

**Structure**
- Le gabarit de page complète étend `base.html` et inclut le gabarit partiel
- Le gabarit partiel ne contient que le fragment HTML dynamique
- HTMX cible la div conteneur du gabarit partiel

**Gardez des gabarits partiels ciblés**
- Chaque gabarit partiel doit représenter un seul composant d'interface logique
- Évitez les gabarits partiels trop volumineux ou qui en font trop
- Composez les interfaces plus vastes à partir de plusieurs gabarits partiels plus petits

## Patrons de vues Django

### Détection HTMX

Vérifiez l'en-tête `HX-Request` pour détecter les requêtes HTMX :

```python
def my_view(request):
    context = {...}

    if request.headers.get("HX-Request"):
        return render(request, "app/_partial.html", context)

    return render(request, "app/full_page.html", context)
```

### Patron de gestion des formulaires

Points clés :
- Validez le formulaire normalement
- En cas de succès : renvoyez un gabarit partiel avec les nouvelles données OU déclenchez un événement côté client
- En cas d'erreur : renvoyez un gabarit partiel avec les erreurs du formulaire
- Gérez toujours les deux cas, HTMX et non-HTMX

```python
def create_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if request.headers.get("HX-Request"):
                return render(request, "app/_item.html", {"item": obj})
            return redirect("app:list")

        # Renvoyer le formulaire avec ses erreurs
        if request.headers.get("HX-Request"):
            return render(request, "app/_form.html", {"form": form})
    else:
        form = MyForm()

    return render(request, "app/create.html", {"form": form})
```

## Référence des en-têtes de réponse

HTMX tient compte d'en-têtes de réponse spéciaux pour piloter le comportement côté client :

### HX-Trigger
Déclenche des événements côté client après la réponse
- Cas d'usage : mettre à jour d'autres parties de la page après une action
- Exemple : `response["HX-Trigger"] = "itemCreated"`
- Le gabarit écoute : `<div hx-get="/count/" hx-trigger="itemCreated from:body">`

### HX-Redirect
Redirection côté client
- Cas d'usage : rediriger après une action réussie
- Exemple : `response["HX-Redirect"] = reverse("app:detail", args=[obj.pk])`

### HX-Retarget / HX-Reswap
Surcharge hx-target et hx-swap depuis le serveur
- Cas d'usage : des cibles différentes en cas de succès et d'erreur
- Succès : `response["HX-Retarget"] = "#main"`
- Erreur : renvoyez le gabarit partiel sans changer de cible (cible le formulaire)

### HX-Refresh
Force le rechargement complet de la page
- Cas d'usage : changement d'état majeur qui affecte toute la page
- Exemple : `response["HX-Refresh"] = "true"`

## Pièges courants

- **Indicateurs de chargement manquants** : utilisez toujours `hx-indicator` - sans retour visuel, les utilisateurs cliquent plusieurs fois
- **Pages complètes dans les réponses HTMX** : renvoyez `_partial.html`, pas des pages complètes avec `base.html` - vérifiez l'en-tête `HX-Request`
- **Erreurs de formulaire non gérées** : renvoyez toujours le formulaire avec ses erreurs en cas d'échec de validation, ne traitez pas seulement le cas de succès
- **Boutons non désactivés** : utilisez `hx-disabled-elt="this"` pour éviter les soumissions en double
- **Requêtes N+1** : les vues HTMX ont besoin de `select_related()`/`prefetch_related()` tout comme les vues classiques

## Intégration avec les autres skills

- **django-templates** : organisation des gabarits partiels et patrons d'héritage
- **django-forms** : soumission et validation de formulaires avec HTMX
- **django-extensions** : utilisez `show_urls` pour vérifier les points de terminaison HTMX
- **pytest-django-patterns** : tests des points de terminaison et des en-têtes HTMX
- **systematic-debugging** : débogage des problèmes de requête/réponse HTMX
