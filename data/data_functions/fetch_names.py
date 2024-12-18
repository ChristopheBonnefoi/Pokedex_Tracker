import requests
import sys
import os

# Ajouter le chemin racine au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from functions.log_error import log_error

def fetch_names_from_pokeapi(pokemon_id):
    """
    Récupère les noms anglais et français d'un Pokémon depuis PokeAPI.
    Retourne : (name_eng, name_fr, pokemon_data)
    """
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)
        response.raise_for_status()
        pokemon_data = response.json()

        name_eng = pokemon_data["name"].capitalize()

        # Récupérer le nom français depuis les "species"
        species_url = pokemon_data["species"]["url"]
        species_response = requests.get(species_url)
        species_response.raise_for_status()
        species_data = species_response.json()

        name_fr = next(
            (entry["name"] for entry in species_data["names"] if entry["language"]["name"] == "fr"), "Inconnu"
        )

        return name_eng, name_fr, pokemon_data

    except Exception as e:
        log_error("fetch_names_error", f"Erreur pour ID {pokemon_id} : {e}")
        return None, None, None
