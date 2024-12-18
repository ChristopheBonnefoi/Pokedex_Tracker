# Documentation des Tests Unitaires - Pokedex Tracker

Ce fichier explique comment exécuter et gérer les tests unitaires du projet **Pokedex Tracker**.

---

## Structure des Tests

Les tests unitaires sont situés dans le dossier `debug_tools/tests` pour faciliter leur identification.

**Emplacement :**

```
debug_tools/ └── tests/ ├── test_fetch_names.py # Test des fonctions pour récupérer les noms ├── test_fetch_types.py # Test des fonctions pour récupérer et traduire les types └── ...
```


---

## Lancer les Tests

### Prérequis
Assure-toi que :
1. **L'environnement virtuel** est activé :
   ```bash
   .venv\Scripts\activate  # Sous Windows
   source .venv/bin/activate  # Sous Linux/macOS

2. Les dépendances nécessaires sont installées :
    ```
    pip install -r requirements.txt
    ```

### Exécuter les Tests Individuels
    Pour exécuter un fichier de test spécifique, utilise :

    ```
    python debug_tools/tests/test_fetch_names.py
    ```

### Exécuter Tous les Tests
    Tu peux lancer tous les tests présents dans le dossier tests en utilisant unittest avec la commande suivante :

    ```
    python -m unittest discover debug_tools/tests
    ```

### Résultats Attendus
    Lorsque les tests sont exécutés, les résultats sont affichés dans le terminal. Voici un exemple de sortie réussie :

    ```
        ..
        ----------------------------------------------------------------------
        Ran 2 tests in 0.001s

        OK
     ```

    ** Signification : **
    . : Un test réussi.
    F : Un test a échoué (Fail).
    E : Une erreur s'est produite lors du test.

## Tests Disponibles

### 1. test_fetch_names.py
    Objectif : Vérifier que les noms anglais et français des Pokémon sont récupérés correctement via PokeAPI.

### 2. test_fetch_types.py
    Objectif : Tester la fonction de traduction des types anglais en français.

        Cas testés :
            Types existants ("Grass" → "Plante").
            Type inconnu ("Unknown" → "Inconnu").
            Valeurs vides ou nulles.


## Ajouter de Nouveaux Tests
    Pour ajouter de nouveaux tests :

        1. Crée un fichier dans debug_tools/tests/ avec le préfixe test_ :
       
        ```
        # Exemple : test_new_function.py
        import unittest
        from data.data_functions.new_function import new_function

        class TestNewFunction(unittest.TestCase):
            def test_case_1(self):
                self.assertEqual(new_function("input"), "expected_output")

        if __name__ == "__main__":
            unittest.main()
        ```

        2. Lance les tests pour vérifier :

        ```
        python -m unittest discover debug_tools/tests
        ```

## Bonnes Pratiques
    - Nommer les tests clairement : Utilise des noms descriptifs pour chaque méthode.
    - Modularité : Chaque fichier de test doit tester une seule fonctionnalité.
    - Utiliser des assertions : self.assertEqual, self.assertTrue, etc.
    - Ajouter des commentaires/docstrings : Explique l'objectif de chaque test.


##Dépannage
    1. Problème d'importation (ModuleNotFoundError)
        Vérifie que le chemin racine est ajouté au sys.path dans les scripts de test.

    2. Problèmes liés à l'environnement virtuel
        Assure-toi que le bon interpréteur est activé dans VSCode.
        Vérifie que l'environnement virtuel est activé avec :
        ```
        .venv\Scripts\activate
        ```