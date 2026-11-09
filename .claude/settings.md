# Documentation des settings de Claude Code

Configuration adaptée aux projets Django maison (venv + pip, PostgreSQL/PostGIS, français).
Les hooks Node.js fonctionnent sous Windows (Git Bash) comme sous Linux : **Node.js doit être installé**.

## Attribution

- `includeCoAuthoredBy` : `false` et `attribution` : `{"commit": "", "pr": ""}` — aucune mention de Claude
  dans les commits ni dans les pull requests (`includeCoAuthoredBy` est conservé pour les anciennes
  versions de Claude Code).

## Variables d'environnement

- `INSIDE_CLAUDE_CODE` : "1" — indique que le code s'exécute dans Claude Code
- `BASH_DEFAULT_TIMEOUT_MS` : "420000" — délai par défaut des commandes bash (7 minutes)
- `BASH_MAX_TIMEOUT_MS` : "420000" — délai maximal des commandes bash (7 minutes)

## Hooks

Tous les garde-fous sont dans `.claude/hooks/garde-fous.js` (un mode par usage). L'événement arrive en
JSON sur l'entrée standard ; une erreur interne du script laisse toujours passer l'action.

### UserPromptSubmit

- **Évaluation des skills** : analyse le prompt (mots-clés français et anglais, chemins, intentions) et
  suggère les skills pertinents
  - **Script** : `.claude/hooks/skill-eval.sh` → `skill-eval.js`, règles dans `skill-rules.json`
  - **Délai** : 5 s

### PreToolUse

1. **Protection du fichier `.env`** (`garde-fous.js env`) — outils Read, Edit, MultiEdit, Write,
   NotebookEdit, Bash, PowerShell
   - Bloque la lecture, la modification et l'affichage de `.env` (`cat`, `type`, `Get-Content`…)
   - `.env.example` reste modifiable ; lister les seuls noms de variables reste possible
2. **Protection de la branche main** (`garde-fous.js main`) — outils Edit, MultiEdit, Write
   - Bloque toute modification sur `main` ou `master` : travailler sur `dev`

### PostToolUse

1. **Syntaxe Python** (`garde-fous.js python`) — après modification d'un fichier `.py`
   - Analyse le fichier avec le Python du venv du projet (`venv/Scripts/python.exe` ou `venv/bin/python`),
     sans l'importer ni écrire de `.pyc` ; signale l'erreur à Claude
2. **Gabarit modifié** (`garde-fous.js gabarit`) — après modification d'un `templates/**/*.html`
   - Rappelle de redémarrer le serveur de vérification lancé avec `--noreload` et de contrôler les
     traductions (`data-i18n`)
3. **Dépendances** (`garde-fous.js dependances`) — après modification d'un `requirements*.txt`
   - Rappelle de figer les versions et de proposer la mise à jour du venv (aucune installation automatique)

## Format de sortie des hooks

- Code `2` + message sur stderr : action bloquée (PreToolUse) ou erreur signalée à Claude (PostToolUse)
- Code `0` + JSON `{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "…"}}` :
  information ajoutée au contexte de Claude
- Code `0` sans sortie : rien à signaler

## Variables d'environnement dans les hooks

- `$CLAUDE_PROJECT_DIR` : répertoire racine du projet
- Le détail de l'outil appelé (`tool_name`, `tool_input.file_path`, `tool_input.command`) est lu dans le
  JSON reçu sur l'entrée standard

## Tester un hook à la main

```bash
node -e "process.stdout.write(JSON.stringify({tool_name:'Read',tool_input:{file_path:'C:\\\\projet\\\\.env'}}))" \
  | node .claude/hooks/garde-fous.js env; echo "code=$?"     # attendu : message de refus, code=2
```
