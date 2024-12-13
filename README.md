# Pokedex Tracker

## Changelog

### V0.1.9
#### Résumé des changements

**Refactorisation et Réorganisation**
- Déplacement de `log_error.py` dans le dossier `functions` pour centraliser les outils communs.
- Correction des imports et des chemins pour garantir la stabilité et la compatibilité avec la structure du projet.
- Suppression et réinitialisation des caches liés aux imports pour résoudre des erreurs de reconnaissance de module.  
- Mise en place de fichiers `__init__.py` dans les dossiers pour officialiser les packages.  

**Base de Données**
- Refonte du script `initialize_db.py` pour gérer la création de la table `national_dex`.  
- Ajout d'une gestion des erreurs SQLite et générales avec un système de logs détaillés dans le dossier `logs`.
- Amélioration du fichier `log_error.py` pour enregistrer les erreurs avec des noms de fichiers spécifiques et horodatés.

**Réorganisation de l'Environnement**
- Nettoyage des erreurs liées aux environnements virtuels (`.venv`).
- Ajout des configurations VSCode dans `.vscode/settings.json` pour faciliter le développement et stabiliser les imports :
  - Mise en place de `python.analysis.extraPaths`.
- Exclusion des fichiers inutiles (`__pycache__`, `.vscode`, etc.) via `.gitignore`.

**Corrections de Bugs**
- Résolution des problèmes de non-détection des modules après déplacement ou renommage.
- Ajustements mineurs dans les fichiers de configuration et l'arborescence du projet.

---

### Versions précédentes

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
