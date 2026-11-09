# Traduction française : fichier modifié par rapport à l'original d'Anthropic (Apache 2.0).
# ruff: noqa: PGH004
# ruff: noqa
#!/usr/bin/env python3
"""
Empaqueteur de skill - Crée un fichier .skill distribuable à partir d'un dossier de skill

Utilisation :
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

Exemple :
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill


def package_skill(skill_path, output_dir=None):
    """
    Empaquette un dossier de skill dans un fichier .skill.

    Args:
        skill_path: Chemin du dossier du skill
        output_dir: Répertoire de sortie facultatif pour le fichier .skill (par défaut, le répertoire courant)

    Returns:
        Chemin du fichier .skill créé, ou None en cas d'erreur
    """
    skill_path = Path(skill_path).resolve()

    # Vérifier que le dossier du skill existe
    if not skill_path.exists():
        print(f"❌ Erreur : dossier du skill introuvable : {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Erreur : le chemin n'est pas un répertoire : {skill_path}")
        return None

    # Vérifier que SKILL.md existe
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Erreur : SKILL.md introuvable dans {skill_path}")
        return None

    # Lancer la validation avant l'empaquetage
    print("🔍 Validation du skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Échec de la validation : {message}")
        print("   Corrigez les erreurs de validation avant l'empaquetage.")
        return None
    print(f"✅ {message}\n")

    # Déterminer l'emplacement de sortie
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # Créer le fichier .skill (format zip)
    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Parcourir le répertoire du skill
            for file_path in skill_path.rglob("*"):
                if file_path.is_file():
                    # Calculer le chemin relatif dans le zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Ajouté : {arcname}")

        print(f"\n✅ Skill empaqueté avec succès dans : {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier .skill : {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Utilisation : python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExemple :")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Empaquetage du skill : {skill_path}")
    if output_dir:
        print(f"   Répertoire de sortie : {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
