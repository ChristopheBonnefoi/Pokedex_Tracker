import requests
from functions.log_error import log_error

def fetch_pokemon_gender(pokemon_data):
    """
    Récupère le genre d'un Pokémon à partir des données de l'API PokeAPI.

    Args:
        pokemon_data (dict): Les données du Pokémon issues de PokeAPI.

    Returns:
        str: 'Male', 'Female', ou 'Neutral'.
    """
    try:
        if not pokemon_data or "id" not in pokemon_data:
            return "Neutral"

        # Vérifie si le Pokémon a une séparation par genre
        gender_rate = pokemon_data.get("gender_rate", -1)  # -1 = aucun genre attribué

        if gender_rate == -1:
            return "Neutral"  # Pokémon sans genre (Magnemite, légendaires neutres, etc.)
        elif gender_rate == 8:
            return "Female"  # 100% Femelle
        elif gender_rate == 0:
            return "Male"  # 100% Mâle
        else:
            return "Male/Female"  # Pokémon avec une répartition mâle/femelle (par exemple, 50/50)

    except Exception as e:
        log_error("fetch_pokemon_gender_error", f"Erreur lors de la récupération du genre : {e}")
        return "Neutral"

def fetch_gender_from_pokeapi(pokemon_id):
    """
    Récupère les données de genre d'un Pokémon depuis l'API PokeAPI.

    Args:
        pokemon_id (int): L'identifiant du Pokémon.

    Returns:
        str: 'Male', 'Female', ou 'Neutral'.
    """
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
        response = requests.get(url)
        response.raise_for_status()
        species_data = response.json()

        return fetch_pokemon_gender(species_data)

    except Exception as e:
        log_error("fetch_gender_from_pokeapi_error", f"Erreur pour Pokémon ID {pokemon_id} : {e}")
        return "Neutral"
