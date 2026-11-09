#!/usr/bin/env bash
# Installe la configuration Claude Code de ce dépôt (Linux, macOS, Git Bash).
#
# Usage (depuis la racine du dépôt) :
#   ./installer.sh                              # skills + agents pour l'utilisateur (tous les projets)
#   ./installer.sh --projet /opt/mon-projet     # en plus : CLAUDE.md, settings et hooks du projet
#   ./installer.sh --projet /opt/mon-projet --force   # remplace CLAUDE.md et settings.json existants
#   ./installer.sh --sans-utilisateur --projet /opt/mon-projet
#
# Les skills et agents installés pour l'utilisateur sont disponibles dans tous les projets.
# Les hooks et settings ne sont installés que dans un projet choisi.
# Tout élément remplacé est d'abord sauvegardé dans ~/.claude/backups/skilll-django-<date>/.
set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_SOURCE="$SOURCE/.claude"
CLAUDE_UTILISATEUR="$HOME/.claude"
SAUVEGARDE="$CLAUDE_UTILISATEUR/backups/skilll-django-$(date +%Y%m%d-%H%M%S)"
PROJET=""
FORCE=0
UTILISATEUR=1

while [ $# -gt 0 ]; do
  case "$1" in
    --projet) PROJET="${2:?--projet attend un chemin}"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --sans-utilisateur) UTILISATEUR=0; shift ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "Option inconnue : $1" >&2; exit 1 ;;
  esac
done

[ -d "$CLAUDE_SOURCE/skills" ] || { echo "Dossier .claude/skills introuvable : lancer depuis la racine du dépôt." >&2; exit 1; }

sauvegarder() {  # sauvegarder <chemin> <sous-dossier>
  if [ -e "$1" ]; then
    mkdir -p "$SAUVEGARDE/$2"
    cp -R "$1" "$SAUVEGARDE/$2/"
    rm -rf "$1"
  fi
}

# --- 1. Skills et agents pour l'utilisateur
if [ "$UTILISATEUR" -eq 1 ]; then
  mkdir -p "$CLAUDE_UTILISATEUR/skills" "$CLAUDE_UTILISATEUR/agents"
  installes=()
  for dossier in "$CLAUDE_SOURCE"/skills/*/; do
    nom="$(basename "$dossier")"
    sauvegarder "$CLAUDE_UTILISATEUR/skills/$nom" skills
    cp -R "$dossier" "$CLAUDE_UTILISATEUR/skills/$nom"
    installes+=("$nom")
  done
  echo "Skills installés dans $CLAUDE_UTILISATEUR/skills : ${installes[*]}"
  for agent in "$CLAUDE_SOURCE"/agents/*.md; do
    sauvegarder "$CLAUDE_UTILISATEUR/agents/$(basename "$agent")" agents
    cp "$agent" "$CLAUDE_UTILISATEUR/agents/"
  done
  echo "Agents installés dans $CLAUDE_UTILISATEUR/agents"
fi

# --- 2. Configuration d'un projet Django (facultatif)
if [ -n "$PROJET" ]; then
  [ -d "$PROJET" ] || { echo "Projet introuvable : $PROJET" >&2; exit 1; }
  mkdir -p "$PROJET/.claude/hooks"
  for paire in "$SOURCE/CLAUDE.md:$PROJET/CLAUDE.md" "$CLAUDE_SOURCE/settings.json:$PROJET/.claude/settings.json"; do
    de="${paire%%:*}"; vers="${paire#*:}"
    if [ -e "$vers" ] && [ "$FORCE" -eq 0 ]; then
      echo "Conservé (déjà présent, --force pour remplacer) : $vers"
      continue
    fi
    sauvegarder "$vers" projet
    cp "$de" "$vers"
    echo "Copié : $vers"
  done
  cp "$CLAUDE_SOURCE"/hooks/* "$PROJET/.claude/hooks/"
  chmod +x "$PROJET/.claude/hooks/"*.sh "$PROJET/.claude/hooks/"*.js 2>/dev/null || true
  cp "$CLAUDE_SOURCE/settings.md" "$PROJET/.claude/"
  echo "Hooks copiés dans $PROJET/.claude/hooks"
  echo
  echo "À faire dans le projet : adapter CLAUDE.md (nom du projet, sous-dossier Django, commandes) et vérifier que Node.js est installé."
fi

[ -d "$SAUVEGARDE" ] && echo "Éléments remplacés sauvegardés dans : $SAUVEGARDE"
echo "Terminé. Redémarrer Claude Code pour charger les nouveaux skills."
