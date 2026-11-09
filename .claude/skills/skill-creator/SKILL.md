---
name: skill-creator
description: Guide pour créer des skills efficaces. Ce skill doit être utilisé quand l'utilisateur veut créer un nouveau skill (ou mettre à jour un skill existant) qui étend les capacités de Claude avec des connaissances spécialisées, des workflows ou des intégrations d'outils.
license: Complete terms in LICENSE.txt
---

> Traduction française de l'original d'Anthropic (licence Apache 2.0, voir LICENSE.txt) ; ce fichier a été modifié.

# Créateur de skills

Ce skill fournit des conseils pour créer des skills efficaces.

## À propos des skills

Les skills sont des paquets modulaires et autonomes qui étendent les capacités de Claude en lui apportant
des connaissances spécialisées, des workflows et des outils. Voyez-les comme des « guides d'intégration » pour des
domaines ou des tâches spécifiques : ils transforment Claude, agent généraliste, en agent spécialisé
doté de connaissances procédurales qu'aucun modèle ne peut posséder entièrement.

### Ce qu'apportent les skills

1. Workflows spécialisés - procédures en plusieurs étapes pour des domaines spécifiques
2. Intégrations d'outils - instructions pour travailler avec des formats de fichiers ou des API spécifiques
3. Expertise métier - connaissances propres à l'entreprise, schémas, logique métier
4. Ressources incluses - scripts, références et assets pour les tâches complexes et répétitives

## Principes fondamentaux

### La concision est essentielle

La fenêtre de contexte est un bien commun. Les skills la partagent avec tout ce dont Claude a besoin par ailleurs : prompt système, historique de la conversation, métadonnées des autres skills et requête effective de l'utilisateur.

**Hypothèse par défaut : Claude est déjà très intelligent.** N'ajoutez que le contexte que Claude n'a pas déjà. Remettez en question chaque information : « Claude a-t-il vraiment besoin de cette explication ? » et « Ce paragraphe justifie-t-il son coût en tokens ? »

Préférez des exemples concis à des explications verbeuses.

### Fixer le bon degré de liberté

Adaptez le niveau de précision à la fragilité et à la variabilité de la tâche :

**Grande liberté (instructions textuelles)** : utilisez-la quand plusieurs approches sont valables, que les décisions dépendent du contexte ou que des heuristiques guident la démarche.

**Liberté moyenne (pseudo-code ou scripts paramétrables)** : utilisez-la quand il existe une approche privilégiée, qu'une certaine variation est acceptable ou que la configuration influe sur le comportement.

**Faible liberté (scripts spécifiques, peu de paramètres)** : utilisez-la quand les opérations sont fragiles et sujettes aux erreurs, que la cohérence est critique ou qu'une séquence précise doit être respectée.

Imaginez Claude explorant un chemin : un pont étroit bordé de falaises exige des garde-fous précis (faible liberté), tandis qu'un champ ouvert permet de nombreux itinéraires (grande liberté).

### Anatomie d'un skill

Tout skill se compose d'un fichier SKILL.md obligatoire et de ressources incluses facultatives :

```
skill-name/
├── SKILL.md (obligatoire)
│   ├── Métadonnées du frontmatter YAML (obligatoire)
│   │   ├── name: (obligatoire)
│   │   └── description: (obligatoire)
│   └── Instructions en Markdown (obligatoire)
└── Ressources incluses (facultatif)
    ├── scripts/          - Code exécutable (Python/Bash/etc.)
    ├── references/       - Documentation destinée à être chargée dans le contexte au besoin
    └── assets/           - Fichiers utilisés dans le résultat (gabarits, icônes, polices, etc.)
```

#### SKILL.md (obligatoire)

Tout SKILL.md se compose de :

- **Frontmatter** (YAML) : contient les champs `name` et `description`. Ce sont les seuls champs que Claude lit pour déterminer quand utiliser le skill ; il est donc très important de décrire de façon claire et complète ce qu'est le skill et quand il doit être utilisé.
- **Corps** (Markdown) : instructions et conseils pour utiliser le skill. Chargé uniquement APRÈS le déclenchement du skill (s'il se déclenche).

#### Ressources incluses (facultatif)

##### Scripts (`scripts/`)

Code exécutable (Python/Bash/etc.) pour les tâches qui exigent une fiabilité déterministe ou qui sont réécrites à répétition.

- **Quand les inclure** : quand le même code est réécrit à plusieurs reprises ou qu'une fiabilité déterministe est nécessaire
- **Exemple** : `scripts/rotate_pdf.py` pour les tâches de rotation de PDF
- **Avantages** : économes en tokens, déterministes, peuvent être exécutés sans être chargés dans le contexte
- **Remarque** : Claude peut tout de même avoir besoin de lire les scripts pour les corriger ou les adapter à l'environnement

##### Références (`references/`)

Documentation et documents de référence destinés à être chargés dans le contexte au besoin, pour éclairer la démarche et la réflexion de Claude.

- **Quand les inclure** : pour la documentation que Claude doit consulter pendant son travail
- **Exemples** : `references/finance.md` pour les schémas financiers, `references/mnda.md` pour le gabarit d'accord de confidentialité (NDA) de l'entreprise, `references/policies.md` pour les politiques de l'entreprise, `references/api_docs.md` pour les spécifications d'API
- **Cas d'usage** : schémas de base de données, documentation d'API, connaissances métier, politiques de l'entreprise, guides de workflow détaillés
- **Avantages** : SKILL.md reste léger ; ces fichiers ne sont chargés que lorsque Claude le juge nécessaire
- **Bonne pratique** : si les fichiers sont volumineux (>10 000 mots), indiquez dans SKILL.md des motifs de recherche grep
- **Évitez les doublons** : une information doit se trouver soit dans SKILL.md, soit dans les fichiers de référence, pas dans les deux. Privilégiez les fichiers de référence pour les informations détaillées, sauf si elles sont vraiment au cœur du skill : SKILL.md reste ainsi léger, et l'information reste trouvable sans accaparer la fenêtre de contexte. Ne gardez dans SKILL.md que les instructions procédurales essentielles et les indications de workflow ; déplacez les documents de référence détaillés, les schémas et les exemples dans les fichiers de référence.

##### Assets (`assets/`)

Fichiers non destinés à être chargés dans le contexte, mais à être utilisés dans le résultat que produit Claude.

- **Quand les inclure** : quand le skill a besoin de fichiers qui serviront dans le résultat final
- **Exemples** : `assets/logo.png` pour les éléments de marque, `assets/slides.pptx` pour les gabarits PowerPoint, `assets/frontend-template/` pour le code de base (boilerplate) HTML/React, `assets/font.ttf` pour la typographie
- **Cas d'usage** : gabarits, images, icônes, code de base (boilerplate), polices, documents d'exemple destinés à être copiés ou modifiés
- **Avantages** : sépare les ressources de sortie de la documentation, permet à Claude d'utiliser des fichiers sans les charger dans le contexte

#### Ce qu'il ne faut pas inclure dans un skill

Un skill ne doit contenir que les fichiers essentiels qui servent directement son fonctionnement. Ne créez PAS de documentation superflue ni de fichiers auxiliaires, notamment :

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

Le skill ne doit contenir que les informations dont un agent d'IA a besoin pour accomplir la tâche. Il ne doit pas contenir de contexte annexe sur la façon dont il a été créé, de procédures d'installation et de test, de documentation destinée aux utilisateurs, etc. Créer des fichiers de documentation supplémentaires ne fait qu'ajouter du désordre et de la confusion.

### Principe de conception : divulgation progressive

Les skills utilisent un système de chargement à trois niveaux pour gérer le contexte efficacement :

1. **Métadonnées (name + description)** - toujours dans le contexte (~100 mots)
2. **Corps de SKILL.md** - quand le skill se déclenche (<5 000 mots)
3. **Ressources incluses** - selon les besoins de Claude (illimitées, car les scripts peuvent être exécutés sans être lus dans la fenêtre de contexte)

#### Patrons de divulgation progressive

Limitez le corps de SKILL.md à l'essentiel et à moins de 500 lignes pour éviter d'encombrer le contexte. Répartissez le contenu dans des fichiers séparés à l'approche de cette limite. Lorsque vous déplacez du contenu dans d'autres fichiers, il est très important de les référencer depuis SKILL.md et d'indiquer clairement quand les lire, afin que le lecteur du skill sache qu'ils existent et quand s'en servir.

**Principe clé :** quand un skill prend en charge plusieurs variantes, frameworks ou options, ne gardez dans SKILL.md que le workflow principal et les indications de choix. Déplacez les détails propres à chaque variante (patrons, exemples, configuration) dans des fichiers de référence séparés.

**Patron 1 : guide de haut niveau avec références**

```markdown
# Traitement de PDF

## Démarrage rapide

Extrayez le texte avec pdfplumber :
[exemple de code]

## Fonctionnalités avancées

- **Remplissage de formulaires** : voir [FORMS.md](FORMS.md) pour le guide complet
- **Référence de l'API** : voir [REFERENCE.md](REFERENCE.md) pour toutes les méthodes
- **Exemples** : voir [EXAMPLES.md](EXAMPLES.md) pour les patrons courants
```

Claude ne charge FORMS.md, REFERENCE.md ou EXAMPLES.md qu'en cas de besoin.

**Patron 2 : organisation par domaine**

Pour les skills couvrant plusieurs domaines, organisez le contenu par domaine afin d'éviter de charger du contexte non pertinent :

```
bigquery-skill/
├── SKILL.md (vue d'ensemble et navigation)
└── reference/
    ├── finance.md (chiffre d'affaires, indicateurs de facturation)
    ├── sales.md (opportunités, pipeline)
    ├── product.md (utilisation de l'API, fonctionnalités)
    └── marketing.md (campagnes, attribution)
```

Quand un utilisateur pose une question sur les indicateurs de ventes, Claude ne lit que sales.md.

De même, pour les skills prenant en charge plusieurs frameworks ou variantes, organisez le contenu par variante :

```
cloud-deploy/
├── SKILL.md (workflow + choix du fournisseur)
└── references/
    ├── aws.md (patrons de déploiement AWS)
    ├── gcp.md (patrons de déploiement GCP)
    └── azure.md (patrons de déploiement Azure)
```

Quand l'utilisateur choisit AWS, Claude ne lit que le fichier aws.md.

**Patron 3 : détails conditionnels**

Présentez le contenu de base et renvoyez par un lien vers le contenu avancé :

```markdown
# Traitement de DOCX

## Créer des documents

Utilisez docx-js pour les nouveaux documents. Voir [DOCX-JS.md](DOCX-JS.md).

## Modifier des documents

Pour les modifications simples, modifiez directement le XML.

**Pour les modifications suivies** : voir [REDLINING.md](REDLINING.md)
**Pour les détails OOXML** : voir [OOXML.md](OOXML.md)
```

Claude ne lit REDLINING.md ou OOXML.md que lorsque l'utilisateur a besoin de ces fonctionnalités.

**Consignes importantes :**

- **Évitez les références profondément imbriquées** - gardez les références à un seul niveau de profondeur depuis SKILL.md. Tous les fichiers de référence doivent être liés directement depuis SKILL.md.
- **Structurez les fichiers de référence longs** - pour les fichiers de plus de 100 lignes, placez une table des matières en tête afin que Claude puisse en voir toute la portée lors d'un aperçu.

## Processus de création d'un skill

La création d'un skill comporte les étapes suivantes :

1. Comprendre le skill à l'aide d'exemples concrets
2. Planifier le contenu réutilisable du skill (scripts, références, assets)
3. Initialiser le skill (lancer init_skill.py)
4. Modifier le skill (implémenter les ressources et rédiger SKILL.md)
5. Empaqueter le skill (lancer package_skill.py)
6. Itérer en fonction de l'usage réel

Suivez ces étapes dans l'ordre et n'en sautez une que s'il existe une raison claire pour laquelle elle ne s'applique pas.

### Étape 1 : comprendre le skill à l'aide d'exemples concrets

Ne sautez cette étape que si les modes d'utilisation du skill sont déjà bien compris. Elle reste utile même lorsque vous travaillez sur un skill existant.

Pour créer un skill efficace, comprenez clairement des exemples concrets de la façon dont il sera utilisé. Cette compréhension peut venir d'exemples fournis directement par l'utilisateur ou d'exemples générés puis validés grâce à ses retours.

Par exemple, pour construire un skill image-editor, voici des questions pertinentes :

- « Quelles fonctionnalités le skill image-editor doit-il prendre en charge ? La retouche, la rotation, autre chose ? »
- « Pouvez-vous donner quelques exemples d'utilisation de ce skill ? »
- « J'imagine des utilisateurs demander par exemple “Supprimez les yeux rouges de cette image” ou “Faites pivoter cette image”. Voyez-vous d'autres façons d'utiliser ce skill ? »
- « Que dirait un utilisateur pour déclencher ce skill ? »

Pour ne pas submerger l'utilisateur, évitez de poser trop de questions dans un même message. Commencez par les plus importantes et complétez ensuite selon les besoins, pour plus d'efficacité.

Terminez cette étape lorsque vous avez une idée claire des fonctionnalités que le skill doit prendre en charge.

### Étape 2 : planifier le contenu réutilisable du skill

Pour transformer des exemples concrets en un skill efficace, analysez chaque exemple en :

1. examinant comment le traiter en partant de zéro ;
2. identifiant les scripts, références et assets qui seraient utiles pour exécuter ces workflows de façon répétée.

Exemple : pour construire un skill `pdf-editor` traitant des demandes comme « Aidez-moi à faire pivoter ce PDF », l'analyse montre que :

1. faire pivoter un PDF oblige à réécrire le même code à chaque fois ;
2. il serait utile de stocker un script `scripts/rotate_pdf.py` dans le skill.

Exemple : pour concevoir un skill `frontend-webapp-builder` traitant des demandes comme « Créez-moi une application de liste de tâches » ou « Créez-moi un tableau de bord pour suivre mes pas », l'analyse montre que :

1. écrire une application web frontend demande à chaque fois le même code de base (boilerplate) HTML/React ;
2. il serait utile de stocker dans le skill un gabarit `assets/hello-world/` contenant les fichiers de projet HTML/React de base.

Exemple : pour construire un skill `big-query` traitant des demandes comme « Combien d'utilisateurs se sont connectés aujourd'hui ? », l'analyse montre que :

1. interroger BigQuery oblige à redécouvrir à chaque fois les schémas des tables et leurs relations ;
2. il serait utile de stocker dans le skill un fichier `references/schema.md` documentant les schémas des tables.

Pour établir le contenu du skill, analysez chaque exemple concret afin de dresser la liste des ressources réutilisables à inclure : scripts, références et assets.

### Étape 3 : initialiser le skill

Il est maintenant temps de créer réellement le skill.

Ne sautez cette étape que si le skill en cours de développement existe déjà et qu'il faut l'itérer ou l'empaqueter. Dans ce cas, passez à l'étape suivante.

Pour créer un nouveau skill à partir de zéro, lancez toujours le script `init_skill.py`. Il génère commodément un nouveau répertoire de skill à partir d'un gabarit, qui contient automatiquement tout ce dont un skill a besoin, ce qui rend la création bien plus efficace et fiable.

Utilisation :

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Le script :

- crée le répertoire du skill à l'emplacement indiqué ;
- génère un gabarit SKILL.md avec un frontmatter correct et des espaces réservés TODO ;
- crée des répertoires de ressources d'exemple : `scripts/`, `references/` et `assets/` ;
- ajoute dans chaque répertoire des fichiers d'exemple que vous pouvez personnaliser ou supprimer.

Après l'initialisation, personnalisez ou supprimez selon les besoins le SKILL.md généré et les fichiers d'exemple.

### Étape 4 : modifier le skill

Lorsque vous modifiez le skill (fraîchement généré ou existant), gardez à l'esprit qu'il est créé pour être utilisé par une autre instance de Claude. Incluez les informations utiles et non évidentes pour Claude. Demandez-vous quelles connaissances procédurales, quels détails propres au domaine ou quels assets réutilisables aideraient une autre instance de Claude à exécuter ces tâches plus efficacement.

#### S'inspirer de patrons de conception éprouvés

Consultez ces guides utiles selon les besoins de votre skill :

- **Processus en plusieurs étapes** : voir references/workflows.md pour les workflows séquentiels et la logique conditionnelle
- **Formats de sortie précis ou exigences de qualité** : voir references/output-patterns.md pour les patrons de gabarit et d'exemples

Ces fichiers rassemblent des bonnes pratiques établies pour concevoir des skills efficaces.

#### Commencer par le contenu réutilisable du skill

Pour commencer l'implémentation, partez des ressources réutilisables identifiées plus haut : fichiers `scripts/`, `references/` et `assets/`. Notez que cette étape peut nécessiter une contribution de l'utilisateur. Par exemple, pour implémenter un skill `brand-guidelines`, l'utilisateur devra peut-être fournir des éléments de marque ou des gabarits à stocker dans `assets/`, ou de la documentation à stocker dans `references/`.

Les scripts ajoutés doivent être testés en les exécutant réellement, pour s'assurer qu'ils ne contiennent pas de bug et que leur sortie correspond à ce qui est attendu. S'il y a beaucoup de scripts similaires, il suffit d'en tester un échantillon représentatif pour avoir confiance dans leur bon fonctionnement, tout en maîtrisant le temps nécessaire.

Supprimez les fichiers et répertoires d'exemple dont le skill n'a pas besoin. Le script d'initialisation crée des fichiers d'exemple dans `scripts/`, `references/` et `assets/` pour illustrer la structure, mais la plupart des skills n'en auront pas tous besoin.

#### Mettre à jour SKILL.md

**Consignes de rédaction :** utilisez toujours la forme impérative/infinitive.

##### Frontmatter

Rédigez le frontmatter YAML avec `name` et `description` :

- `name` : le nom du skill
- `description` : c'est le principal mécanisme de déclenchement de votre skill ; il aide Claude à comprendre quand utiliser le skill.
  - Indiquez à la fois ce que fait le skill et les déclencheurs/contextes précis dans lesquels l'utiliser.
  - Placez ici toutes les informations « quand l'utiliser », et non dans le corps. Le corps n'est chargé qu'après le déclenchement : les sections « Quand utiliser ce skill » dans le corps ne sont donc d'aucune aide pour Claude.
  - Exemple de description pour un skill `docx` : « Création, modification et analyse complètes de documents, avec prise en charge des modifications suivies, des commentaires, de la conservation de la mise en forme et de l'extraction de texte. À utiliser quand Claude doit travailler sur des documents professionnels (fichiers .docx) pour : (1) créer de nouveaux documents, (2) modifier ou retoucher du contenu, (3) travailler avec les modifications suivies, (4) ajouter des commentaires, ou toute autre tâche sur des documents »

N'incluez aucun autre champ dans le frontmatter YAML.

##### Corps

Rédigez les instructions d'utilisation du skill et de ses ressources incluses.

### Étape 5 : empaqueter un skill

Une fois le développement du skill terminé, il doit être empaqueté dans un fichier .skill distribuable, qui sera partagé avec l'utilisateur. Le processus d'empaquetage commence par valider automatiquement le skill pour s'assurer qu'il respecte toutes les exigences :

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Indication facultative du répertoire de sortie :

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

Le script d'empaquetage va :

1. **Valider** automatiquement le skill, en vérifiant :

   - le format du frontmatter YAML et les champs obligatoires ;
   - les conventions de nommage du skill et la structure des répertoires ;
   - l'exhaustivité et la qualité de la description ;
   - l'organisation des fichiers et les références aux ressources.

2. **Empaqueter** le skill si la validation réussit, en créant un fichier .skill portant le nom du skill (par ex. `my-skill.skill`) qui inclut tous les fichiers et conserve la structure de répertoires adéquate pour la distribution. Le fichier .skill est un fichier zip avec l'extension .skill.

Si la validation échoue, le script signale les erreurs et s'arrête sans créer de paquet. Corrigez les erreurs de validation et relancez la commande d'empaquetage.

### Étape 6 : itérer

Après avoir testé le skill, les utilisateurs peuvent demander des améliorations. Cela arrive souvent juste après l'utilisation du skill, quand on a encore bien en tête la façon dont il s'est comporté.

**Workflow d'itération :**

1. Utilisez le skill sur des tâches réelles
2. Repérez les difficultés ou les inefficacités
3. Déterminez comment SKILL.md ou les ressources incluses doivent être mis à jour
4. Appliquez les modifications et testez à nouveau
