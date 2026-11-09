# Traduction française : fichier modifié par rapport à l'original d'Anthropic (Apache 2.0).
# ruff: noqa: PGH004
# ruff: noqa
#!/usr/bin/env python3
"""
Script de validation rapide des skills - version minimale
"""

import sys
import os
import re
import yaml
from pathlib import Path


def validate_skill(skill_path):
    """Validation de base d'un skill"""
    skill_path = Path(skill_path)

    # Vérifier que SKILL.md existe
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md introuvable"

    # Lire et valider le frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "Aucun frontmatter YAML trouvé"

    # Extraire le frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Format de frontmatter invalide"

    frontmatter_text = match.group(1)

    # Analyser le frontmatter YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Le frontmatter doit être un dictionnaire YAML"
    except yaml.YAMLError as e:
        return False, f"YAML invalide dans le frontmatter : {e}"

    # Définir les propriétés autorisées
    ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}

    # Rechercher les propriétés inattendues (hors clés imbriquées sous metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Clé(s) inattendue(s) dans le frontmatter de SKILL.md : {', '.join(sorted(unexpected_keys))}. "
            f"Propriétés autorisées : {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Vérifier les champs obligatoires
    if "name" not in frontmatter:
        return False, "Champ 'name' absent du frontmatter"
    if "description" not in frontmatter:
        return False, "Champ 'description' absent du frontmatter"

    # Extraire le nom pour le valider
    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Le nom doit être une chaîne de caractères, type reçu : {type(name).__name__}"
    name = name.strip()
    if name:
        # Vérifier la convention de nommage (hyphen-case : minuscules et tirets)
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Le nom '{name}' doit être en hyphen-case (lettres minuscules, chiffres et tirets uniquement)"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Le nom '{name}' ne peut ni commencer ni finir par un tiret, ni contenir de tirets consécutifs"
        # Vérifier la longueur du nom (64 caractères maximum selon la spécification)
        if len(name) > 64:
            return False, f"Le nom est trop long ({len(name)} caractères). Le maximum est de 64 caractères."

    # Extraire et valider la description
    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"La description doit être une chaîne de caractères, type reçu : {type(description).__name__}"
    description = description.strip()
    if description:
        # Rechercher les chevrons
        if "<" in description or ">" in description:
            return False, "La description ne peut pas contenir de chevrons (< ou >)"
        # Vérifier la longueur de la description (1024 caractères maximum selon la spécification)
        if len(description) > 1024:
            return False, f"La description est trop longue ({len(description)} caractères). Le maximum est de 1024 caractères."

    return True, "Le skill est valide !"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
