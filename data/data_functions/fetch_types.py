import json
import os

# Charger les traductions des types depuis le JSON
TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), "type_translations.json")

def load_type_translations():
    """
    Charge les traductions des types depuis le fichier JSON.
    Retourne un dictionnaire avec les types traduits.
    """
    try:
        with open(TRANSLATIONS_PATH, "r", encoding="utf-8") as file:
            translations = json.load(file)
        return translations
    except Exception as e:
        print(f"Erreur lors du chargement des traductions des types : {e}")
        return {}

TYPE_TRANSLATIONS = load_type_translations()

def fetch_types_from_pokeapi(pokemon_data):
    """
    Récupère les types d'un Pokémon depuis les données de l'API.
    Retourne une paire (type1, type2) avec des valeurs par défaut si manquantes.
    """
    type1 = "Inconnu"  # Valeur par défaut pour type1
    type2 = None       # Valeur par défaut pour type2

    if pokemon_data.get("types"):
        types = pokemon_data["types"]
        if len(types) > 0:
            type1 = types[0]["type"]["name"].capitalize()
        if len(types) > 1:
            type2 = types[1]["type"]["name"].capitalize()
    return type1, type2

def translate_type_to_french(type_eng):
    """
    Traduit un type anglais en français en utilisant le dictionnaire TYPE_TRANSLATIONS.
    Retourne 'Inconnu' si le type n'est pas trouvé.
    """
    return TYPE_TRANSLATIONS.get(type_eng, "Inconnu")

if __name__ == "__main__":
    # Exemple de test
    print("Test de traduction des types :")
    print(f"Grass → {translate_type_to_french('Grass')}")
    print(f"Fire → {translate_type_to_french('Fire')}")
    print(f"Unknown → {translate_type_to_french('Unknown')}")
