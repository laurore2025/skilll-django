#!/bin/bash
# Hook d'évaluation des skills v2.0
# Script d'enveloppe qui délègue au moteur d'évaluation Node.js
#
# Ce hook s'exécute sur UserPromptSubmit et analyse le prompt pour repérer :
# - les mots-clés et motifs indiquant qu'un skill est pertinent ;
# - les chemins de fichiers mentionnés dans le prompt ;
# - les motifs d'intention (ce que l'utilisateur veut faire) ;
# - les associations de répertoires (quels répertoires correspondent à quels skills).
#
# La configuration se trouve dans skill-rules.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_SCRIPT="$SCRIPT_DIR/skill-eval.js"

# Vérifier que Node.js est disponible
if ! command -v node &>/dev/null; then
  # Repli : sortie silencieuse si Node.js est introuvable
  exit 0
fi

# Vérifier que le script Node existe
if [[ ! -f "$NODE_SCRIPT" ]]; then
  exit 0
fi

# Transmettre l'entrée standard au script Node.js (en masquant le bruit stderr de nvm / de l'initialisation du shell)
cat | node "$NODE_SCRIPT" 2>/dev/null

# Toujours sortir avec 0 pour laisser passer le prompt
exit 0
