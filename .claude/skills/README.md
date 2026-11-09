# Skills Claude Code

Ce répertoire contient des skills propres au projet, qui apportent à Claude la connaissance du domaine et les bonnes pratiques de cette base de code Django.

## Skills par catégorie

### Conventions maison (à appliquer en premier)
| Skill | Description |
|-------|-------------|
| [conventions-django](./conventions-django/SKILL.md) | Style de développement et structure des projets Django de Laurore : structure du dépôt, settings piloté par `.env`, PostgreSQL/PostGIS sans GeoDjango, français, intégrations, tests REST Client, git sans attribution, déploiement Docker. **Prime sur les autres skills en cas de conflit.** |

### Méta et outils de développement
| Skill | Description |
|-------|-------------|
| [skill-creator](./skill-creator/SKILL.md) | Guide pour créer des skills efficaces qui étendent les capacités de Claude |
| [django-extensions](./django-extensions/SKILL.md) | Commandes de gestion de django-extensions pour l'introspection, le débogage et le développement |

### Flux de travail
| Skill | Description |
|-------|-------------|
| [onboard](./onboard/SKILL.md) | Préparer Claude à une nouvelle tâche en explorant la base de code et en construisant le contexte |
| [ticket](./ticket/SKILL.md) | Traiter un ticket JIRA/Linear de bout en bout |
| [pr-review](./pr-review/SKILL.md) | Faire la revue d'une pull request selon les standards du projet |
| [pr-summary](./pr-summary/SKILL.md) | Générer un résumé de pull request pour la branche courante |
| [code-quality](./code-quality/SKILL.md) | Exécuter les contrôles de qualité du code et présenter les constats par gravité |
| [docs-sync](./docs-sync/SKILL.md) | Vérifier que la documentation est synchronisée avec le code |
| [worktree-commit-merge](./worktree-commit-merge/SKILL.md) | Commiter les modifications du worktree, fusionner (merge) dans master/main, synchroniser la branche |

### Tests et débogage
| Skill | Description |
|-------|-------------|
| [pytest-django-patterns](./pytest-django-patterns/SKILL.md) | pytest-django, Factory Boy, fixtures, flux de travail TDD |
| [systematic-debugging](./systematic-debugging/SKILL.md) | Méthode de débogage en quatre phases, analyse de la cause racine |

### Cœur de Django
| Skill | Description |
|-------|-------------|
| [django-models](./django-models/SKILL.md) | Conception des modèles, optimisation des QuerySet, signaux, migrations |
| [django-forms](./django-forms/SKILL.md) | Gestion des formulaires, validation, patrons ModelForm |
| [django-templates](./django-templates/SKILL.md) | Héritage de gabarits, balises, filtres, gabarits partiels |

### Frontend et interface utilisateur
| Skill | Description |
|-------|-------------|
| [htmx-patterns](./htmx-patterns/SKILL.md) | Attributs HTMX, gabarits partiels, interface dynamique |

### Tâches d'arrière-plan
| Skill | Description |
|-------|-------------|
| [celery-patterns](./celery-patterns/SKILL.md) | Tâches Celery, stratégies de nouvelle tentative, tâches périodiques |

## Combinaisons de skills pour les tâches courantes

### Développer une nouvelle fonctionnalité
0. **conventions-django** - Structure, langue, sécurité et git (toujours en premier)
1. **django-models** - Concevez les modèles
2. **django-forms** - Créez les formulaires de saisie utilisateur
3. **htmx-patterns** - Interface dynamique (si le projet utilise HTMX ; sinon `fetch` + `JsonResponse`)
4. **django-templates** - Gabarits de page
5. **pytest-django-patterns** - Écrivez les tests (si le projet utilise pytest ; sinon requêtes REST Client `.http`)

### Développer une tâche d'arrière-plan
0. **conventions-django** - Par défaut, commande de gestion (`--loop`) plutôt que Celery
1. **celery-patterns** - Définition de la tâche (si une vraie file de tâches est nécessaire)
2. **django-models** - Opérations sur la base de données
3. **pytest-django-patterns** - Tests de la tâche

### Déboguer un problème
1. **systematic-debugging** - Analyse de la cause racine
2. **pytest-django-patterns** - Écrivez d'abord un test qui échoue
3. **django-extensions** - Utilisez show_urls, list_model_info, shell_plus pour l'investigation

### Créer de nouveaux skills
1. **skill-creator** - Suivez le guide de création de skills
2. **django-extensions** - Testez votre skill avec les commandes d'introspection du projet

## Fonctionnement des skills

Les skills sont invoqués automatiquement lorsque Claude reconnaît un contexte pertinent. Chaque skill fournit :

- **Quand l'utiliser** - Conditions de déclenchement
- **Patrons essentiels** - Bonnes pratiques et exemples
- **Anti-patrons** - Ce qu'il faut éviter
- **Intégration** - Comment les skills s'articulent entre eux

## Ajouter de nouveaux skills

1. Créez le répertoire : `.claude/skills/skill-name/`
2. Ajoutez `SKILL.md` (sensible à la casse) avec un frontmatter YAML :
   ```yaml
   ---
   # Champs obligatoires
   name: skill-name              # Minuscules, tirets, 64 caractères max.
   description: Ce qu'il fait et quand l'utiliser. Incluez des mots-clés déclencheurs.  # 1 024 caractères max.

   # Champs facultatifs
   allowed-tools: Read, Grep, Glob    # Restreint les outils disponibles
   model: claude-sonnet-4-20250514    # Modèle spécifique à utiliser
   ---
   ```
3. Incluez les sections standard : Quand l'utiliser, Patrons essentiels, Anti-patrons, Intégration
4. Ajoutez-le à ce README
5. Ajoutez les déclencheurs dans `.claude/hooks/skill-rules.json`

**Important :** le champ `description` est essentiel — Claude s'appuie sur une correspondance sémantique avec ce champ pour décider quand appliquer le skill. Incluez les mots-clés que les utilisateurs mentionneraient naturellement.

## Maintenance

- Mettez à jour les skills lorsque les patrons évoluent
- Supprimez les informations obsolètes
- Ajoutez de nouveaux patrons à mesure qu'ils apparaissent
- Maintenez les exemples à jour par rapport à la base de code
