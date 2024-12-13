import os
import requests
from PIL import Image
from io import BytesIO
import sqlite3
import json
from datetime import datetime

# --- Configuration des chemins ---
DEFAULT_IMAGE_PATH = os.path.join("assets", "default_image.png")
IMAGES_DIR = os.path.join("assets", "pokemon_images")
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"error-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log")

# --- Traductions des types ---
TYPE_TRANSLATIONS = {
    "Grass": "Plante", "Fire": "Feu", "Water": "Eau", "Electric": "Électrique",
    "Normal": "Normal", "Flying": "Vol", "Poison": "Poison", "Ground": "Sol",
    "Rock": "Roche", "Bug": "Insecte", "Ghost": "Spectre", "Steel": "Acier",
    "Fighting": "Combat", "Psychic": "Psy", "Ice": "Glace", "Dragon": "Dragon",
    "Dark": "Ténèbres", "Fairy": "Fée"
}

# --- Logging ---
def log_error(message):
    """Écrit un message d'erreur dans le fichier de log."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

# --- Téléchargement et sauvegarde des images ---
def download_and_save_image(image_url, filename):
    """Télécharge une image depuis une URL et la sauvegarde localement."""
    file_path = os.path.join(IMAGES_DIR, filename)
    try:
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()

        if not response.headers.get('Content-Type', '').startswith('image/'):
            raise ValueError(f"Le contenu retourné n'est pas une image ({image_url}).")

        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data)
        pil_image.save(file_path)
        return file_path

    except Exception as e:
        log_error(f"Erreur lors du téléchargement de l'image : {e}")
        return DEFAULT_IMAGE_PATH

# --- Fonction pour récupérer les évolutions ---
def fetch_evolution_chain(pokemon_name):
    """Récupère les évolutions pour un Pokémon donné."""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
        response = requests.get(url)
        response.raise_for_status()

        species_data = response.json()
        evolution_chain_url = species_data["evolution_chain"]["url"]

        response = requests.get(evolution_chain_url)
        response.raise_for_status()

        evolution_data = response.json()
        chain = evolution_data["chain"]

        def parse_chain(node):
            """Parcourt la chaîne d'évolution récursivement."""
            result = {
                "name": node["species"]["name"].capitalize(),
                "evolves_to": [parse_chain(evo) for evo in node["evolves_to"]]
            }
            return result

        return parse_chain(chain)

    except Exception as e:
        log_error(f"Erreur lors de la récupération des évolutions pour {pokemon_name} : {e}")
        return None

# --- Enrichissement des données ---
def enrich_pokemon_data(pokemon_id):
    """Enrichit les données d'un Pokémon à partir de l'API."""
    try:
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
        species_response = requests.get(species_url)
        species_response.raise_for_status()

        species_data = species_response.json()
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_response = requests.get(pokemon_url)
        pokemon_response.raise_for_status()

        pokemon_data = pokemon_response.json()

        # Extraire les types
        type1_eng = pokemon_data["types"][0]["type"]["name"].capitalize() if pokemon_data["types"] else None
        type2_eng = pokemon_data["types"][1]["type"]["name"].capitalize() if len(pokemon_data["types"]) > 1 else None
        type1_fr = TYPE_TRANSLATIONS.get(type1_eng, "Inconnu")
        type2_fr = TYPE_TRANSLATIONS.get(type2_eng, "Inconnu")

        # Extraire les statistiques
        stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]}
        hp = stats.get("hp", 0)
        attaque = stats.get("attack", 0)
        defense = stats.get("defense", 0)
        attaque_special = stats.get("special-attack", 0)
        defense_special = stats.get("special-defense", 0)
        vitesse = stats.get("speed", 0)

        # Description
        descriptions = species_data["flavor_text_entries"]
        description_fr = next((entry["flavor_text"] for entry in descriptions if entry["language"]["name"] == "fr"), "")
        description_eng = next((entry["flavor_text"] for entry in descriptions if entry["language"]["name"] == "en"), "")

        # Jeux disponibles
        games_available = json.dumps([game["version"]["name"] for game in pokemon_data["game_indices"]])

        # Forme
        forme = species_data["name"].split("-")[1].capitalize() if "-" in species_data["name"] else "Default"

        # Retour des données enrichies
        return {
            "numero": pokemon_id,
            "nom_eng": species_data["name"].capitalize(),
            "forme": forme,
            "image_url": pokemon_data["sprites"]["front_default"],
            "shiny_image_url": pokemon_data["sprites"].get("front_shiny"),
            "evolutions": json.dumps(fetch_evolution_chain(species_data["name"])),
            "type1_fr": type1_fr,
            "type1_eng": type1_eng,
            "type2_fr": type2_fr,
            "type2_eng": type2_eng,
            "description_fr": description_fr,
            "description_eng": description_eng,
            "hp": hp,
            "attaque": attaque,
            "defense": defense,
            "attaque_special": attaque_special,
            "defense_special": defense_special,
            "vitesse": vitesse,
            "games_available": games_available,
        }

    except Exception as e:
        log_error(f"Erreur d'enrichissement des données pour le Pokémon {pokemon_id} : {e}")
        return None

# --- Population de la base de données ---
def populate_database():
    """Récupère et insère les données de tous les Pokémon dans la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        for pokemon_id in range(1, 1009):  # Limite ajustée selon les besoins
            data = enrich_pokemon_data(pokemon_id)
            if not data:
                continue

            # Téléchargement de l'image locale
            local_image_path = download_and_save_image(data["image_url"], f"{data['numero']}_{data['forme']}.png")
            data["image_url"] = local_image_path

            cursor.execute('''
                INSERT INTO pokemon (
                    numero, image_url, shiny_image_url, nom_fr, nom_eng, forme,
                    evolutions, type1_fr, type1_eng, type2_fr, type2_eng,
                    games_available, locations_per_game, color, category,
                    description_fr, description_eng, hp, attaque, defense,
                    attaque_special, defense_special, vitesse, shiny, capture
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data["numero"], data["image_url"], data["shiny_image_url"], "",
                data["nom_eng"], data["forme"], data["evolutions"], data["type1_fr"], data["type1_eng"],
                data["type2_fr"], data["type2_eng"], data["games_available"], "[]", "",
                "", data["description_fr"], data["description_eng"], data["hp"], data["attaque"],
                data["defense"], data["attaque_special"], data["defense_special"], data["vitesse"], 0, 0
            ))
            conn.commit()
            print(f"Ajouté : {data['nom_eng']} ({data['forme']}) (Numéro {data['numero']})")

    except Exception as e:
        log_error(f"Erreur lors de la population de la base de données : {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    populate_database()
