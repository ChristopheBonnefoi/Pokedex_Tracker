import sqlite3
import requests
import json

def is_pokemon_in_database(conn, numero):
    """Vérifie si un Pokémon est déjà présent dans la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pokemon WHERE numero = ?", (numero,))
    return cursor.fetchone() is not None

def fetch_pokemon_data(pokemon_id):
    """Récupère les données principales d'un Pokémon depuis PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur : Impossible de récupérer les données pour le Pokémon {pokemon_id}. Script arrêté.")
        exit(1)  # Arrêter le script immédiatement en cas d'erreur critique

    data = response.json()
    return {
        "numero": data["id"],
        "image_url": data["sprites"]["front_default"],  # URL de l'image principale
        "nom_eng": data["name"].capitalize(),  # Nom en anglais
        "nom_fr": fetch_french_name(pokemon_id),  # Nom en français
        "type1": data["types"][0]["type"]["name"].capitalize(),  # Type principal
        "type2": data["types"][1]["type"]["name"].capitalize() if len(data["types"]) > 1 else None,  # Type secondaire
        "hp": data["stats"][0]["base_stat"],  # Points de vie
        "attaque": data["stats"][1]["base_stat"],  # Attaque
        "defense": data["stats"][2]["base_stat"],  # Défense
        "jeux_disponibles": json.dumps([version["version"]["name"] for version in data["game_indices"]])  # Jeux
    }

def fetch_french_name(pokemon_id):
    """Récupère le nom en français d'un Pokémon depuis l'API des espèces."""
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur : Impossible de récupérer le nom en français pour le Pokémon {pokemon_id}. Script arrêté.")
        exit(1)  # Arrêter le script immédiatement en cas d'erreur critique

    data = response.json()
    for name in data["names"]:
        if name["language"]["name"] == "fr":
            return name["name"]
    return None

def populate_database():
    """Récupère et insère tous les Pokémon jusqu'à Paldea DLC inclus."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Récupérer tous les Pokémon disponibles
    url = "https://pokeapi.co/api/v2/pokemon?limit=2000"  # Tous les Pokémon
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur : Impossible de récupérer la liste des Pokémon. Script arrêté.")
        exit(1)  # Arrêter le script immédiatement en cas d'erreur critique

    all_pokemon = response.json()["results"]
    for index, pokemon in enumerate(all_pokemon, start=1):
        # Vérifier si le Pokémon est déjà dans la base
        if is_pokemon_in_database(conn, index):
            print(f"Pokémon {index} déjà présent dans la base, mise à jour ignorée.")
            continue

        # Récupérer les données du Pokémon
        data = fetch_pokemon_data(index)
        if not data:
            print(f"Erreur lors de la récupération des données pour le Pokémon {index}. Script arrêté.")
            exit(1)  # Arrêter le script immédiatement en cas d'erreur critique

        # Insérer les données dans la base
        cursor.execute('''
            INSERT INTO pokemon (numero, image_url, nom_fr, nom_eng, type1, type2, hp, attaque, defense, jeux_disponibles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["numero"],
            data["image_url"],
            data["nom_fr"] or "",  # Parfois, le nom en français peut être absent
            data["nom_eng"],
            data["type1"],
            data["type2"],
            data["hp"],
            data["attaque"],
            data["defense"],
            data["jeux_disponibles"]
        ))

        print(f"Ajouté : {data['nom_fr'] or data['nom_eng']} (Numéro {data['numero']})")
        conn.commit()

    conn.close()
    print("Tous les Pokémon ont été ajoutés ou mis à jour dans la base de données.")

if __name__ == "__main__":
    populate_database()
