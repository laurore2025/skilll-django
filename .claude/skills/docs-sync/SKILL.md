---
name: docs-sync
description: "Vérifie que la documentation est synchronisée avec le code. À utiliser lorsque l'utilisateur veut s'assurer que la documentation correspond au code actuel, repérer la documentation obsolète ou auditer l'exactitude de la documentation. Se déclenche sur des demandes comme « vérifie la doc », « synchronise la documentation », « la doc est-elle à jour ? », « /docs-sync »."
---

# Synchronisation de la documentation

Vérifiez que la documentation correspond à l'état actuel du code.

## Instructions

1. **Trouvez les modifications récentes du code** :
   ```bash
   git log --since="30 days ago" --name-only --pretty=format: -- "*.py" "*.ts" "*.tsx" | sort -u
   ```

2. **Trouvez la documentation associée** :
   - Cherchez dans `/docs/` les fichiers qui mentionnent le code modifié
   - Vérifiez les fichiers README proches du code modifié
   - Repérez les docstrings dans les fichiers modifiés

3. **Vérifiez l'exactitude de la documentation** :
   - Les exemples de code fonctionnent-ils toujours ?
   - Les signatures d'API sont-elles correctes ?
   - Les types de champs sont-ils à jour ?

4. **Ne signalez que les problèmes réels** :
   - Signalez uniquement ce qui est FAUX, pas ce qui manque
   - Ne suggérez pas de documentation pour le simple plaisir de documenter

5. **Produisez une liste de vérification** de la documentation à mettre à jour
