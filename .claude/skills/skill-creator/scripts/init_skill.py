# Traduction française : fichier modifié par rapport à l'original d'Anthropic (Apache 2.0).
# ruff: noqa: PGH004
# ruff: noqa
#!/usr/bin/env python3
"""
Initialiseur de skill - Crée un nouveau skill à partir d'un gabarit

Utilisation :
    init_skill.py <skill-name> --path <path>

Exemples :
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Expliquez de façon complète et informative ce que fait le skill et quand l'utiliser. Indiquez QUAND utiliser ce skill - scénarios précis, types de fichiers ou tâches qui le déclenchent.]
---

# {skill_title}

## Vue d'ensemble

[TODO: 1 à 2 phrases expliquant ce que ce skill permet de faire]

## Structurer ce skill

[TODO: Choisissez la structure la mieux adaptée à l'objectif de ce skill. Patrons courants :

**1. Par workflow** (idéal pour les processus séquentiels)
- Convient quand il existe des procédures claires, étape par étape
- Exemple : skill DOCX avec « Arbre de décision du workflow » → « Lecture » → « Création » → « Modification »
- Structure : ## Vue d'ensemble → ## Arbre de décision du workflow → ## Étape 1 → ## Étape 2...

**2. Par tâche** (idéal pour les collections d'outils)
- Convient quand le skill propose différentes opérations/capacités
- Exemple : skill PDF avec « Démarrage rapide » → « Fusionner des PDF » → « Scinder des PDF » → « Extraire le texte »
- Structure : ## Vue d'ensemble → ## Démarrage rapide → ## Catégorie de tâches 1 → ## Catégorie de tâches 2...

**3. Référence/Consignes** (idéal pour les normes ou les spécifications)
- Convient aux chartes de marque, aux normes de codage ou aux exigences
- Exemple : style de marque avec « Charte de marque » → « Couleurs » → « Typographie » → « Fonctionnalités »
- Structure : ## Vue d'ensemble → ## Consignes → ## Spécifications → ## Utilisation...

**4. Par capacités** (idéal pour les systèmes intégrés)
- Convient quand le skill fournit plusieurs fonctionnalités liées entre elles
- Exemple : gestion de produit avec « Capacités principales » → liste numérotée des capacités
- Structure : ## Vue d'ensemble → ## Capacités principales → ### 1. Fonctionnalité → ### 2. Fonctionnalité...

Les patrons peuvent être mélangés et combinés selon les besoins. La plupart des skills combinent plusieurs patrons (par ex. commencer par une structure par tâche, puis ajouter un workflow pour les opérations complexes).

Supprimez entièrement cette section « Structurer ce skill » une fois terminé - ce n'est qu'une aide.]

## [TODO: Remplacez par la première section principale selon la structure choisie]

[TODO: Ajoutez le contenu ici. Voir les exemples dans les skills existants :
- Exemples de code pour les skills techniques
- Arbres de décision pour les workflows complexes
- Exemples concrets avec des demandes d'utilisateur réalistes
- Références aux scripts/gabarits/références selon les besoins]

## Ressources

Ce skill comprend des répertoires de ressources d'exemple qui montrent comment organiser les différents types de ressources incluses :

### scripts/
Code exécutable (Python/Bash/etc.) qui peut être lancé directement pour effectuer des opérations précises.

**Exemples tirés d'autres skills :**
- Skill PDF : `fill_fillable_fields.py`, `extract_form_field_info.py` - utilitaires de manipulation de PDF
- Skill DOCX : `document.py`, `utilities.py` - modules Python de traitement de documents

**Adapté pour :** les scripts Python, les scripts shell ou tout code exécutable qui réalise de l'automatisation, du traitement de données ou des opérations précises.

**Remarque :** les scripts peuvent être exécutés sans être chargés dans le contexte, mais Claude peut tout de même les lire pour les corriger ou les adapter à l'environnement.

### references/
Documentation et documents de référence destinés à être chargés dans le contexte pour éclairer la démarche et la réflexion de Claude.

**Exemples tirés d'autres skills :**
- Gestion de produit : `communication.md`, `context_building.md` - guides de workflow détaillés
- BigQuery : documentation de référence de l'API et exemples de requêtes
- Finance : documentation des schémas, politiques de l'entreprise

**Adapté pour :** la documentation approfondie, les références d'API, les schémas de base de données, les guides complets ou toute information détaillée que Claude doit consulter pendant son travail.

### assets/
Fichiers non destinés à être chargés dans le contexte, mais à être utilisés dans le résultat que produit Claude.

**Exemples tirés d'autres skills :**
- Style de marque : fichiers de gabarit PowerPoint (.pptx), fichiers de logo
- Générateur frontend : répertoires de projet de base (boilerplate) HTML/React
- Typographie : fichiers de police (.ttf, .woff2)

**Adapté pour :** les gabarits, le code de base (boilerplate), les gabarits de documents, les images, les icônes, les polices ou tout fichier destiné à être copié ou utilisé dans le résultat final.

---

**Les répertoires inutiles peuvent être supprimés.** Tous les skills n'ont pas besoin des trois types de ressources.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Script d'aide d'exemple pour {skill_name}

Ceci est un script provisoire qui peut être exécuté directement.
Remplacez-le par une implémentation réelle ou supprimez-le s'il n'est pas nécessaire.

Exemples de scripts réels tirés d'autres skills :
- pdf/scripts/fill_fillable_fields.py - Remplit les champs d'un formulaire PDF
- pdf/scripts/convert_pdf_to_images.py - Convertit les pages d'un PDF en images
"""

def main():
    print("Ceci est un script d'exemple pour {skill_name}")
    # TODO: Ajoutez ici la logique réelle du script
    # Il peut s'agir de traitement de données, de conversion de fichiers, d'appels d'API, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Documentation de référence pour {skill_title}

Ceci est un espace réservé pour une documentation de référence détaillée.
Remplacez-le par un contenu de référence réel ou supprimez-le s'il n'est pas nécessaire.

Exemples de documents de référence réels tirés d'autres skills :
- product-management/references/communication.md - Guide complet pour les points d'avancement
- product-management/references/context_building.md - Analyse approfondie de la collecte de contexte
- bigquery/references/ - Références d'API et exemples de requêtes

## Quand les documents de référence sont utiles

Les documents de référence sont idéaux pour :
- Une documentation d'API complète
- Des guides de workflow détaillés
- Des processus complexes en plusieurs étapes
- Des informations trop longues pour le SKILL.md principal
- Du contenu nécessaire uniquement pour des cas d'usage précis

## Suggestions de structure

### Exemple de référence d'API
- Vue d'ensemble
- Authentification
- Points de terminaison (endpoints) avec exemples
- Codes d'erreur
- Limites de débit

### Exemple de guide de workflow
- Prérequis
- Instructions étape par étape
- Patrons courants
- Dépannage
- Bonnes pratiques
"""

EXAMPLE_ASSET = """# Fichier d'asset d'exemple

Cet espace réservé indique où seraient stockés les fichiers d'assets.
Remplacez-le par de vrais fichiers d'assets (gabarits, images, polices, etc.) ou supprimez-le s'il n'est pas nécessaire.

Les fichiers d'assets ne sont PAS destinés à être chargés dans le contexte, mais à être utilisés
dans le résultat que produit Claude.

Exemples de fichiers d'assets tirés d'autres skills :
- Charte de marque : logo.png, slides_template.pptx
- Générateur frontend : répertoire hello-world/ avec du code de base (boilerplate) HTML/React
- Typographie : custom-font.ttf, font-family.woff2
- Données : sample_data.csv, test_dataset.json

## Types d'assets courants

- Gabarits : .pptx, .docx, répertoires de code de base
- Images : .png, .jpg, .svg, .gif
- Polices : .ttf, .otf, .woff, .woff2
- Code de base : répertoires de projet, fichiers de démarrage
- Icônes : .ico, .svg
- Fichiers de données : .csv, .json, .xml, .yaml

Remarque : ceci est un espace réservé textuel. Les vrais assets peuvent être de n'importe quel type de fichier.
"""


def title_case_skill_name(skill_name):
    """Convertit un nom de skill à tirets en casse de titre (Title Case) pour l'affichage."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def init_skill(skill_name, path):
    """
    Initialise un nouveau répertoire de skill avec un gabarit SKILL.md.

    Args:
        skill_name: Nom du skill
        path: Chemin où créer le répertoire du skill

    Returns:
        Chemin du répertoire de skill créé, ou None en cas d'erreur
    """
    # Déterminer le chemin du répertoire du skill
    skill_dir = Path(path).resolve() / skill_name

    # Vérifier si le répertoire existe déjà
    if skill_dir.exists():
        print(f"❌ Erreur : le répertoire du skill existe déjà : {skill_dir}")
        return None

    # Créer le répertoire du skill
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Répertoire du skill créé : {skill_dir}")
    except Exception as e:
        print(f"❌ Erreur lors de la création du répertoire : {e}")
        return None

    # Créer SKILL.md à partir du gabarit
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content)
        print("✅ SKILL.md créé")
    except Exception as e:
        print(f"❌ Erreur lors de la création de SKILL.md : {e}")
        return None

    # Créer les répertoires de ressources avec des fichiers d'exemple
    try:
        # Créer le répertoire scripts/ avec un script d'exemple
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / "example.py"
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ scripts/example.py créé")

        # Créer le répertoire references/ avec un document de référence d'exemple
        references_dir = skill_dir / "references"
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / "api_reference.md"
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ references/api_reference.md créé")

        # Créer le répertoire assets/ avec un asset d'exemple provisoire
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / "example_asset.txt"
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ assets/example_asset.txt créé")
    except Exception as e:
        print(f"❌ Erreur lors de la création des répertoires de ressources : {e}")
        return None

    # Afficher les étapes suivantes
    print(f"\n✅ Skill '{skill_name}' initialisé avec succès dans {skill_dir}")
    print("\nÉtapes suivantes :")
    print("1. Modifiez SKILL.md pour compléter les éléments TODO et mettre à jour la description")
    print("2. Personnalisez ou supprimez les fichiers d'exemple dans scripts/, references/ et assets/")
    print("3. Lancez le validateur, une fois prêt, pour vérifier la structure du skill")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("Utilisation : init_skill.py <skill-name> --path <path>")
        print("\nExigences pour le nom du skill :")
        print("  - Identifiant en hyphen-case (par ex. 'data-analyzer')")
        print("  - Lettres minuscules, chiffres et tirets uniquement")
        print("  - 40 caractères maximum")
        print("  - Doit correspondre exactement au nom du répertoire")
        print("\nExemples :")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 Initialisation du skill : {skill_name}")
    print(f"   Emplacement : {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
