import sys
import os

# Ajoute le chemin racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from data.data_functions.fetch_names import fetch_names_from_pokeapi

def test_fetch_names():
    """
    Teste la récupération des noms anglais et français pour quelques Pokémon.
    """
    test_ids = [1, 4, 7, 25, 1025]  # Exemple : Bulbasaur, Charmander, Squirtle, Pikachu, Mewtwo

    for pokemon_id in test_ids:
        name_eng, name_fr = fetch_names_from_pokeapi(pokemon_id)
        print(f"ID {pokemon_id} - Nom anglais (PokeAPI) : {name_eng}")
        print(f"ID {pokemon_id} - Nom français (PokeAPI) : {name_fr}")

if __name__ == "__main__":
    test_fetch_names()
