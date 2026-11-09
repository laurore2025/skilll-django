---
name: onboard
description: "Prépare Claude à une nouvelle tâche en explorant la base de code, en construisant le contexte et en se préparant à l'implémentation. À utiliser au début d'une nouvelle tâche, fonctionnalité ou correction de bug qui exige d'abord de comprendre la base de code. Se déclenche sur des demandes comme « fais l'onboarding », « prépare-toi pour cette tâche », « explore et prépare-toi », « /onboard »."
---

# Onboarding

L'utilisateur a fourni le contexte de la tâche en argument. Servez-vous-en pour guider l'exploration.

## Instructions

> « Les modèles d'IA sont des génies qui repartent de zéro à chaque tâche. » – Noam Brown

Préparez-vous à la tâche en cours :

- En lisant d'abord `CLAUDE.md`, le skill `conventions-django`, puis `<projet>/docs/` et `<projet>/http/README.md`
- En explorant la base de code en profondeur (sans jamais afficher le contenu de `.env`)
- En posant des questions de clarification à l'utilisateur si nécessaire

L'objectif est d'être entièrement prêt à commencer à travailler sur la tâche.

Prenez tout le temps nécessaire. Mieux vaut en faire trop que pas assez.

Consignez tout dans un fichier `.claude/tasks/[TASK_ID]/onboarding.md`. Ce fichier servira à refaire l'onboarding dans une nouvelle session si nécessaire ; rendez-le donc exhaustif.
