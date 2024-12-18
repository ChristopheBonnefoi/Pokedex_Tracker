# Pokedex Tracker

## Changelog

### V0.1.10
#### Résumé des changements

**Refactorisation et Modularisation**
- Création du module `fetch_types.py` pour isoler la gestion des types des Pokémon (anglais → français).
- Externalisation des traductions des types dans un fichier **JSON** pour une meilleure lisibilité et flexibilité.
- Modularisation progressive des fonctions de récupération des données (ex. `fetch_names`, `fetch_types`).

**Gestion des Logs**
- Amélioration du système de **logs** pour centraliser toutes les erreurs dans un seul fichier horodaté.
- Implémentation d'une logique pour éviter la multiplication des fichiers logs.

**Tests Unitaires**
- Mise en place de tests unitaires pour les nouvelles fonctionnalités :
  - Tests de récupération des types et traduction via `test_fetch_types.py`.
  - Tests pour la récupération des noms anglais et français avec `test_fetch_names.py`.
- Centralisation des tests dans `debug_tools/tests/`.

**Corrections de Bugs**
- Résolution du problème `NOT NULL constraint failed` pour la colonne `type1_fr`.
- Ajustement des imports pour assurer la compatibilité avec la nouvelle structure des modules.
- Correction des erreurs liées à `ModuleNotFoundError` en ajustant les chemins dynamiques dans `sys.path`.

**Divers**
- Mise à jour des instructions pour exécuter les tests dans un fichier dédié : **README_TESTS.md**.
- Nettoyage et stabilisation des scripts existants.

---

### Versions précédentes

#### V0.1.9
- Refactorisation et réorganisation des fichiers pour une structure modulaire.
- Amélioration de la gestion des erreurs avec centralisation des logs.
- Mise à jour de la configuration VSCode et exclusion des fichiers inutiles dans `.gitignore`.
- Corrections des bugs liés aux imports et amélioration de la stabilité.

#### V0.1.8
- Refactorisation des noms en anglais pour la BDD et le code associé (colonnes, variables, commentaires).
- Restructuration de l’arborescence du projet pour une meilleure organisation.

#### V0.1.7
- Améliorations de la gestion de la BDD.
- Ajout des `.gitkeep` pour gérer les dossiers vides (`logs`, `images`).
- Corrections et optimisation du code.

#### V0.1.6
- Finalisation de l'interface de base avec PyQt5.
- Affichage des données des Pokémon dans un tableau interactif.

#### V0.1.5
- Téléchargement des images des Pokémon via l'API.
- Affichage des Pokémon (noms, images, formes) dans l'interface utilisateur.

#### V0.1.4
- Amélioration de la BDD pour inclure :
  - Gestion des formes des Pokémon.
  - Ajout d'une image par défaut pour `image_url` si aucune image n'est disponible.

#### V0.1.3
- Mise en place des outils de débogage.
- Restructuration initiale des fichiers et réorganisation du projet.

#### V0.1.2
- Création de la structure initiale du projet.
- Ajout des fichiers principaux pour démarrer le développement.

#### V0.1.1
- Commit initial :
  - Initialisation du dépôt Git.
  - Mise en place des fichiers de base et configuration du projet.
