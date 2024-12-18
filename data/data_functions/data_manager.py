import sqlite3
import sys
import os

# Ajoute le chemin racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from data.data_functions.fetch_names import fetch_names_from_pokeapi
from data.data_functions.fetch_types import fetch_types_from_pokeapi, translate_type_to_french
from data.data_functions.fetch_forms import fetch_pokemon_forms
from functions.log_error import log_error


def pokemon_exists(cursor, pokemon_id, form="Default"):
    """
    Vérifie si un Pokémon existe déjà dans la base de données avec une forme spécifique.
    Args:
        cursor: Objet curseur pour la base de données SQLite.
        pokemon_id (int): ID du Pokémon.
        form (str): Forme spécifique du Pokémon.
    Returns:
        bool: True si le Pokémon avec cette forme existe, False sinon.
    """
    cursor.execute(
        "SELECT 1 FROM national_dex WHERE number = ? AND form = ?",
        (pokemon_id, form),
    )
    return cursor.fetchone() is not None


def update_pokemon_data(max_attempts=3000):
    """
    Met à jour les noms, types et formes des Pokémon dans la base de données.
    - Arrête le script si un ID dépasse les données disponibles.
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('pokedex.sqlite3')
        cursor = conn.cursor()

        # Boucle sur chaque ID pour récupérer les données
        for pokemon_id in range(1, max_attempts + 1):
            try:
                # Récupération des noms depuis PokeAPI
                name_eng, name_fr, pokemon_data = fetch_names_from_pokeapi(pokemon_id)

                # Si aucun nom n'est trouvé, on stoppe l'exécution
                if not name_eng and not name_fr:
                    print(f"ID {pokemon_id} : Aucun nom trouvé. Fin du script, base à jour.")
                    break

                # Récupération des types
                type1_eng, type2_eng = fetch_types_from_pokeapi(pokemon_data)
                type1_fr = translate_type_to_french(type1_eng)
                type2_fr = translate_type_to_french(type2_eng)

                # Récupération des formes
                forms = fetch_pokemon_forms(pokemon_id)

                # Boucle sur chaque forme spécifique du Pokémon
                for form in forms:
                    # Vérification de l'existence pour éviter les doublons
                    if pokemon_exists(cursor, pokemon_id, form):
                        print(f"ID {pokemon_id} ({form}) : Existe déjà. Ignoré.")
                        continue

                    # Insertion dans la base de données
                    cursor.execute('''
                        INSERT INTO national_dex (
                            number, name_eng, name_fr, type1_eng, type1_fr, type2_eng, type2_fr, form
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (pokemon_id, name_eng, name_fr, type1_eng, type1_fr, type2_eng, type2_fr, form))
                    conn.commit()

                    print(f"ID {pokemon_id} - Forme ajoutée : {form}, Types : {type1_fr}, {type2_fr}")

            except Exception as e:
                log_error("update_pokemon_data_error", f"Erreur pour ID {pokemon_id} : {e}")
                print(f"Erreur lors de la mise à jour pour l'ID {pokemon_id}")

    except sqlite3.Error as e:
        log_error("database_connection_error", f"Erreur SQLite : {e}")
    finally:
        # Fermeture de la connexion
        conn.close()
        print("Mise à jour des données terminée.")


if __name__ == "__main__":
    update_pokemon_data()
