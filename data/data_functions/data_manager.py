import sqlite3
import sys
import os

# Ajoute le chemin racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)
    
from data.data_functions.fetch_names import fetch_names_from_pokeapi
from data.data_functions.fetch_types import fetch_types_from_pokeapi, translate_type_to_french
from functions.log_error import log_error

def update_pokemon_names(max_attempts=3000):
    """
    Met à jour les noms anglais et français et les types des Pokémon dans la base de données.
    - Arrête le script si un ID dépasse les données disponibles (pour anticiper les ajouts).
    """
    try:
        conn = sqlite3.connect('pokedex.sqlite3')
        cursor = conn.cursor()

        for pokemon_id in range(1, max_attempts + 1):  # Tente jusqu'à 3000 Pokémon
            try:
                # Récupérer les noms depuis PokeAPI
                name_eng, name_fr, pokemon_data = fetch_names_from_pokeapi(pokemon_id)

                # Si aucun nom n'est trouvé, on stoppe le script
                if not name_eng and not name_fr:
                    print(f"ID {pokemon_id} : Aucun nom trouvé. Fin du script, base à jour.")
                    break

                # Récupérer les types
                type1_eng, type2_eng = fetch_types_from_pokeapi(pokemon_data)
                type1_fr = translate_type_to_french(type1_eng)
                type2_fr = translate_type_to_french(type2_eng)

                # Mise à jour ou insertion dans la BDD
                cursor.execute('''
                    INSERT INTO national_dex (number, name_eng, name_fr, type1_eng, type1_fr, type2_eng, type2_fr)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(number) DO UPDATE SET 
                        name_eng = excluded.name_eng,
                        name_fr = excluded.name_fr,
                        type1_eng = excluded.type1_eng,
                        type1_fr = excluded.type1_fr,
                        type2_eng = excluded.type2_eng,
                        type2_fr = excluded.type2_fr
                ''', (pokemon_id, name_eng, name_fr, type1_eng, type1_fr, type2_eng, type2_fr))
                conn.commit()

                print(f"ID {pokemon_id} - Noms et types mis à jour : {name_eng}/{name_fr}, {type1_fr}, {type2_fr}")

            except Exception as e:
                log_error("update_pokemon_names_error", f"Erreur pour ID {pokemon_id} : {e}")
                print(f"Erreur lors de la mise à jour pour l'ID {pokemon_id}")

    except sqlite3.Error as e:
        log_error("database_connection_error", f"Erreur SQLite : {e}")
    finally:
        conn.close()
        print("Mise à jour des noms et types terminée.")

if __name__ == "__main__":
    update_pokemon_names()
