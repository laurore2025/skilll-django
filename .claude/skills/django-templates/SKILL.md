---
name: django-templates
description: "Patrons de gabarits (templates) Django : héritage, gabarits partiels, balises et filtres. À utiliser pour travailler sur des gabarits, créer des composants réutilisables ou organiser la structure des gabarits."
---

# Patrons de gabarits Django

## Organisation des gabarits

```
templates/
├── base.html              # Gabarit racine avec la structure commune
├── partials/              # Fragments réutilisables (barre de navigation, pied de page, pagination)
├── components/            # Composants d'interface (bouton, carte, fenêtre modale)
└── <app>/                 # Gabarits propres à l'application
    ├── list.html          # Les pages complètes étendent base.html
    ├── detail.html
    ├── _list.html         # Gabarits partiels HTMX (préfixe tiret bas)
    └── _form.html
```

**Conventions de nommage :**
- Pages complètes : `list.html`, `detail.html`, `form.html`
- Gabarits partiels HTMX : `_list.html`, `_card.html` (préfixe tiret bas)
- Gabarits partiels partagés : `partials/_navbar.html`, `partials/_pagination.html`
- Composants : `components/_button.html`, `components/_modal.html`

## Héritage de gabarits

Utilisez un héritage à trois niveaux pour des mises en page cohérentes :

1. **base.html** - Structure globale du site (squelette HTML, barre de navigation, pied de page)
2. **Gabarits de section** - Gabarits intermédiaires facultatifs pour les sections qui partagent des éléments
3. **Gabarits de page** - Pages individuelles qui étendent base ou les gabarits de section

**Blocs standard à définir dans base.html :**
- `title` - Titre de la page (utilisez `{{ block.super }}` pour l'ajouter au nom du site)
- `content` - Contenu principal de la page
- `extra_css` - Feuilles de style propres à la page
- `extra_js` - Scripts propres à la page

## Gabarits partiels et composants

Les **gabarits partiels** sont des fragments de gabarit inclus dans d'autres gabarits. Utilisez-les pour :
- Le contenu répété (pagination, états vides)
- Les réponses HTMX qui remplacent des portions de la page
- Garder les gabarits DRY

Les **composants** sont des éléments d'interface autonomes au comportement configurable. Passez-leur le contexte avec :
- `{% include "components/_button.html" with text="Envoyer" variant="primary" %}`
- Ajoutez `only` pour isoler le contexte : `{% include "_card.html" with title=post.title only %}`

## Balises et filtres personnalisés

**Quand créer des balises de gabarit personnalisées :**
- `simple_tag` - Renvoie une valeur de type chaîne (par ex. classe de lien actif, sortie formatée)
- `inclusion_tag` - Effectue le rendu d'un fragment de gabarit (par ex. composant de pagination, avatar d'utilisateur)

**Quand créer des filtres personnalisés :**
- Pour transformer une seule valeur (par ex. initiales à partir d'un nom, calcul de pourcentage)
- Pour les chaîner avec d'autres filtres et composer des transformations

**Emplacement :** `apps/<app>/templatetags/<app>_tags.py` (créez `__init__.py` dans le répertoire templatetags)

## Anti-patrons

**Sortez la logique des gabarits :**
- Les conditions complexes ont leur place dans les vues ou les méthodes de modèle
- Utilisez `user.can_moderate` et non `user.role == "admin" or user.role == "moderator"`

**Utilisez les noms d'URL, pas des chemins codés en dur :**
- Utilisez `{% url 'posts:detail' pk=post.pk %}` et non `/posts/{{ post.id }}/`

**Utilisez des classes CSS, pas des styles en ligne :**
- Utilisez `class="error-message"` et non `style="color: red;"`

**Gérez les états vides :**
- Incluez toujours une clause `{% empty %}` dans les boucles susceptibles de ne contenir aucun élément

## Intégration avec les autres skills

- **htmx-patterns** - Gabarits partiels HTMX et interface dynamique
- **django-forms** - Patrons de rendu et de validation des formulaires
- **pytest-django-patterns** - Tests du rendu des gabarits
