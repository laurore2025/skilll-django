---
name: worktree-commit-merge
description: "Commite les modifications du worktree, les fusionne (merge) dans master/main, puis synchronise la branche du worktree avec master. À déclencher lorsque l'utilisateur dit par exemple « commit et merge sur master », « on a fini avec ce worktree, commit et merge », ou toute formulation similaire. N'attendez pas que l'utilisateur prononce explicitement le mot « worktree » — s'il y a des modifications et qu'il parle de fusionner dans master/main, utilisez ce skill."
---

## Vue d'ensemble

Vous êtes dans un worktree git, sur une branche de fonctionnalité qui contient des modifications non commitées. Ce skill :
1. Commite ces modifications sur la branche courante
2. Fusionne la branche dans master/main — en fast-forward si possible, sinon par un commit de fusion classique

## Étape 1 : rassemblez le contexte

Exécutez ces commandes en parallèle :

```bash
git status
git diff HEAD
git branch --show-current
git worktree list
git log --oneline -10
```

Vous obtenez ainsi :
- Les fichiers modifiés, et ce qui est indexé ou non indexé
- Le nom de la branche courante (la branche du worktree)
- Le chemin du worktree principal et la branche qui y est extraite
- Le style des commits récents, pour que votre message s'accorde avec le projet

## Étape 2 : commitez les modifications

Indexez des fichiers précis plutôt que d'utiliser `git add -A`, qui peut inclure accidentellement des fichiers non souhaités comme `.env` ou des artefacts de build :

```bash
git add <specific relevant files>
```

Rédigez un message de commit en français qui suit le style du journal récent — dans les projets maison,
« Sujet : précisions, précisions » (voir le skill `conventions-django`). Passez-le toujours via un heredoc
pour préserver la mise en forme. **N'ajoutez aucune ligne d'attribution** (pas de `Co-Authored-By`,
pas de « Generated with Claude Code ») :

```bash
git commit -m "$(cat <<'EOF'
<Sujet> : <précisions>

<détails éventuels, une ligne par changement>
EOF
)"
```

## Étape 3 : identifiez la cible de la fusion

Dans la sortie de `git worktree list`, la **première entrée est toujours le worktree principal**. Identifiez :
- `MAIN_PATH` — chemin du worktree principal dans le système de fichiers
- `MAIN_BRANCH` — branche extraite à cet endroit (généralement `master` ou `main`)
- `CURRENT_BRANCH` — la branche sur laquelle vous venez de commiter

## Étape 4 : fusionnez dans master/main

Essayez d'abord le fast-forward. Si les historiques ont divergé, rabattez-vous sur un commit de fusion classique :

```bash
git -C <MAIN_PATH> merge --ff-only <CURRENT_BRANCH> \
  || git -C <MAIN_PATH> merge <CURRENT_BRANCH> --no-edit
```

Indiquez à l'utilisateur quelle voie a été suivie — fast-forward ou commit de fusion — pour qu'il sache ce qu'il est advenu de l'historique.

## Étape 5 : synchronisez la branche du worktree avec master/main

Après la fusion, mettez à jour la branche du worktree pour qu'elle inclue les commits qui se trouvaient déjà sur master/main (par ex. issus d'autres fusions) :

```bash
git merge <MAIN_BRANCH>
```

Cette commande s'exécute dans le répertoire du worktree (le répertoire courant) et y récupère l'état complet de master/main.

## Étape 6 : confirmez

```bash
git -C <MAIN_PATH> log --oneline -5
```

Indiquez ce qui a été commité (fichiers + message), comment la fusion a été effectuée, et que la branche du worktree est désormais synchronisée avec master/main.

**Ne poussez pas** (`git push`) sauf demande explicite de l'utilisateur : donnez-lui plutôt la commande à lancer.
