# Pokedex Tracker

## Changelog

### V0.1.11
#### Résumé des changements

**Gestion des doublons dans la BDD**
- Ajout d'une vérification pour éviter l'insertion en double des Pokémon dans la base de données.
- Si un Pokémon avec le même ID existe déjà, il est ignoré afin de prévenir les doublons.

**Prise en charge des formes alternatives des Pokémon**
- Intégration des formes spécifiques des Pokémon (Alola, Galar, Hisui, etc.) via l'API.
- Chaque forme est insérée avec un nom, un ID unique, et une mention de la forme dans la colonne `form`.
- Exemple de gestion pour **Mewtwo** avec ses formes normales et **Gigantamax**.
- Support similaire pour **Meowth** (formes Alola et Galar).

**Améliorations des scripts**
- Refactorisation des fonctions dans `fetch_forms.py` pour récupérer et traiter les formes alternatives.
- Mise à jour du script `data_manager.py` pour intégrer la gestion des formes et éviter les conflits d'insertion.

---

### Versions précédentes

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
