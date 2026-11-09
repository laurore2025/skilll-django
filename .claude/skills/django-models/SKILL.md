---
name: django-models
description: "Patrons de conception des modèles Django privilégiant les modèles riches et les vues légères (fat models/thin views), l'optimisation des QuerySet et l'encapsulation de la logique du domaine. À utiliser pour concevoir des modèles, optimiser des requêtes, implémenter de la logique métier ou travailler avec l'ORM."
---

# Patrons de modèles Django

> **Dans les projets maison** (skill `conventions-django`) : noms métier et `verbose_name` en français ;
> tables héritées en `managed = False` (jamais recréées par une migration) ; tables PostGIS créées par
> `migrations.RunSQL` avec SQL inverse, sans GeoDjango ; configuration éditable par un modèle à
> enregistrement unique (`charger()`). Exemples : `conventions-django/references/modeles-de-code.md`.

## Philosophie de base : modèles riches, vues légères

**La logique métier a sa place dans les modèles et les managers, pas dans les vues.** Les vues orchestrent les flux de travail ; les modèles implémentent le comportement du domaine. Ce principe produit un code testable et réutilisable, qui reste maintenable à mesure que la complexité augmente.

**Bien** : les méthodes de modèle gèrent les règles métier, les transitions d'état, la validation
**Mal** : les vues contiennent de la logique if/else pour les règles du domaine, calculent des valeurs dérivées

## Conception des modèles

### Structurez vos modèles autour des concepts du domaine
- Utilisez `TextChoices`/`IntegerChoices` pour les champs de statut et les énumérations
- Ajoutez `get_absolute_url()` pour les URL canoniques des objets
- Incluez `__str__()` pour des représentations lisibles
- Définissez un `ordering` approprié dans Meta pour un tri par défaut cohérent
- Ajoutez des index de base de données pour les champs fréquemment filtrés ou triés
- Utilisez des modèles de base abstraits pour les champs partagés (horodatages, suppressions logiques, etc.)

### Règles de choix des champs
- Utilisez `blank=True, default=""` pour les champs texte facultatifs (évitez null)
- Utilisez `null=True, blank=True` pour les clés étrangères facultatives
- Pour les champs uniques facultatifs, utilisez `null=True` afin d'éviter les problèmes de collision
- Tirez parti de `JSONField` pour les métadonnées flexibles (évitez de créer de nombreux champs facultatifs)
- Définissez une `max_length` adaptée aux besoins réels des données

### Encapsulez la logique métier dans les méthodes de modèle
- Transitions d'état : `post.publish()`, `order.cancel()`
- Vérifications de permissions : `post.is_editable_by(user)`
- Calculs complexes : `invoice.calculate_total()`
- Utilisez des propriétés pour les valeurs calculées en lecture seule
- Précisez `update_fields` lors de l'enregistrement de modifications partielles

## Patrons de QuerySet : la puissance de la composition

**Les classes QuerySet personnalisées sont votre arme secrète.** Elles rendent les requêtes réutilisables, chaînables et testables.

### Patron : QuerySet comme manager
```
Définissez une sous-classe de QuerySet avec des méthodes de filtrage propres au domaine
Attachez-la à votre modèle : objects = YourQuerySet.as_manager()
Chaînez les méthodes pour composer des requêtes
```

### Avantages
- Logique de requête réutilisable dans les vues, les tâches, les commandes de gestion
- Les méthodes chaînables permettent des requêtes expressives et lisibles
- Faciles à tester isolément
- Encapsulent la complexité des requêtes à l'écart des vues

### Méthodes de QuerySet courantes
- Filtrage par statut/état
- Requêtes par plage de dates (récents, à venir, expirés)
- Requêtes limitées à un utilisateur (owned_by, visible_to)
- Recherches combinées (published_and_recent)

## Optimisation des requêtes : évitez les requêtes N+1

### Les règles d'or
1. **select_related()** : à utiliser pour ForeignKey et OneToOneField (crée une jointure SQL)
2. **prefetch_related()** : à utiliser pour ManyToManyField et les ForeignKey inverses (requête séparée + jointure en Python)
3. **only()** : chargez uniquement certains champs lorsque vous n'avez pas besoin de l'objet entier
4. **defer()** : excluez les champs lourds (TextField, JSONField) que vous n'utiliserez pas
5. Objet **Prefetch()** : personnalisez le préchargement avec des filtres et select_related

### Comptages et tests d'existence efficaces
- Utilisez `.exists()` au lieu de `if queryset:` ou `if len(queryset):`
- Utilisez `.count()` au lieu de `len(queryset.all())`
- Les deux effectuent l'opération au niveau de la base de données sans charger les objets

### Agrégation et annotation
- `annotate()` : ajoute des champs calculés à chaque objet (Count, Sum, Avg, etc.)
- `aggregate()` : calcule des valeurs sur l'ensemble du queryset
- Utilisez des expressions `F()` pour les mises à jour au niveau de la base de données (`views=F('views') + 1`)
- Combinez annotate et filter pour obtenir les « objets ayant au moins N éléments liés »

## Managers ou QuerySets

**Utilisez les QuerySets pour la logique de requête chaînable.**
**Utilisez les Managers pour les opérations au niveau du modèle qui ne renvoient pas de querysets.**

Manager : pensez « méthodes factory » - `User.objects.create_user()`
QuerySet : pensez « filtres et transformations » - `Post.objects.published().recent()`

La plupart du temps, c'est un QuerySet personnalisé qu'il vous faut, pas un Manager personnalisé.

## Signaux : à utiliser avec parcimonie

Les signaux créent un couplage implicite et rendent le code plus difficile à suivre. **Préférez les appels de méthode explicites.**

### Quand les signaux ont du sens
- Journalisation d'audit (suivi de toutes les modifications d'un modèle)
- Invalidation de cache (vider le cache quand le modèle change)
- Découplage d'applications (une application tierce doit réagir à vos modèles)

### Quand éviter les signaux
- Logique métier qui devrait se trouver dans les méthodes de modèle
- Logique étroitement couplée au code appelant (appelez simplement la fonction directement)
- Flux de travail complexes (utilisez plutôt une couche de services explicite)

**Règle empirique** : si vous contrôlez à la fois le déclencheur et la réaction, n'utilisez pas de signal.

## Migrations

### Flux de travail
- Exécutez `makemigrations` après toute modification des modèles
- Relisez les fichiers de migration générés avant de les appliquer
- Exécutez `migrate` pour appliquer les migrations
- Les migrations doivent être réversibles autant que possible

### Migrations de données
Créez-les avec `makemigrations --empty app_name`. Utilisez `apps.get_model()` pour accéder aux modèles (pas d'imports directs). Écrivez à la fois l'opération aller et l'opération retour.

**Utilisez les migrations de données pour** : renseigner de nouveaux champs, transformer des données, migrer d'un champ à un autre.

## Anti-patrons à éviter

### Anti-patrons de requêtes
- Itérer sur des objets et accéder à leurs relations sans `select_related()`/`prefetch_related()`
- Utiliser `if queryset:` au lieu de `.exists()`
- Utiliser `len()` pour compter au lieu de `.count()`
- Charger des objets entiers alors que vous n'avez besoin que de certains champs

### Anti-patrons de conception
- Logique métier dans les vues au lieu des modèles
- Vues effectuant des calculs qui relèvent des méthodes de modèle
- Usage excessif des signaux pour des opérations synchrones
- Création de nouveaux modèles alors qu'un JSONField suffirait
- Oubli des index sur les champs filtrés ou triés

## Intégration

Fonctionne avec :
- **pytest-django-patterns** : tests de modèles à base de factories
- **celery-patterns** : opérations asynchrones sur les modèles (passez des identifiants, pas des instances)
- **django-forms** : validation et enregistrement via ModelForm
