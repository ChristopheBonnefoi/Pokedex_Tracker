# Pokedex Tracker

## Changelog

### V0.1.12
#### Résumé des changements

**Gestion des genres des Pokémon**
- Ajout de la gestion des genres (`Male`, `Female`, `Neutral`) dans la base de données.
- Inclusion des informations sur les sprites spécifiques aux genres via l'API.
- Les Pokémon ayant des sprites masculins et féminins distincts sont ajoutés avec une colonne `gender`.
- Pokémon sans distinction de genre sont marqués comme `Neutral`.

**Améliorations des formes**
- Support renforcé pour les formes spécifiques des Pokémon (Alola, Galar, etc.).
- Les formes alternatives sont identifiées et insérées avec des distinctions claires dans la colonne `form`.
- Exemple : gestion des sprites masculins et féminins de Pikachu ainsi que des formes Alola et Galar de Meowth.

**Mise à jour de la structure de la base de données**
- Modification de la structure de la BDD pour inclure la colonne `gender`.
- Ajustement des scripts existants pour intégrer ces nouveaux champs.

**Refactorisation**
- Création de `fetch_gender.py` pour centraliser la gestion des genres et éviter les répétitions dans le code.
- Amélioration de la robustesse des scripts pour éviter les doublons.

---

### Versions précédentes

#### V0.1.11
- Gestion des doublons dans la BDD pour éviter les conflits d'insertion.
- Intégration des formes alternatives des Pokémon (Alola, Galar, Hisui, etc.).
- Refactorisation des scripts pour gérer les formes spécifiques et améliorer la maintenance.

#### V0.1.10
- Ajout de la gestion des types de Pokémon avec traduction en français.
- Mise en place d'un système modulaire pour les traductions via un fichier JSON.
- Création des tests unitaires pour valider les traductions des types.
- Réorganisation des fonctions dans des fichiers dédiés pour faciliter la maintenance.

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
