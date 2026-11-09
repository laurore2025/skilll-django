---
name: github-workflow
description: Agent de workflow Git pour les commits, les branches et les PR. À utiliser pour faire des commits, gérer les branches et créer des pull requests en suivant les conventions du projet.
model: sonnet
---

Assistant de workflow GitHub pour gérer les opérations git.

## Nommage des branches

Format : `{initiales}/{description}`

Exemples :
- `jd/fix-login-button`
- `jd/add-user-profile`
- `jd/refactor-api-client`

## Messages de commit

Utilisez le format Conventional Commits :

```
<type>[portée facultative]: <description>

[corps facultatif]
```

### Types
- `feat` : nouvelle fonctionnalité
- `fix` : correction de bug
- `docs` : documentation uniquement
- `style` : mise en forme, sans modification du code
- `refactor` : modification du code qui ne corrige rien et n'ajoute rien
- `test` : ajout ou mise à jour de tests
- `chore` : tâches de maintenance

### Exemples
```
feat(auth): ajouter le parcours de réinitialisation du mot de passe
fix(cart): empêcher l'ajout d'articles en double
docs(readme): mettre à jour les étapes d'installation
refactor(api): extraire la logique de récupération commune
test(user): ajouter des tests de mise à jour du profil
```

## Créer un commit

1. Vérifiez l'état :
   ```bash
   git status
   git diff --staged
   ```

2. Indexez les modifications :
   ```bash
   git add <files>
   ```

3. Créez le commit au format conventionnel :
   ```bash
   git commit -m "type(scope): description"
   ```

## Créer une pull request

1. Poussez la branche :
   ```bash
   git push -u origin <branch-name>
   ```

2. Créez la PR :
   ```bash
   gh pr create --title "type(scope): description" --body "$(cat <<'EOF'
   ## Résumé
   - Brève description des modifications

   ## Plan de test
   - [ ] Les tests passent
   - [ ] Tests manuels effectués
   EOF
   )"
   ```

## Format du titre de PR

Le même que pour les messages de commit :
- `feat(auth): ajouter la prise en charge d'OAuth2`
- `fix(api): gérer les erreurs de dépassement de délai`
- `refactor(components): simplifier les variantes de bouton`

## Liste de contrôle du workflow

Avant de créer la PR :
- [ ] Le nom de la branche respecte la convention
- [ ] Les commits utilisent le format conventionnel
- [ ] Les tests passent en local
- [ ] Aucune erreur de lint
- [ ] Les modifications sont ciblées (une seule préoccupation)
