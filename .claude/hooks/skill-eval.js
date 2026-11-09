#!/usr/bin/env node
/**
 * Moteur d'évaluation des skills v2.0
 *
 * Activation intelligente des skills selon :
 * - les mots-clés et motifs présents dans le prompt ;
 * - les chemins de fichiers mentionnés ou en cours de modification ;
 * - les correspondances de répertoires ;
 * - la détection d'intention ;
 * - les motifs de contenu (extraits de code).
 *
 * Produit un rappel structuré listant les skills retenus et les raisons.
 */

const fs = require('fs');
const path = require('path');

// Configuration
const RULES_PATH = path.join(__dirname, 'skill-rules.json');

/**
 * @typedef {Object} SkillMatch
 * @property {string} name - Nom du skill
 * @property {number} score - Score de confiance
 * @property {string[]} reasons - Raisons de la correspondance
 * @property {number} priority - Priorité du skill
 */

/**
 * Charge les règles des skills depuis le fichier JSON
 * @returns {Object} Règles analysées
 */
function loadRules() {
  try {
    const content = fs.readFileSync(RULES_PATH, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`Impossible de charger les règles des skills : ${error.message}`);
    process.exit(0); // Sortie silencieuse pour ne pas bloquer le prompt
  }
}

/**
 * Extrait les chemins de fichiers mentionnés dans le prompt
 * @param {string} prompt - Texte du prompt de l'utilisateur
 * @returns {string[]} Chemins de fichiers détectés
 */
function extractFilePaths(prompt) {
  const paths = new Set();

  // Chemins Windows (barres obliques inverses) ramenés au format « / »
  const texte = prompt.replace(/\\/g, '/');

  // Chemins explicites avec extension : Python/Django, web, configuration, scripts, documentation
  const extensionPattern =
    /(?:^|\s|["'`(\[])([\w\-./:]+\.(?:py|html|css|[tj]sx?|json|ya?ml|toml|txt|http|sql|ps1|sh|md|env|example|cfg|ini|gql))\b/gi;
  let match;
  while ((match = extensionPattern.exec(texte)) !== null) {
    paths.add(match[1]);
  }

  // Chemins commençant par un répertoire courant (projets Django et configuration Claude)
  const dirPattern =
    /(?:^|\s|["'`(\[])((?:apps|templates|static|docs|http|scripts|data|config|migrations|management|src|app|services|\.claude|\.github)\/[\w\-./]+)/gi;
  while ((match = dirPattern.exec(texte)) !== null) {
    paths.add(match[1]);
  }

  // Chemins entre guillemets
  const quotedPattern = /["'`]([\w\-./:]+\/[\w\-./]+)["'`]/g;
  while ((match = quotedPattern.exec(texte)) !== null) {
    paths.add(match[1]);
  }

  return Array.from(paths);
}

/**
 * Indique si un motif correspond au texte
 * @param {string} text - Texte à analyser
 * @param {string} pattern - Expression régulière
 * @param {string} flags - Options de l'expression régulière
 * @returns {boolean}
 */
function matchesPattern(text, pattern, flags = 'i') {
  try {
    const regex = new RegExp(pattern, flags);
    return regex.test(text);
  } catch {
    return false;
  }
}

/**
 * Indique si un motif glob correspond à un chemin de fichier
 * @param {string} filePath - Chemin à vérifier
 * @param {string} globPattern - Motif glob (simplifié)
 * @returns {boolean}
 */
function matchesGlob(filePath, globPattern) {
  // Conversion du glob en expression régulière (simplifiée)
  const regexPattern = globPattern
    .replace(/\./g, '\\.')
    .replace(/\*\*\//g, '<<<DOUBLESTARSLASH>>>')
    .replace(/\*\*/g, '<<<DOUBLESTAR>>>')
    .replace(/\*/g, '[^/]*')
    .replace(/<<<DOUBLESTARSLASH>>>/g, '(.*\\/)?')
    .replace(/<<<DOUBLESTAR>>>/g, '.*')
    .replace(/\?/g, '.');

  try {
    const regex = new RegExp(`^${regexPattern}$`, 'i');
    return regex.test(filePath.replace(/\\/g, '/'));
  } catch {
    return false;
  }
}

/**
 * Indique si un chemin correspond à une association répertoire → skill
 * @param {string} filePath - Chemin à vérifier
 * @param {Object} mappings - Associations répertoire → skill
 * @returns {string|null} Nom du skill associé, ou null
 */
function matchDirectoryMapping(filePath, mappings) {
  const chemin = filePath.replace(/\\/g, '/');
  for (const [dir, skillName] of Object.entries(mappings)) {
    const d = dir.replace(/\/+$/, '');
    if (chemin === d || chemin.startsWith(d + '/') || chemin.includes('/' + d + '/')) {
      return skillName;
    }
  }
  return null;
}

/**
 * Évalue un skill par rapport au prompt et au contexte
 * @param {string} skillName - Nom du skill
 * @param {Object} skill - Configuration du skill
 * @param {string} prompt - Prompt de l'utilisateur
 * @param {string} promptLower - Prompt en minuscules
 * @param {string[]} filePaths - Chemins extraits
 * @param {Object} rules - Ensemble des règles
 * @returns {SkillMatch|null}
 */
function evaluateSkill(
  skillName,
  skill,
  prompt,
  promptLower,
  filePaths,
  rules
) {
  const { triggers = {}, excludePatterns = [], priority = 5 } = skill;
  const scoring = rules.scoring;

  let score = 0;
  const reasons = [];

  // Motifs d'exclusion en premier
  for (const excludePattern of excludePatterns) {
    if (matchesPattern(promptLower, excludePattern)) {
      return null;
    }
  }

  // 1. Mots-clés
  if (triggers.keywords) {
    for (const keyword of triggers.keywords) {
      if (promptLower.includes(keyword.toLowerCase())) {
        score += scoring.keyword;
        reasons.push(`mot-clé "${keyword}"`);
      }
    }
  }

  // 2. Motifs de mots-clés (expressions régulières)
  if (triggers.keywordPatterns) {
    for (const pattern of triggers.keywordPatterns) {
      if (matchesPattern(promptLower, pattern)) {
        score += scoring.keywordPattern;
        reasons.push(`motif /${pattern}/`);
      }
    }
  }

  // 3. Motifs d'intention
  if (triggers.intentPatterns) {
    for (const pattern of triggers.intentPatterns) {
      if (matchesPattern(promptLower, pattern)) {
        score += scoring.intentPattern;
        reasons.push(`intention détectée`);
        break;
      }
    }
  }

  // 4. Motifs de contexte
  if (triggers.contextPatterns) {
    for (const pattern of triggers.contextPatterns) {
      if (promptLower.includes(pattern.toLowerCase())) {
        score += scoring.contextPattern;
        reasons.push(`contexte "${pattern}"`);
      }
    }
  }

  // 5. Chemins de fichiers comparés aux motifs de chemin
  if (triggers.pathPatterns && filePaths.length > 0) {
    for (const filePath of filePaths) {
      for (const pattern of triggers.pathPatterns) {
        if (matchesGlob(filePath, pattern)) {
          score += scoring.pathPattern;
          reasons.push(`chemin "${filePath}"`);
          break;
        }
      }
    }
  }

  // 6. Associations de répertoires
  if (rules.directoryMappings && filePaths.length > 0) {
    for (const filePath of filePaths) {
      const mappedSkill = matchDirectoryMapping(
        filePath,
        rules.directoryMappings
      );
      if (mappedSkill === skillName) {
        score += scoring.directoryMatch;
        reasons.push(`association de répertoire`);
        break;
      }
    }
  }

  // 7. Motifs de contenu dans le prompt (extraits de code)
  if (triggers.contentPatterns) {
    for (const pattern of triggers.contentPatterns) {
      if (matchesPattern(prompt, pattern)) {
        score += scoring.contentPattern;
        reasons.push(`motif de code détecté`);
        break;
      }
    }
  }

  if (score > 0) {
    return {
      name: skillName,
      score,
      reasons: [...new Set(reasons)],
      priority,
    };
  }

  return null;
}

/**
 * Renvoie les skills liés à suggérer en complément
 * @param {SkillMatch[]} matches - Correspondances actuelles
 * @param {Object} skills - Définitions de tous les skills
 * @returns {string[]} Noms des skills supplémentaires à suggérer
 */
function getRelatedSkills(matches, skills) {
  const matchedNames = new Set(matches.map((m) => m.name));
  const related = new Set();

  for (const match of matches) {
    const skill = skills[match.name];
    if (skill?.relatedSkills) {
      for (const relatedName of skill.relatedSkills) {
        if (!matchedNames.has(relatedName)) {
          related.add(relatedName);
        }
      }
    }
  }

  return Array.from(related);
}

/**
 * Libellé du niveau de confiance selon le score
 * @param {number} score - Score de confiance
 * @param {number} minScore - Seuil minimal
 * @returns {string} Libellé de confiance
 */
function formatConfidence(score, minScore) {
  if (score >= minScore * 3) return 'ÉLEVÉE';
  if (score >= minScore * 2) return 'MOYENNE';
  return 'FAIBLE';
}

/**
 * Fonction principale d'évaluation
 * @param {string} prompt - Prompt de l'utilisateur
 * @returns {string} Sortie mise en forme
 */
function evaluate(prompt) {
  const rules = loadRules();
  const { config, skills } = rules;

  const promptLower = prompt.toLowerCase();
  const filePaths = extractFilePaths(prompt);

  // Évaluation de tous les skills
  const matches = [];
  for (const [name, skill] of Object.entries(skills)) {
    const match = evaluateSkill(
      name,
      skill,
      prompt,
      promptLower,
      filePaths,
      rules
    );
    if (match && match.score >= config.minConfidenceScore) {
      matches.push(match);
    }
  }

  if (matches.length === 0) {
    return '';
  }

  // Tri par score (décroissant), puis par priorité (décroissante)
  matches.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return b.priority - a.priority;
  });

  // Limite au nombre maximal de skills
  const topMatches = matches.slice(0, config.maxSkillsToShow);

  // Skills liés
  const relatedSkills = getRelatedSkills(topMatches, skills);

  // Mise en forme de la sortie
  let output = '<user-prompt-submit-hook>\n';
  output += 'ACTIVATION DE SKILLS REQUISE\n\n';

  if (filePaths.length > 0) {
    output += `Chemins de fichiers détectés : ${filePaths.join(', ')}\n\n`;
  }

  output += 'Skills correspondants (classés par pertinence) :\n';

  for (let i = 0; i < topMatches.length; i++) {
    const match = topMatches[i];
    const confidence = formatConfidence(match.score, config.minConfidenceScore);

    output += `${i + 1}. ${match.name} (confiance ${confidence})\n`;

    if (config.showMatchReasons && match.reasons.length > 0) {
      output += `   Correspondance : ${match.reasons.slice(0, 3).join(', ')}\n`;
    }
  }

  if (relatedSkills.length > 0) {
    output += `\nSkills liés à envisager : ${relatedSkills.join(', ')}\n`;
  }

  output += '\nAvant toute implémentation, vous DEVEZ :\n';
  output += '1. ÉVALUER : indiquer OUI/NON pour chaque skill, avec une brève justification\n';
  output += "2. ACTIVER : invoquer l'outil Skill pour chaque skill marqué OUI\n";
  output += "3. IMPLÉMENTER : ne commencer qu'après l'activation des skills\n";
  output += "\nExemple d'évaluation :\n";
  output += `- ${topMatches[0].name} : OUI - [votre justification]\n`;
  if (topMatches.length > 1) {
    output += `- ${topMatches[1].name} : NON - [votre justification]\n`;
  }
  output += '\nNE SAUTEZ PAS cette étape. Invoquez les skills pertinents MAINTENANT.\n';
  output += '</user-prompt-submit-hook>';

  return output;
}

// Exécution principale
function main() {
  let input = '';

  process.stdin.setEncoding('utf8');

  process.stdin.on('data', (chunk) => {
    input += chunk;
  });

  process.stdin.on('end', () => {
    let prompt = '';

    try {
      const data = JSON.parse(input);
      prompt = data.prompt || '';
    } catch {
      prompt = input;
    }

    if (!prompt.trim()) {
      process.exit(0);
    }

    try {
      const output = evaluate(prompt);
      if (output) {
        console.log(output);
      }
    } catch (error) {
      console.error(`Échec de l'évaluation des skills : ${error.message}`);
    }

    process.exit(0);
  });
}

main();
