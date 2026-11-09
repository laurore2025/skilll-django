# Configuration de Claude Code pour les projets Django

> La plupart des ingénieurs logiciels sous-estiment sérieusement à quel point les agents LLM sont performants aujourd'hui, en particulier un outil comme Claude Code.

Une fois Claude Code configuré, vous pouvez le diriger vers votre base de code, lui faire apprendre vos conventions, y intégrer les bonnes pratiques et tout affiner jusqu'à ce qu'il fonctionne pratiquement comme un coéquipier doté de super-pouvoirs. **Le vrai déclic, c'est de construire un solide ensemble de « [skills](#skills---connaissances-métier) » réutilisables, plus quelques « [agents](#agents---assistants-spécialisés) », pour les tâches que vous faites tout le temps.**

### Ce que cela donne en pratique

**Des skills de connaissances métier ?** Nous avons [17 skills spécialisés](.claude/skills/), dont [`conventions-django`](.claude/skills/conventions-django/SKILL.md) qui décrit le style maison et prime sur les autres, qui couvrent tout, des [modèles Django](.claude/skills/django-models/SKILL.md) et des [formulaires](.claude/skills/django-forms/SKILL.md) aux [patterns HTMX](.claude/skills/htmx-patterns/SKILL.md) et aux [tâches Celery](.claude/skills/celery-patterns/SKILL.md). Lors du débogage, notre [skill de débogage systématique](.claude/skills/systematic-debugging/SKILL.md) garantit une analyse de la cause racine avant toute correction. Besoin d'explorer votre projet Django ? Utilisez [django-extensions](.claude/skills/django-extensions/SKILL.md). Vous voulez créer de nouveaux skills ? Suivez le [guide skill-creator](.claude/skills/skill-creator/SKILL.md).

**Des contrôles qualité automatisés ?** Des [hooks](.claude/settings.json) (script [garde-fous.js](.claude/hooks/garde-fous.js), documenté dans [settings.md](.claude/settings.md)) protègent le fichier `.env`, [bloquent les modifications sur la branche main](.claude/settings.md), vérifient la syntaxe de chaque fichier Python modifié avec le Python du venv, et rappellent de redémarrer le serveur de vérification après un gabarit modifié. Aucune attribution Claude n'est ajoutée aux commits ni aux PR.

**Une revue de code approfondie ?** Nous avons un [agent de revue de code](.claude/agents/code-reviewer.md) que Claude exécute une fois les modifications effectuées. Il suit une liste de vérification détaillée qui couvre les annotations de type Python, l'optimisation des QuerySet, la gestion des erreurs, la validation des formulaires, et plus encore. Quand une PR est ouverte, une [GitHub Action](.github/workflows/pr-claude-code-review.yml) en fait automatiquement une revue complète.

**Une maintenance planifiée ?** Nous avons des agents de workflow GitHub qui s'exécutent selon un calendrier :
- [Synchronisation mensuelle de la documentation](.github/workflows/scheduled-claude-code-docs-sync.yml) - Lit les commits du dernier mois et vérifie que la documentation est toujours alignée
- [Qualité du code hebdomadaire](.github/workflows/scheduled-claude-code-quality.yml) - Passe en revue des répertoires choisis au hasard et corrige automatiquement les problèmes
- [Audit bimensuel des dépendances](.github/workflows/scheduled-claude-code-dependency-audit.yml) - Mises à jour sûres des dépendances, vérifiées par les tests

**Des suggestions de skills intelligentes ?** Nous avons construit un [système d'évaluation des skills](#hooks-dévaluation-des-skills) qui analyse chaque prompt et suggère automatiquement les skills que Claude doit activer, en fonction des mots-clés, des chemins de fichiers et des motifs d'intention.

Une énorme partie du travail de maintenance et de qualité est tout simplement... automatisée. Et ça tourne incroyablement bien.

**Une intégration JIRA/Linear ?** Nous connectons Claude Code à notre système de tickets via des [serveurs MCP](.mcp.json). Claude peut désormais lire le ticket, comprendre les exigences, implémenter la fonctionnalité, mettre à jour le statut du ticket, et même créer de nouveaux tickets s'il trouve des bugs en cours de route. Le [skill `ticket`](.claude/skills/ticket/SKILL.md) gère l'ensemble du workflow, de la lecture des critères d'acceptation jusqu'à la liaison de la PR avec le ticket.

Nous utilisons même Claude Code pour le tri des tickets. Il lit le ticket, explore la base de code et laisse un commentaire indiquant ce qui, selon lui, devrait être fait. Ainsi, quand un ingénieur prend le ticket, il démarre pratiquement à mi-chemin.

**Il y a tellement de gains faciles à portée de main que je suis franchement sidéré que tout le monde ne s'en empare pas.**

---

## Adaptation maison

Ce dépôt est traduit en français et adapté au style de développement de Laurore :

- **Skill [`conventions-django`](.claude/skills/conventions-django/SKILL.md)** : structure des projets (venv et `.env` à la racine, projet Django dans un sous-dossier, applications sous `<projet>/apps`), `settings.py` unique piloté par `.env`, PostgreSQL/PostGIS en SQL brut, français partout, intégrations externes avec copie locale, tests REST Client, git sans attribution, déploiement Docker. Ses références contiennent des [fichiers modèles](.claude/skills/conventions-django/references/structure-projet.md), des [modèles de code](.claude/skills/conventions-django/references/modeles-de-code.md) et la [procédure de déploiement](.claude/skills/conventions-django/references/deploiement.md).
- **Outillage** : `pip` + `requirements.txt` figé et venv à la racine (pas d'uv) ; pytest, HTMX et Celery restent disponibles mais ne servent que si le projet les adopte.
- **Hooks** : garde-fous Node.js valables sous Windows et Linux (voir [settings.md](.claude/settings.md)) ; mots-clés français dans [skill-rules.json](.claude/hooks/skill-rules.json).

### Installation

Les skills et agents s'installent **pour l'utilisateur** (disponibles dans tous les projets) ; les hooks, `settings.json` et `CLAUDE.md` s'installent **dans un projet choisi**. Tout élément remplacé est sauvegardé dans `~/.claude/backups/`.

```powershell
# Windows (PowerShell), depuis la racine de ce dépôt
.\installer.ps1                                     # skills + agents pour tous les projets
.\installer.ps1 -Projet C:\xampp\htdocs\MonProjet   # + CLAUDE.md, settings.json et hooks du projet
```

```bash
# Linux, macOS, Git Bash
./installer.sh
./installer.sh --projet /chemin/vers/mon-projet
```

Mise à jour : `git pull` dans ce dépôt, puis relancer le script. Redémarrer Claude Code pour charger les skills. Les hooks exigent Node.js.

---

## Table des matières

- [Adaptation maison](#adaptation-maison)
- [Structure des répertoires](#structure-des-répertoires)
- [Démarrage rapide](#démarrage-rapide)
- [Travailler avec les worktrees](#travailler-avec-les-worktrees)
- [Référence de configuration](#référence-de-configuration)
  - [CLAUDE.md - Mémoire du projet](#claudemd---mémoire-du-projet)
  - [settings.json - Hooks et environnement](#settingsjson---hooks-et-environnement)
  - [Serveurs MCP - Intégrations externes](#serveurs-mcp---intégrations-externes)
  - [Serveurs LSP - Intelligence du code en temps réel](#serveurs-lsp---intelligence-du-code-en-temps-réel)
  - [Hooks d'évaluation des skills](#hooks-dévaluation-des-skills)
  - [Skills - Connaissances métier](#skills---connaissances-métier)
  - [Agents - Assistants spécialisés](#agents---assistants-spécialisés)
- [Workflows GitHub Actions](#workflows-github-actions)
- [Bonnes pratiques](#bonnes-pratiques)
- [Exemples dans ce dépôt](#exemples-dans-ce-dépôt)

---

## Structure des répertoires

```
your-project/
├── CLAUDE.md                      # Mémoire du projet (emplacement alternatif)
├── .mcp.json                      # Configuration des serveurs MCP (JIRA, GitHub, etc.)
├── .claude/
│   ├── settings.json              # Hooks, environnement, permissions
│   ├── settings.local.json        # Surcharges personnelles (ignoré par git)
│   ├── settings.md                # Documentation des hooks lisible par un humain
│   ├── .gitignore                 # Ignore les fichiers locaux/personnels
│   │
│   ├── agents/                    # Agents IA personnalisés
│   │   └── code-reviewer.md       # Agent de revue de code proactif
│   │
│   ├── hooks/                     # Scripts de hooks
│   │   ├── garde-fous.js          # Protection de .env et de main, syntaxe Python, rappels
│   │   ├── skill-eval.sh          # Correspondance des skills à la soumission d'un prompt
│   │   ├── skill-eval.js          # Moteur Node.js de correspondance des skills
│   │   └── skill-rules.json       # Configuration de la correspondance de motifs
│   │
│   ├── skills/                    # Skills de connaissances métier + skills de workflow
│   │   ├── README.md              # Vue d'ensemble des skills
│   │   ├── conventions-django/    # Style maison (prioritaire) + references/
│   │   │   └── SKILL.md
│   │   ├── skill-creator/
│   │   │   └── SKILL.md
│   │   ├── ticket/                # Skills de workflow invocables par l'utilisateur
│   │   │   └── SKILL.md
│   │   ├── pr-review/
│   │   │   └── SKILL.md
│   │   ├── django-extensions/
│   │   │   └── SKILL.md
│   │   ├── systematic-debugging/
│   │   │   └── SKILL.md
│   │   └── ...
│   │
│   └── rules/                     # Instructions modulaires (facultatif)
│       ├── code-style.md
│       └── security.md
│
└── .github/
    └── workflows/
        ├── pr-claude-code-review.yml           # Revue automatique des PR
        ├── scheduled-claude-code-docs-sync.yml # Synchronisation mensuelle de la documentation
        ├── scheduled-claude-code-quality.yml   # Revue qualité hebdomadaire
        └── scheduled-claude-code-dependency-audit.yml
```

---

## Démarrage rapide

### 1. Créez le répertoire `.claude`

```bash
mkdir -p .claude/{agents,hooks,skills}
```

### 2. Ajoutez un fichier CLAUDE.md

Créez `CLAUDE.md` à la racine de votre projet avec les informations clés de votre projet. Consultez [CLAUDE.md](CLAUDE.md) pour un exemple complet.

```markdown
# Nom du projet

## Informations clés
- **Stack** : Django 5.2 LTS, PostgreSQL/PostGIS, JavaScript natif
- **Environnement** : venv à la racine du dépôt, `pip` + `requirements.txt` figé
- **Vérification** : `..\venv\Scripts\python.exe manage.py check` (depuis le sous-dossier du projet)
- **Migrations manquantes** : `..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run`
- **Tests manuels** : requêtes REST Client `<projet>/http/*.http`

## Répertoires clés
- `apps/` - Applications Django
- `config/` - Settings Django et URLconf racine
- `templates/` - Gabarits Django
- `tests/` - Fichiers de test

## Style de code
- Python 3.12+ avec annotations de type obligatoires
- Pas de types `Any` - utilisez des annotations de type appropriées
- Utilisez les retours anticipés, évitez les conditions imbriquées
- Privilégiez les vues basées sur des fonctions
```

### 3. Ajoutez settings.json avec des hooks

Créez `.claude/settings.json`. Consultez [settings.json](.claude/settings.json) pour un exemple complet avec formatage automatique, tests, et plus encore.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "[ \"$(git branch --show-current)\" != \"main\" ] || { echo '{\"block\": true, \"message\": \"Cannot edit on main branch\"}' >&2; exit 2; }",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### 4. Ajoutez votre premier skill

Créez `.claude/skills/your-skill-name/SKILL.md`. Consultez [skill-creator/SKILL.md](.claude/skills/skill-creator/SKILL.md) pour des conseils sur la création de skills efficaces, ou [django-extensions/SKILL.md](.claude/skills/django-extensions/SKILL.md) pour un exemple simple.

```markdown
---
name: your-skill-name
description: Ce que fait ce skill et quand l'utiliser. Incluez les mots-clés que les utilisateurs mentionneraient.
---

# Titre de votre skill

## Quand l'utiliser
- Décrivez quand Claude doit utiliser ce skill
- Incluez des scénarios de déclenchement précis

## Patrons essentiels
- Montrez des exemples et des bonnes pratiques
- Incluez des extraits de code si c'est pertinent
```

> **Astuce :** le champ `description` est essentiel : Claude s'en sert pour décider quand appliquer le skill. Incluez les mots-clés que les utilisateurs mentionneraient naturellement.

---

## Travailler avec les worktrees

Claude Code prend en charge nativement les worktrees, ce qui vous permet d'exécuter Claude dans une copie isolée de votre dépôt. Votre répertoire de travail principal reste ainsi propre pendant que Claude expérimente, implémente des fonctionnalités ou effectue des modifications de grande ampleur.

```bash
claude --worktree   # ou : claude -w
```

Cette commande crée un worktree git temporaire sur une nouvelle branche, y démarre Claude et laisse votre branche actuelle intacte.

### Pourquoi utiliser les worktrees

- **Expérimentation sans risque** — Claude peut effectuer et annuler des modifications librement, sans toucher à votre arbre de travail
- **Travail en parallèle** — exécutez plusieurs sessions Claude sur différentes fonctionnalités simultanément
- **Fusions (merges) propres** — relisez la branche du worktree avant de fusionner quoi que ce soit dans `main`

### Environnement automatique avec direnv

Les worktrees ont besoin du même virtualenv Python et des mêmes variables d'environnement que le dépôt principal — mais ils se trouvent dans un autre répertoire. Notre [`.envrc`](.envrc) gère cela automatiquement grâce à [direnv](https://direnv.net/) :

```bash
# .envrc — fonctionne aussi bien dans le dépôt principal que dans n'importe quel worktree
_main_venv="$(git worktree list --porcelain | awk 'NR==1{print $2}')/.venv"
export VIRTUAL_ENV="$_main_venv"
PATH_add "$_main_venv/bin"

_main_worktree="$(git worktree list --porcelain | awk 'NR==1{print $2}')"
dotenv_if_exists "$_main_worktree/.env"
dotenv_if_exists ".env"
```

Lorsque direnv charge ce fichier dans un worktree, il effectue automatiquement les opérations suivantes :
- Il active le **`.venv` du dépôt principal** — inutile de réinstaller les dépendances pour chaque worktree
- Il charge le **`.env` du dépôt principal** — les secrets et la configuration sont hérités sans copie
- Il charge un `.env` local s'il en existe un dans le worktree (pour les surcharges)

Pour l'activer, installez direnv et raccordez-le à votre shell :

```bash
# macOS
brew install direnv

# Ubuntu/Debian
sudo apt install direnv

# Ajoutez à ~/.zshrc ou ~/.bashrc
eval "$(direnv hook zsh)"   # ou bash
```

Autorisez ensuite le `.envrc` une fois pour toutes à la racine de votre projet :

```bash
direnv allow
```

À partir de là, chaque worktree créé par Claude héritera automatiquement du bon environnement.

### Commit et fusion en retour

Une fois satisfait des modifications d'une session dans un worktree, utilisez le [skill `worktree-commit-merge`](.claude/skills/worktree-commit-merge/SKILL.md) pour commiter le travail et le fusionner dans `main` :

```
Vous : c'est terminé, commite et fusionne dans main
```

Claude va :
1. Commiter toutes les modifications du worktree avec un message de commit conventionnel
2. Fusionner la branche du worktree dans `main`
3. Synchroniser la branche du worktree avec `main`

Le skill se déclenche automatiquement lorsque vous dites par exemple « commite et fusionne dans master/main » ou « on a fini avec ce worktree ».

---

## Référence de configuration

### CLAUDE.md - Mémoire du projet

CLAUDE.md est la mémoire persistante de Claude, chargée automatiquement au démarrage de la session.

**Emplacements (par ordre de priorité) :**
1. `.claude/CLAUDE.md` (projet, dans le dossier .claude)
2. `./CLAUDE.md` (racine du projet)
3. `~/.claude/CLAUDE.md` (niveau utilisateur, tous les projets)

**Ce qu'il faut inclure :**
- La stack du projet et une vue d'ensemble de l'architecture
- Les commandes clés (test, build, lint, déploiement)
- Les règles de style de code
- Les répertoires importants et leur rôle
- Les règles et contraintes critiques

**📄 Exemple :** [CLAUDE.md](CLAUDE.md)

---

### settings.json - Hooks et environnement

Le fichier de configuration principal pour les hooks, les variables d'environnement et les permissions.

**Emplacement :** `.claude/settings.json`

**📄 Exemple :** [settings.json](.claude/settings.json) | [Documentation lisible par un humain](.claude/settings.md)

#### Événements de hook

| Événement | Moment du déclenchement | Cas d'usage |
|-------|---------------|----------|
| `PreToolUse` | Avant l'exécution d'un outil | Bloquer les modifications sur main, valider les commandes |
| `PostToolUse` | Après l'exécution d'un outil | Formatage automatique, exécution des tests, lint |
| `UserPromptSubmit` | L'utilisateur soumet un prompt | Ajouter du contexte, suggérer des skills |
| `Stop` | L'agent a terminé | Décider si Claude doit continuer |

#### Format de réponse des hooks

```json
{
  "block": true,           // Bloque l'action (PreToolUse uniquement)
  "message": "Reason",     // Message affiché à l'utilisateur
  "feedback": "Info",      // Retour non bloquant
  "suppressOutput": true,  // Masque la sortie de la commande
  "continue": false        // Indique s'il faut continuer
}
```

#### Codes de sortie
- `0` - Succès
- `2` - Erreur bloquante (PreToolUse uniquement, bloque l'outil)
- Autre - Erreur non bloquante

---

### Serveurs MCP - Intégrations externes

Les serveurs MCP (Model Context Protocol) permettent à Claude Code de se connecter à des outils externes comme JIRA, GitHub, Slack, des bases de données, et bien d'autres. C'est ainsi que vous rendez possibles des workflows comme « lire un ticket, l'implémenter et mettre à jour le statut du ticket ».

**Emplacement :** `.mcp.json` (racine du projet, commité dans git pour le partage en équipe)

**📄 Exemple :** [.mcp.json](.mcp.json)

#### Fonctionnement de MCP

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Claude Code   │────▶│   Serveur MCP   │────▶│   API externe   │
│                 │◀────│  (pont local)   │◀────│  (JIRA, GitHub) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

Les serveurs MCP s'exécutent localement et fournissent à Claude des outils pour interagir avec des services externes. Lorsque vous configurez un serveur MCP JIRA, Claude obtient des outils comme `jira_get_issue`, `jira_update_issue`, `jira_create_issue`, etc.

#### Format de .mcp.json

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Champs :**

| Champ | Obligatoire | Description |
|-------|----------|-------------|
| `type` | Oui | Type de serveur : `stdio` (processus local) ou `http` (distant) |
| `command` | Pour stdio | Exécutable à lancer (par ex. `npx`, `python`) |
| `args` | Non | Arguments de ligne de commande |
| `env` | Non | Variables d'environnement (prend en charge l'expansion `${VAR}`) |
| `url` | Pour http | URL du serveur distant |
| `headers` | Pour http | En-têtes HTTP pour l'authentification |

#### Exemple : intégration JIRA

```json
{
  "mcpServers": {
    "jira": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-jira"],
      "env": {
        "JIRA_HOST": "${JIRA_HOST}",
        "JIRA_EMAIL": "${JIRA_EMAIL}",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
      }
    }
  }
}
```

**Ce que cela permet :**
- Lire les détails du ticket, les critères d'acceptation et les commentaires
- Mettre à jour le statut du ticket (To Do → In Progress → In Review)
- Ajouter des commentaires pour signaler l'avancement
- Créer de nouveaux tickets pour les bugs trouvés pendant le développement
- Lier les PR aux tickets

**Exemple de workflow avec le [skill `ticket`](.claude/skills/ticket/SKILL.md) :**
```
Vous : /ticket PROJ-123

Claude :
1. Récupération de PROJ-123 depuis JIRA...
   "Ajouter l'envoi d'un avatar sur le profil utilisateur"

2. Lecture des critères d'acceptation...
   - Bouton d'envoi sur la page de profil
   - Prise en charge de JPG/PNG jusqu'à 5 Mo
   - Affichage d'un état de chargement

3. Recherche des fichiers associés dans la base de code...
   Trouvé : apps/users/views.py
   Trouvé : templates/users/profile.html

4. Création de la branche : cw/PROJ-123-avatar-upload

5. [Implémentation de la fonctionnalité...]

6. Passage du statut JIRA à "In Review"
   Ajout du commentaire : "PR #456 prête pour la revue"

7. Création de la PR liée à PROJ-123...
```

#### Configurations courantes de serveurs MCP

**Suivi des tickets :**
```json
{
  "jira": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-jira"],
    "env": {
      "JIRA_HOST": "${JIRA_HOST}",
      "JIRA_EMAIL": "${JIRA_EMAIL}",
      "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
    }
  },
  "linear": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-linear"],
    "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
  }
}
```

**Code et DevOps :**
```json
{
  "github": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-github"],
    "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
  },
  "sentry": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-sentry"],
    "env": {
      "SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}",
      "SENTRY_ORG": "${SENTRY_ORG}"
    }
  }
}
```

**Communication :**
```json
{
  "slack": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-slack"],
    "env": {
      "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
      "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
    }
  }
}
```

**Bases de données :**
Jetez un œil à [postgres-mcp](https://github.com/crystaldba/postgres-mcp).
```json
{
  "postgres": {
    "command": "uv",
    "args": [
      "run",
      "postgres-mcp",
      "--access-mode=unrestricted"
    ],
    "env": {
      "DATABASE_URI": "${DATABASE_URL}"
    }
  }
}
```

#### Variables d'environnement

Les configurations MCP prennent en charge l'expansion de variables :
- `${VAR}` - Est remplacé par la variable d'environnement (échoue si elle n'est pas définie)
- `${VAR:-default}` - Utilise la valeur par défaut si VAR n'est pas définie

Définissez-les dans le profil de votre shell ou dans un fichier `.env` (ne commitez pas de secrets !) :
```bash
export JIRA_HOST="https://yourcompany.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="your-api-token"
```

#### Settings pour MCP

Dans `settings.json`, vous pouvez approuver automatiquement les serveurs MCP :

```json
{
  "enableAllProjectMcpServers": true
}
```

Ou approuver des serveurs précis :
```json
{
  "enabledMcpjsonServers": ["jira", "github", "slack"]
}
```

---

### Serveurs LSP - Intelligence du code en temps réel

LSP (Language Server Protocol) donne à Claude une compréhension en temps réel de votre code : informations de type, erreurs, complétions et navigation. Au lieu de simplement lire du texte, Claude peut « voir » votre code comme le fait votre IDE.

**Pourquoi c'est important :** lorsque vous modifiez du TypeScript, Claude sait immédiatement si vous avez introduit une erreur de type. Lorsque vous faites référence à une fonction, Claude peut aller directement à sa définition. Cela améliore considérablement la qualité du code généré.

#### Activer LSP

La prise en charge de LSP s'active au moyen de plugins dans `settings.json` :

```json
{
  "enabledPlugins": {
    "pyright-lsp@claude-plugins-official": true,
    "typescript-lsp@claude-plugins-official": true
  }
}
```

#### Ce que LSP apporte à Claude

| Fonctionnalité | Description |
|---------|-------------|
| **Diagnostics** | Erreurs et avertissements en temps réel après chaque modification |
| **Informations de type** | Infos au survol, signatures de fonctions, définitions de types |
| **Navigation dans le code** | Aller à la définition, trouver les références |
| **Complétions** | Suggestions de symboles adaptées au contexte |

#### Plugins LSP disponibles

| Plugin | Langage | Binaire à installer au préalable |
|--------|----------|---------------------|
| `pyright-lsp` | Python | `pip install pyright` ou `uv tool install pyright` |
| `typescript-lsp` | TypeScript/JavaScript | `npm install -g typescript-language-server typescript` |
| `rust-lsp` | Rust | `rustup component add rust-analyzer` |

#### Configuration LSP personnalisée

Pour des configurations avancées, créez `.lsp.json` :

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    },
    "initializationOptions": {
      "preferences": {
        "quotePreference": "single"
      }
    }
  }
}
```

#### Dépannage

Si LSP ne fonctionne pas :

1. **Vérifiez que le binaire est installé :**
   ```bash
   which typescript-language-server  # Doit renvoyer un chemin
   ```

2. **Activez la journalisation de débogage :**
   ```bash
   claude --enable-lsp-logging
   ```

3. **Vérifiez l'état du plugin :**
   ```bash
   claude /plugin  # Consultez l'onglet Errors
   ```

4. **Définissez une variable d'environnement :**
   ```bash
   export ENABLE_LSP_TOOL=1
   ```

---

### Hooks d'évaluation des skills

L'une de nos automatisations les plus puissantes est le **système d'évaluation des skills**. Il s'exécute à chaque soumission de prompt et suggère intelligemment les skills que Claude doit activer.

**📄 Fichiers :** [skill-eval.sh](.claude/hooks/skill-eval.sh) | [skill-eval.js](.claude/hooks/skill-eval.js) | [skill-rules.json](.claude/hooks/skill-rules.json)

#### Fonctionnement

Lorsque vous soumettez un prompt, le hook `UserPromptSubmit` déclenche notre moteur d'évaluation des skills :

1. **Analyse du prompt** - Le moteur recherche dans votre prompt :
   - **Mots-clés** : correspondance simple de mots (`test`, `form`, `graphql`, `bug`)
   - **Motifs** : correspondance par expressions régulières (`\btest(?:s|ing)?\b`, `\.stories\.`)
   - **Chemins de fichiers** : extraction des fichiers mentionnés (`src/components/Button.tsx`)
   - **Intention** : détection de ce que vous cherchez à faire (`create.*test`, `fix.*bug`)

2. **Correspondance des répertoires** - Les chemins de fichiers sont associés aux skills pertinents :
   ```json
   {
     "src/components/core": "core-components",
     "src/graphql": "graphql-schema",
     ".github/workflows": "github-actions",
     "src/hooks": "react-ui-patterns"
   }
   ```

3. **Score de confiance** - Chaque type de déclencheur a une valeur en points :
   ```json
   {
     "keyword": 2,
     "keywordPattern": 3,
     "pathPattern": 4,
     "directoryMatch": 5,
     "intentPattern": 4
   }
   ```

4. **Suggestion de skills** - Les skills qui dépassent le seuil de confiance sont suggérés, avec leurs justifications :
   ```
   ACTIVATION DE SKILLS REQUISE

   Chemins de fichiers détectés : .claude/skills/README.md, README.md

   Skills correspondants (classés par pertinence) :
   1. skill-creator (confiance ÉLEVÉE)
      Correspondance : mot-clé "skill", chemin ".claude/skills/"
   2. django-extensions (confiance MOYENNE)
      Correspondance : association de répertoire ".claude/"
   ```

#### Configuration

Les skills sont définis dans [skill-rules.json](.claude/hooks/skill-rules.json) :

```json
{
  "systematic-debugging": {
    "description": "Four-phase debugging methodology with root cause analysis",
    "priority": 9,
    "triggers": {
      "keywords": ["bug", "debug", "fix", "error", "issue", "troubleshoot"],
      "keywordPatterns": ["\\bbug\\b", "\\bdebug\\b", "\\bfix\\b"],
      "pathPatterns": ["**/tests/**", "**/test_*.py"],
      "intentPatterns": [
        "(?:fix|debug|investigate).*(?:bug|issue|error)",
        "(?:why|what).*(?:failing|broken|wrong)"
      ]
    },
    "excludePatterns": []
  }
}
```

#### Ajout à votre projet

1. Copiez les hooks dans votre projet :
   ```bash
   cp -r .claude/hooks/ your-project/.claude/hooks/
   ```

2. Ajoutez le hook à votre `settings.json` :
   ```json
   {
     "hooks": {
       "UserPromptSubmit": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/skill-eval.sh",
               "timeout": 5
             }
           ]
         }
       ]
     }
   }
   ```

3. Personnalisez [skill-rules.json](.claude/hooks/skill-rules.json) avec les skills et les déclencheurs de votre projet.

---

### Skills - Connaissances métier

Les skills sont des documents Markdown qui enseignent à Claude les patrons et les conventions propres au projet.

**Emplacement :** `.claude/skills/{skill-name}/SKILL.md`

**📄 Exemples :**

*Skills de workflow (invocables par l'utilisateur) :*
- [ticket](.claude/skills/ticket/SKILL.md) - Workflow de bout en bout pour les tickets JIRA/Linear
- [onboard](.claude/skills/onboard/SKILL.md) - Exploration approfondie de la tâche et constitution du contexte
- [pr-review](.claude/skills/pr-review/SKILL.md) - Revue de PR avec la liste de vérification du projet
- [pr-summary](.claude/skills/pr-summary/SKILL.md) - Génère la description de la PR à partir du diff de la branche
- [code-quality](.claude/skills/code-quality/SKILL.md) - Exécute ruff, pyright, pytest et rend compte des résultats
- [docs-sync](.claude/skills/docs-sync/SKILL.md) - Vérifie que la documentation correspond au code actuel
- [worktree-commit-merge](.claude/skills/worktree-commit-merge/SKILL.md) - Commite les modifications du worktree et les fusionne dans master/main

*Skills de connaissances métier (déclenchés automatiquement) :*
- [skill-creator](.claude/skills/skill-creator/SKILL.md) - Guide de création de skills efficaces
- [django-extensions](.claude/skills/django-extensions/SKILL.md) - Commandes de gestion de django-extensions
- [systematic-debugging](.claude/skills/systematic-debugging/SKILL.md) - Méthodologie de débogage en quatre phases
- [pytest-django-patterns](.claude/skills/pytest-django-patterns/SKILL.md) - pytest-django, Factory Boy, fixtures, TDD
- [django-models](.claude/skills/django-models/SKILL.md) - Conception des modèles, optimisation des QuerySet, migrations
- [django-forms](.claude/skills/django-forms/SKILL.md) - Gestion des formulaires, validation, patterns ModelForm
- [django-templates](.claude/skills/django-templates/SKILL.md) - Héritage de gabarits, balises, filtres
- [htmx-patterns](.claude/skills/htmx-patterns/SKILL.md) - Attributs HTMX, interface dynamique
- [celery-patterns](.claude/skills/celery-patterns/SKILL.md) - Tâches Celery, stratégies de nouvelle tentative

#### Champs du frontmatter de SKILL.md

| Champ | Obligatoire | Longueur max. | Description |
|-------|----------|------------|-------------|
| `name` | **Oui** | 64 caractères | Lettres minuscules, chiffres et tirets uniquement. Doit correspondre au nom du répertoire. |
| `description` | **Oui** | 1024 caractères | Ce que fait le skill et quand l'utiliser. Claude s'en sert pour décider quand appliquer le skill. Incluez des mots-clés déclencheurs et des exemples d'invocation par l'utilisateur. |

#### Format de SKILL.md

````markdown
---
name: skill-name
description: Ce que fait ce skill et quand l'utiliser. Incluez les mots-clés que les utilisateurs mentionneraient.
---

# Titre du skill

## Quand l'utiliser
- Condition de déclenchement 1
- Condition de déclenchement 2

## Patrons essentiels

### Nom du patron
```python
# Exemple de code
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
```

## Anti-patrons

### Ce qu'il ne faut PAS faire
```python
# Mauvais exemple - requête N+1
for user in User.objects.all():
    print(user.profile.bio)  # Une requête par utilisateur !
```

## Intégration
- Skill associé : `other-skill`
```

#### Bonnes pratiques pour les skills

1. **Gardez SKILL.md ciblé** - Moins de 500 lignes ; placez la documentation détaillée dans des fichiers séparés et référencés
2. **Rédigez des descriptions riches en déclencheurs** - Claude effectue une correspondance sémantique sur les descriptions pour décider quand appliquer les skills
3. **Incluez des exemples** - Montrez avec du code les bons comme les mauvais patrons
4. **Faites référence à d'autres skills** - Montrez comment les skills fonctionnent ensemble
5. **Utilisez le nom de fichier exact** - Il doit s'agir de `SKILL.md` (sensible à la casse)
````
---

### Agents - Assistants spécialisés

Les agents sont des assistants IA dotés d'un objectif ciblé et de leurs propres prompts.

**Emplacement :** `.claude/agents/{agent-name}.md`

**📄 Exemples :**
- [code-reviewer.md](.claude/agents/code-reviewer.md) - Revue de code complète avec liste de vérification
- [github-workflow.md](.claude/agents/github-workflow.md) - Commits Git, branches, PR

#### Format d'un agent

```markdown
---
name: code-reviewer
description: Relit le code pour en vérifier la qualité, la sécurité et le respect des conventions. À utiliser après avoir écrit ou modifié du code.
model: opus
---

# Prompt système de l'agent

Vous êtes un relecteur de code senior...

## Votre processus
1. Exécutez `git diff` pour voir les modifications
2. Appliquez la liste de vérification de la revue
3. Formulez vos retours

## Liste de vérification
- [ ] Aucun type Python `Any`
- [ ] Gestion correcte des erreurs (pas d'exceptions silencieuses)
- [ ] Optimisation des QuerySet (select_related/prefetch_related)
- [ ] Tests inclus
```

#### Champs de configuration d'un agent

| Champ | Obligatoire | Description |
|-------|----------|-------------|
| `name` | Oui | Minuscules avec tirets |
| `description` | Oui | Quand/pourquoi l'utiliser (1024 caractères max.) |
| `model` | Non | `sonnet`, `opus` ou `haiku` |
| `tools` | Non | Liste d'outils séparés par des virgules |

---

---

## Workflows GitHub Actions

Automatisez la revue de code, les contrôles qualité et la maintenance avec Claude Code.

**📄 Exemples :**
- [pr-claude-code-review.yml](.github/workflows/pr-claude-code-review.yml) - Revue automatique des PR
- [scheduled-claude-code-docs-sync.yml](.github/workflows/scheduled-claude-code-docs-sync.yml) - Synchronisation mensuelle de la documentation
- [scheduled-claude-code-quality.yml](.github/workflows/scheduled-claude-code-quality.yml) - Revue qualité hebdomadaire
- [scheduled-claude-code-dependency-audit.yml](.github/workflows/scheduled-claude-code-dependency-audit.yml) - Mises à jour bimensuelles des dépendances

### Revue de code des PR

Relit automatiquement les PR et répond aux mentions `@claude`.

```yaml
name: PR - Claude Code Review
on:
  pull_request:
    types: [opened, synchronize, reopened]
  issue_comment:
    types: [created]

jobs:
  review:
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' &&
       github.event.issue.pull_request &&
       contains(github.event.comment.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: anthropics/claude-code-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-opus-4-5-20251101
          prompt: |
            Review this PR using .claude/agents/code-reviewer.md standards.
            Run `git diff origin/main...HEAD` to see changes.
```

### Workflows planifiés

| Workflow | Planification | Objectif |
|----------|----------|---------|
| [Qualité du code](.github/workflows/scheduled-claude-code-quality.yml) | Hebdomadaire (dimanche) | Passe en revue des répertoires choisis au hasard, corrige automatiquement les problèmes |
| [Synchronisation de la documentation](.github/workflows/scheduled-claude-code-docs-sync.yml) | Mensuel (le 1er) | Garantit que la documentation reste alignée sur les modifications du code |
| [Audit des dépendances](.github/workflows/scheduled-claude-code-dependency-audit.yml) | Bimensuel (le 1er et le 15) | Mises à jour sûres des dépendances, avec tests |

### Configuration requise

Ajoutez `ANTHROPIC_API_KEY` aux secrets de votre dépôt :
- Settings → Secrets and variables → Actions → New repository secret

### Estimation des coûts

| Workflow | Fréquence | Coût estimé |
|----------|-----------|-----------|
| Revue de PR | Par PR | ~0,05 $ - 0,50 $ |
| Synchronisation de la documentation | Mensuelle | ~0,50 $ - 2,00 $ |
| Audit des dépendances | Bimensuelle | ~0,20 $ - 1,00 $ |
| Qualité du code | Hebdomadaire | ~1,00 $ - 5,00 $ |

**Total mensuel estimé :** ~10 $ - 50 $ (selon le volume de PR)

---

## Bonnes pratiques

### 1. Commencez par CLAUDE.md

Votre `CLAUDE.md` est la base de tout. Incluez-y :
- Une vue d'ensemble de la stack
- Les commandes clés
- Les règles critiques
- La structure des répertoires

### 2. Construisez vos skills progressivement

N'essayez pas de tout documenter d'un coup :
1. Commencez par vos patrons les plus courants
2. Ajoutez des skills au fur et à mesure que des points de friction apparaissent
3. Concentrez chaque skill sur un seul domaine

### 3. Utilisez les hooks pour l'automatisation

Laissez les hooks gérer les tâches répétitives :
- Formatage automatique à l'enregistrement
- Exécution des tests quand des fichiers de test changent
- Régénération des types quand les schémas changent
- Blocage des modifications sur les branches protégées

### 4. Créez des agents pour les workflows complexes

Les agents sont parfaits pour :
- La revue de code (avec la liste de vérification de votre équipe)
- La création et la gestion des PR
- Les workflows de débogage
- La prise en main de nouvelles tâches

### 5. Tirez parti de GitHub Actions

Automatisez la maintenance :
- Revue de chaque PR
- Passes qualité hebdomadaires
- Alignement mensuel de la documentation
- Mises à jour des dépendances

### 6. Versionnez votre configuration

Commitez tout, sauf :
- `settings.local.json` (préférences personnelles)
- `CLAUDE.local.md` (notes personnelles)
- Les identifiants propres à chaque utilisateur

---

## Exemples dans ce dépôt

| Fichier | Description |
|------|-------------|
| [CLAUDE.md](CLAUDE.md) | Exemple de fichier de mémoire du projet |
| [.claude/settings.json](.claude/settings.json) | Configuration complète des hooks |
| [.claude/settings.md](.claude/settings.md) | Documentation des hooks lisible par un humain |
| [.mcp.json](.mcp.json) | Configuration des serveurs MCP (JIRA, GitHub, Slack, etc.) |
| **Agents** | |
| [.claude/agents/code-reviewer.md](.claude/agents/code-reviewer.md) | Agent de revue de code complète |
| [.claude/agents/github-workflow.md](.claude/agents/github-workflow.md) | Agent de workflow Git |
| **Hooks** | |
| [.claude/hooks/skill-eval.sh](.claude/hooks/skill-eval.sh) | Script d'enveloppe de l'évaluation des skills |
| [.claude/hooks/skill-eval.js](.claude/hooks/skill-eval.js) | Moteur Node.js de correspondance des skills |
| [.claude/hooks/skill-rules.json](.claude/hooks/skill-rules.json) | Règles de correspondance de motifs |
| **Skills (workflow)** | |
| [.claude/skills/ticket/SKILL.md](.claude/skills/ticket/SKILL.md) | **Workflow des tickets JIRA/Linear (lecture → implémentation → mise à jour)** |
| [.claude/skills/onboard/SKILL.md](.claude/skills/onboard/SKILL.md) | Exploration approfondie de la tâche et constitution du contexte |
| [.claude/skills/pr-review/SKILL.md](.claude/skills/pr-review/SKILL.md) | Revue de PR avec la liste de vérification du projet |
| [.claude/skills/pr-summary/SKILL.md](.claude/skills/pr-summary/SKILL.md) | Génère la description de la PR à partir du diff de la branche |
| [.claude/skills/code-quality/SKILL.md](.claude/skills/code-quality/SKILL.md) | Exécute ruff, pyright, pytest et rend compte des résultats |
| [.claude/skills/docs-sync/SKILL.md](.claude/skills/docs-sync/SKILL.md) | Vérifie que la documentation correspond au code actuel |
| [.claude/skills/worktree-commit-merge/SKILL.md](.claude/skills/worktree-commit-merge/SKILL.md) | Commite les modifications du worktree et les fusionne dans master/main |
| **Skills (connaissances métier)** | |
| [.claude/skills/skill-creator/SKILL.md](.claude/skills/skill-creator/SKILL.md) | Guide de création de skills efficaces |
| [.claude/skills/django-extensions/SKILL.md](.claude/skills/django-extensions/SKILL.md) | Commandes de gestion de django-extensions |
| [.claude/skills/systematic-debugging/SKILL.md](.claude/skills/systematic-debugging/SKILL.md) | Méthodologie de débogage en quatre phases |
| [.claude/skills/pytest-django-patterns/SKILL.md](.claude/skills/pytest-django-patterns/SKILL.md) | pytest-django, Factory Boy, fixtures, TDD |
| [.claude/skills/django-models/SKILL.md](.claude/skills/django-models/SKILL.md) | Conception des modèles, optimisation des QuerySet |
| [.claude/skills/django-forms/SKILL.md](.claude/skills/django-forms/SKILL.md) | Gestion des formulaires, validation |
| [.claude/skills/django-templates/SKILL.md](.claude/skills/django-templates/SKILL.md) | Héritage de gabarits, balises, filtres |
| [.claude/skills/htmx-patterns/SKILL.md](.claude/skills/htmx-patterns/SKILL.md) | Attributs HTMX, interface dynamique |
| [.claude/skills/celery-patterns/SKILL.md](.claude/skills/celery-patterns/SKILL.md) | Tâches Celery, stratégies de nouvelle tentative |
| **Workflows GitHub** | |
| [.github/workflows/pr-claude-code-review.yml](.github/workflows/pr-claude-code-review.yml) | Revue automatique des PR |
| [.github/workflows/scheduled-claude-code-docs-sync.yml](.github/workflows/scheduled-claude-code-docs-sync.yml) | Synchronisation mensuelle de la documentation |
| [.github/workflows/scheduled-claude-code-quality.yml](.github/workflows/scheduled-claude-code-quality.yml) | Revue qualité hebdomadaire |
| [.github/workflows/scheduled-claude-code-dependency-audit.yml](.github/workflows/scheduled-claude-code-dependency-audit.yml) | Audit bimensuel des dépendances |

---

## Pour aller plus loin

- [Documentation de Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Action](https://github.com/anthropics/claude-code-action) - GitHub Action
- [API Anthropic](https://docs.anthropic.com/en/api)

---

## Licence

MIT - Utilisez ce dépôt comme modèle pour vos propres projets.
