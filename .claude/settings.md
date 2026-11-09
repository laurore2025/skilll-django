# Documentation des settings de Claude Code

## Variables d'environnement

- `INSIDE_CLAUDE_CODE` : "1" — indique que le code s'exécute dans Claude Code
- `BASH_DEFAULT_TIMEOUT_MS` : "420000" — délai par défaut des commandes bash (7 minutes)
- `BASH_MAX_TIMEOUT_MS` : "420000" — délai maximal des commandes bash (7 minutes)

## Hooks

### UserPromptSubmit

- **Évaluation des skills** : analyse les prompts et suggère les skills pertinents
  - **Script** : `.claude/hooks/skill-eval.sh`
  - **Comportement** : rapproche mots-clés, chemins de fichiers et motifs pour suggérer des skills
  - **Délai** : 5 s

### PreToolUse

- **Protection de la branche main** : empêche les modifications sur la branche main (délai de 5 s)
  - **Déclencheurs** : avant la modification de fichiers avec les outils Edit, MultiEdit ou Write
  - **Comportement** : bloque la modification sur la branche main et suggère de créer une branche de travail

### PostToolUse

1. **Formatage Ruff** : formate automatiquement les fichiers Python (délai de 30 s)
   - **Déclencheurs** : après la modification de fichiers `.py`
   - **Commande** : `uv run ruff format`
   - **Comportement** : formate le code, masque la sortie en cas de succès, affiche un retour en cas d'échec

2. **Installation des dépendances** : installation automatique après un changement de dépendances (délai de 60 s)
   - **Déclencheurs** : après la modification de `pyproject.toml` ou de fichiers `requirements*.txt`
   - **Commande** : `uv sync`
   - **Comportement** : installe les dépendances, masque la sortie en cas de succès, affiche un retour en cas d'échec

3. **Exécution des tests** : lance les tests après la modification d'un fichier de test (délai de 90 s)
   - **Déclencheurs** : après la modification de fichiers `test_*.py`, `*_test.py` ou `*/tests/*.py`
   - **Commande** : `uv run pytest <fichier> -x -q`
   - **Comportement** : lance les tests du fichier modifié, affiche les 30 dernières lignes de sortie, non bloquant

4. **Vérification des types Pyright** : vérifie les types des fichiers Python (délai de 30 s)
   - **Déclencheurs** : après la modification de fichiers `.py`
   - **Commande** : `uv run pyright`
   - **Comportement** : n'affiche que les 20 premières lignes d'erreurs, non bloquant, code de sortie 0

5. **Lint Ruff** : analyse les fichiers Python (délai de 30 s)
   - **Déclencheurs** : après la modification de fichiers `.py`
   - **Commande** : `uv run ruff check`
   - **Comportement** : n'affiche que les 20 premières lignes de problèmes, non bloquant, code de sortie 0

## Format de réponse des hooks

```json
{
  "feedback": "Message à afficher",
  "suppressOutput": true,
  "block": true,
  "continue": false
}
```

## Variables d'environnement dans les hooks

- `$CLAUDE_TOOL_INPUT_FILE_PATH` : fichier en cours de modification
- `$CLAUDE_TOOL_NAME` : outil utilisé
- `$CLAUDE_PROJECT_DIR` : répertoire racine du projet

## Codes de sortie

- `0` : succès
- `1` : erreur non bloquante (affiche un retour)
- `2` : erreur bloquante (PreToolUse uniquement — bloque l'action)
