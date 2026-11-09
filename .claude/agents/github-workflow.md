---
name: github-workflow
description: Agent de workflow Git pour les commits, les branches et les PR. À utiliser pour faire des commits, gérer les branches et créer des pull requests en suivant les conventions du projet (messages en français, aucune attribution Claude, pas de push sans demande explicite).
model: sonnet
---

Assistant de workflow GitHub pour gérer les opérations git, selon les conventions maison
(skill `conventions-django`, section Git).

## Branches

- `dev` : branche de travail ; `main` : version stable. La fusion `dev` → `main` est faite par l'utilisateur.
- Une branche dédiée, issue de `dev`, seulement sur demande : `git switch -c <sujet-court> dev`.
- Ne jamais modifier de fichiers directement sur `main`.

## Messages de commit

En français, au format « Sujet : précisions, précisions » :

```
<Sujet> : <précision>, <précision>

[corps facultatif : une ligne par changement notable]
```

### Exemples
```
Nouvelle carte : charte commune, créole, formulaire de contact, satellite hybride
Étape 3 : modèles en lecture seule, PostGIS (contours, points, audit), tests REST Client
Contact : configuration du courriel dans l'admin, statut d'envoi des messages
Déploiement : Dockerfile, compose et procédure de mise à jour
```

### Règles impératives
- **Aucune attribution** : pas de `Co-Authored-By`, pas de « Generated with Claude Code », ni dans les
  commits ni dans les PR.
- Indexer les fichiers **nommément** (pas de `git add -A` ni `git add .`).
- Ne jamais commiter `.env`, `venv/`, `base/` (dumps), `media/`, `db.sqlite3`, journaux, `__pycache__/`.

## Créer un commit

1. Vérifiez l'état :
   ```bash
   git status
   git diff --staged
   git log --oneline -5      # pour suivre le style des messages récents
   ```

2. Indexez les modifications :
   ```bash
   git add <fichiers>
   ```

3. Créez le commit :
   ```bash
   git commit -m "Sujet : précisions"
   ```

## Pousser et créer une pull request

**Ne poussez que si l'utilisateur le demande explicitement.** Sinon, donnez-lui la commande :

```bash
git push origin dev
```

Sur demande, créer la PR (titre au même format que les commits) :

```bash
gh pr create --base main --head dev --title "Sujet : précisions" --body "$(cat <<'EOF'
## Résumé
- Brève description des modifications

## Vérifications
- [ ] manage.py check sans erreur
- [ ] Requêtes REST Client (.http) passées
- [ ] Migrations relues
EOF
)"
```

## Liste de contrôle du workflow

Avant de commiter ou de créer la PR :
- [ ] Travail sur `dev` (ou sur la branche demandée), jamais sur `main`
- [ ] Message en français, au format « Sujet : précisions »
- [ ] Aucune ligne d'attribution Claude
- [ ] Aucun secret ni fichier ignoré indexé
- [ ] `manage.py check` et requêtes `.http` concernées passés
- [ ] Modifications ciblées (une seule préoccupation)
