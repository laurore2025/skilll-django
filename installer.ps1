# Installe la configuration Claude Code de ce depot (Windows, PowerShell 5.1 ou 7).
# Fichier volontairement en ASCII : PowerShell 5.1 abime les accents des scripts sans BOM.
#
# Usage (depuis la racine du depot) :
#   .\installer.ps1                                   # skills + agents pour l'utilisateur (tous les projets)
#   .\installer.ps1 -Projet C:\xampp\htdocs\MonProjet # en plus : CLAUDE.md, settings et hooks du projet
#   .\installer.ps1 -Projet C:\...\MonProjet -Force   # remplace CLAUDE.md et settings.json existants
#   .\installer.ps1 -SansUtilisateur -Projet C:\...    # projet seulement
#
# Les skills et agents installes pour l'utilisateur sont disponibles dans tous les projets.
# Les hooks et settings ne sont installes que dans un projet choisi : ils ne s'appliquent pas ailleurs.
# Tout element remplace est d'abord sauvegarde dans ~/.claude/backups/skilll-django-<date>/.

param(
    [string]$Projet = "",
    [switch]$Force,
    [switch]$SansUtilisateur
)

$ErrorActionPreference = "Stop"
$source = $PSScriptRoot
$claudeSource = Join-Path $source ".claude"
$claudeUtilisateur = Join-Path $HOME ".claude"
$horodatage = Get-Date -Format "yyyyMMdd-HHmmss"
$sauvegarde = Join-Path $claudeUtilisateur "backups\skilll-django-$horodatage"

function Sauvegarder([string]$chemin, [string]$sousDossier) {
    if (Test-Path $chemin) {
        $cible = Join-Path $sauvegarde $sousDossier
        New-Item -ItemType Directory -Force $cible | Out-Null
        Copy-Item $chemin $cible -Recurse -Force
        Remove-Item $chemin -Recurse -Force
    }
}

if (-not (Test-Path (Join-Path $claudeSource "skills"))) {
    throw "Dossier .claude/skills introuvable : lancer le script depuis la racine du depot skilll-django."
}

# --- 1. Skills et agents pour l'utilisateur ------------------------------------------
if (-not $SansUtilisateur) {
    $dossierSkills = Join-Path $claudeUtilisateur "skills"
    $dossierAgents = Join-Path $claudeUtilisateur "agents"
    New-Item -ItemType Directory -Force $dossierSkills, $dossierAgents | Out-Null

    $skills = Get-ChildItem (Join-Path $claudeSource "skills") -Directory
    foreach ($s in $skills) {
        $cible = Join-Path $dossierSkills $s.Name
        Sauvegarder $cible "skills"
        Copy-Item $s.FullName $cible -Recurse -Force
    }
    Write-Host ("Skills installes dans {0} : {1}" -f $dossierSkills, (($skills | ForEach-Object Name) -join ", "))

    $agents = Get-ChildItem (Join-Path $claudeSource "agents") -Filter *.md
    foreach ($a in $agents) {
        $cible = Join-Path $dossierAgents $a.Name
        Sauvegarder $cible "agents"
        Copy-Item $a.FullName $cible -Force
    }
    Write-Host ("Agents installes dans {0} : {1}" -f $dossierAgents, (($agents | ForEach-Object BaseName) -join ", "))
}

# --- 2. Configuration d'un projet Django (facultatif) -------------------------------
if ($Projet) {
    if (-not (Test-Path $Projet)) { throw "Projet introuvable : $Projet" }
    $claudeProjet = Join-Path $Projet ".claude"
    New-Item -ItemType Directory -Force (Join-Path $claudeProjet "hooks") | Out-Null

    # Fichiers que l'utilisateur personnalise : jamais remplaces sans -Force
    $personnalises = @(
        @{ De = Join-Path $source "CLAUDE.md";            Vers = Join-Path $Projet "CLAUDE.md" },
        @{ De = Join-Path $claudeSource "settings.json"; Vers = Join-Path $claudeProjet "settings.json" }
    )
    foreach ($f in $personnalises) {
        if ((Test-Path $f.Vers) -and -not $Force) {
            Write-Host ("Conserve (deja present, -Force pour remplacer) : {0}" -f $f.Vers)
            continue
        }
        Sauvegarder $f.Vers "projet"
        Copy-Item $f.De $f.Vers -Force
        Write-Host ("Copie : {0}" -f $f.Vers)
    }

    # Fichiers geres par ce depot : remplaces a chaque installation
    Copy-Item (Join-Path $claudeSource "hooks\*") (Join-Path $claudeProjet "hooks") -Force
    Copy-Item (Join-Path $claudeSource "settings.md") $claudeProjet -Force
    Write-Host ("Hooks copies dans {0}" -f (Join-Path $claudeProjet "hooks"))

    Write-Host ""
    Write-Host "A faire dans le projet :"
    Write-Host "  - adapter CLAUDE.md (nom du projet, sous-dossier Django, commandes) ;"
    Write-Host "  - verifier que Node.js est installe (hooks) ;"
    Write-Host "  - ajouter .claude/settings.local.json au .gitignore si des reglages personnels y sont mis."
}

if (Test-Path $sauvegarde) { Write-Host "Elements remplaces sauvegardes dans : $sauvegarde" }
Write-Host "Termine. Redemarrer Claude Code pour charger les nouveaux skills."
