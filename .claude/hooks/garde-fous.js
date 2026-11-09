#!/usr/bin/env node
/**
 * Garde-fous des projets Django maison (hooks PreToolUse / PostToolUse de Claude Code).
 *
 * Usage : node garde-fous.js <mode>   — l'événement du hook arrive en JSON sur l'entrée standard.
 *
 * Modes :
 *   env          (PreToolUse)  bloque la lecture, l'affichage et la modification du fichier .env
 *   main         (PreToolUse)  bloque les modifications de fichiers sur la branche main
 *   python       (PostToolUse) vérifie la syntaxe d'un fichier .py modifié avec le Python du venv
 *   gabarit      (PostToolUse) rappelle de redémarrer le serveur --noreload après un gabarit modifié
 *   dependances  (PostToolUse) rappelle de mettre à jour le venv après une modification de requirements.txt
 *
 * Conventions de sortie (Claude Code) :
 *   - code 2 + message sur stderr : action bloquée (PreToolUse) ou erreur signalée à Claude (PostToolUse) ;
 *   - code 0 + JSON hookSpecificOutput.additionalContext : information ajoutée au contexte de Claude ;
 *   - code 0 sans sortie : rien à signaler.
 * Toute erreur interne du script laisse passer l'action (code 0) : un garde-fou ne doit pas bloquer à tort.
 */

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const DOSSIER_PROJET = process.env.CLAUDE_PROJECT_DIR || process.cwd();

function lireEntree() {
  try {
    return JSON.parse(fs.readFileSync(0, 'utf8') || '{}');
  } catch {
    return {};
  }
}

function cheminFichier(evenement) {
  const entree = evenement.tool_input || {};
  return entree.file_path || entree.notebook_path || '';
}

function bloquer(message) {
  process.stderr.write(message + '\n');
  process.exit(2);
}

function informer(evenement, message) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: evenement.hook_event_name || 'PostToolUse',
      additionalContext: message,
    },
  }));
  process.exit(0);
}

// --------------------------------------------------------------------- mode env
// .env contient les secrets : ni affichage, ni lecture, ni modification par Claude.
// .env.example (sans secret) reste librement modifiable.
function estFichierEnv(chemin) {
  return path.basename(chemin || '') === '.env';
}

const AFFICHAGE_ENV = /(?:^|[\s;|&(])(?:cat|type|more|less|head|tail|bat|nl|Get-Content|gc)\s+(?:[^\s;|&]*[\\/])?\.env(?=$|[\s;|&)"'])/i;

function modeEnv(evenement) {
  const outil = evenement.tool_name || '';
  if (['Read', 'Edit', 'MultiEdit', 'Write', 'NotebookEdit'].includes(outil) && estFichierEnv(cheminFichier(evenement))) {
    bloquer("Accès refusé au fichier .env (secrets). Pour un diagnostic, ne lister que les noms de variables "
      + "et si elles sont renseignées ; pour une nouvelle variable, modifier .env.example et indiquer à "
      + "l'utilisateur la ligne à ajouter dans son .env.");
  }
  const commande = (evenement.tool_input || {}).command || '';
  if (['Bash', 'PowerShell'].includes(outil) && AFFICHAGE_ENV.test(commande)) {
    bloquer("Commande refusée : elle afficherait le contenu du fichier .env (secrets). "
      + "Ne lister que les noms de variables, sans leurs valeurs.");
  }
}

// -------------------------------------------------------------------- mode main
function modeMain() {
  let branche = '';
  try {
    branche = execFileSync('git', ['branch', '--show-current'],
      { cwd: DOSSIER_PROJET, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
  } catch {
    return; // pas un dépôt git : rien à protéger
  }
  if (branche === 'main' || branche === 'master') {
    bloquer(`Modification interdite sur la branche ${branche}. Travaillez sur la branche dev `
      + '(git switch dev) ou sur une branche de travail ; la fusion vers main est faite par l’utilisateur.');
  }
}

// ------------------------------------------------------------------ mode python
function pythonDuProjet() {
  const candidats = [
    path.join(DOSSIER_PROJET, 'venv', 'Scripts', 'python.exe'),
    path.join(DOSSIER_PROJET, 'venv', 'bin', 'python'),
    path.join(DOSSIER_PROJET, '.venv', 'Scripts', 'python.exe'),
    path.join(DOSSIER_PROJET, '.venv', 'bin', 'python'),
  ];
  return candidats.find((c) => fs.existsSync(c)) || (process.platform === 'win32' ? 'python' : 'python3');
}

function modePython(evenement) {
  const fichier = cheminFichier(evenement);
  if (!fichier.endsWith('.py') || !fs.existsSync(fichier)) return;
  // ast.parse vérifie la syntaxe sans écrire de .pyc ni importer le module
  const code = 'import ast, sys; ast.parse(open(sys.argv[1], encoding="utf-8").read(), sys.argv[1])';
  try {
    execFileSync(pythonDuProjet(), ['-c', code, fichier], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 20000 });
  } catch (erreur) {
    if (erreur.code === 'ENOENT') return; // Python introuvable : ne pas bloquer
    const detail = String(erreur.stderr || erreur.message).trim().split('\n').slice(-6).join('\n');
    bloquer(`Erreur de syntaxe Python dans ${fichier} :\n${detail}`);
  }
}

// ----------------------------------------------------------------- mode gabarit
function modeGabarit(evenement) {
  const fichier = cheminFichier(evenement).replace(/\\/g, '/');
  if (!/\/templates\/.+\.html$/i.test(fichier)) return;
  informer(evenement, 'Gabarit modifié : si un serveur de vérification tourne avec --noreload (port 8010), '
    + 'le redémarrer avant de contrôler le rendu (les gabarits restent en cache). '
    + "Vérifier aussi les textes en français et les clés data-i18n des traductions.");
}

// ------------------------------------------------------------- mode dependances
function modeDependances(evenement) {
  const fichier = path.basename(cheminFichier(evenement));
  if (!/^requirements.*\.txt$/i.test(fichier)) return;
  informer(evenement, 'requirements.txt modifié : garder des versions figées (paquet==version), déclarer '
    + "explicitement toute bibliothèque importée, puis proposer à l'utilisateur la mise à jour du venv : "
    + 'venv\\Scripts\\python.exe -m pip install -r <projet>\\requirements.txt (Windows) ou '
    + 'venv/bin/python -m pip install -r <projet>/requirements.txt (Linux).');
}

// --------------------------------------------------------------------------------
const MODES = { env: modeEnv, main: modeMain, python: modePython, gabarit: modeGabarit, dependances: modeDependances };

try {
  const mode = MODES[process.argv[2]];
  if (mode) mode(lireEntree());
} catch {
  // erreur interne : ne jamais bloquer à tort
}
process.exit(0);
