import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
import sqlite3
import json

# Chemin de l'image par défaut
DEFAULT_IMAGE_PATH = os.path.join("assets", "default_image.png")
IMAGES_DIR = os.path.join("assets", "pokemon_images")  # Dossier des images locales

def download_and_save_image(image_url, filename):
    """Télécharge une image depuis une URL et la sauvegarde localement, ou utilise une image par défaut."""
    file_path = os.path.join(IMAGES_DIR, filename)

    print(f"Téléchargement de l'image pour : {image_url}")
    print(f"Chemin cible : {file_path}")

    try:
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()

        # Vérifier le contenu retourné
        if not response.headers.get('Content-Type', '').startswith('image/'):
            print(f"Erreur : le contenu retourné n'est pas une image ({image_url}). Utilisation de l'image par défaut.")
            return DEFAULT_IMAGE_PATH

        # Sauvegarder l'image téléchargée
        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data)
        pil_image.save(file_path)
        print(f"Image sauvegardée avec succès dans {file_path}")
        return file_path

    except Exception as e:
        print(f"Erreur lors du téléchargement ou de la sauvegarde de l'image : {e}")
        return DEFAULT_IMAGE_PATH


def load_default_image():
    """Charge une image par défaut locale."""
    try:
        pil_image = Image.open(DEFAULT_IMAGE_PATH).resize((96, 96))  # Redimensionne l'image
        return ImageTk.PhotoImage(pil_image)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image locale par défaut : {e}")
        return None

def is_pokemon_form_in_database(conn, numero, forme):
    """Vérifie si une forme spécifique d'un Pokémon est déjà présente dans la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pokemon WHERE numero = ? AND forme = ?", (numero, forme))
    return cursor.fetchone() is not None

def extract_form(variety_name):
    """Extrait la forme à partir du suffixe du nom."""
    suffix = variety_name.split("-")[1] if "-" in variety_name else "default"
    return suffix.capitalize() if suffix != "default" else "Default"

def fetch_evolution_chain(pokemon_name):
    """Récupère les évolutions pour un Pokémon donné."""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
        response = requests.get(url)
        response.raise_for_status()

        species_data = response.json()
        evolution_chain_url = species_data["evolution_chain"]["url"]

        # Récupérer la chaîne d'évolution
        response = requests.get(evolution_chain_url)
        response.raise_for_status()

        evolution_data = response.json()
        chain = evolution_data["chain"]

        def parse_chain(node):
            """Parcourt la chaîne d'évolution récursivement."""
            result = {
                "name": node["species"]["name"].capitalize(),
                "evolves_to": []
            }
            for evo in node["evolves_to"]:
                result["evolves_to"].append(parse_chain(evo))
            return result

        return parse_chain(chain)

    except Exception as e:
        print(f"Erreur lors de la récupération des évolutions pour {pokemon_name} : {e}")
        return None

def fetch_pokemon_data(pokemon_id):
    """Récupère les données principales et les formes d'un Pokémon depuis PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur : Impossible de récupérer les données pour le Pokémon {pokemon_id}.")
        return []

    species_data = response.json()
    varieties = species_data["varieties"]

    forms = []
    for variety in varieties:
        variety_name = variety["pokemon"]["name"]  # Nom complet (ex. rattata-alola)
        base_name = variety_name.split("-")[0].capitalize()  # Récupère le nom principal (avant le suffixe)
        forme = extract_form(variety_name)  # Détecte automatiquement la forme

        # URL de l'image spécifique à cette forme
        pokemon_url = variety["pokemon"]["url"]
        response = requests.get(pokemon_url)
        pokemon_data = response.json()
        image_url = pokemon_data["sprites"]["front_default"]

        # Récupérer les évolutions
        evolutions = fetch_evolution_chain(base_name)

        forms.append({
            "numero": pokemon_id,
            "forme": forme,
            "nom_eng": base_name,
            "image_url": image_url,
            "evolutions": json.dumps(evolutions)  # Convertir les évolutions en JSON
        })

    return forms

def populate_database():
    """Récupère et insère tous les Pokémon et leurs formes dans la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    url = "https://pokeapi.co/api/v2/pokemon?limit=2000"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur : Impossible de récupérer la liste des Pokémon.")
        return

    all_pokemon = response.json()["results"]
    for index, pokemon in enumerate(all_pokemon, start=1):
        forms = fetch_pokemon_data(index)

        for form in forms:
            if is_pokemon_form_in_database(conn, form["numero"], form["forme"]):
                print(f"Forme {form['forme']} du Pokémon {form['nom_eng']} déjà présente, ignorée.")
                continue

            local_image_path = download_and_save_image(form["image_url"], f"{form['numero']}_{form['forme']}.png")

            cursor.execute('''
                INSERT INTO pokemon (numero, forme, image_url, nom_fr, nom_eng, type1, type2, hp, attaque, defense, evolutions, jeux_disponibles)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                form["numero"], form["forme"], local_image_path, "", form["nom_eng"], "",
                "", 0, 0, 0, form["evolutions"], "[]"
            ))
            print(f"Ajouté : {form['nom_eng']} ({form['forme']}) (Numéro {form['numero']})")
            conn.commit()

    conn.close()
    print("Base de données mise à jour avec succès.")

if __name__ == "__main__":
    populate_database()

