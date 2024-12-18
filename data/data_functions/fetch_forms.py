import requests
from functions.log_error import log_error

def fetch_pokemon_forms(pokemon_id):
    """
    Récupère les formes alternatives d'un Pokémon via PokeAPI.
    Args:
        pokemon_id (int): ID du Pokémon.
    Returns:
        list: Liste des formes du Pokémon.
    """
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)
        response.raise_for_status()

        pokemon_data = response.json()
        forms = [form['name'].capitalize() for form in pokemon_data['forms']]

        return forms
    except Exception as e:
        log_error("fetch_forms_error", f"Erreur pour ID {pokemon_id}: {e}")
        return []
