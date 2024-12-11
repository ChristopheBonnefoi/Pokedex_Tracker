import sqlite3
import requests
import json

def is_pokemon_form_in_database(conn, numero, forme):
    """Vérifie si une forme spécifique d'un Pokémon est déjà présente dans la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pokemon WHERE numero = ? AND forme = ?", (numero, forme))
    return cursor.fetchone() is not None

def extract_form(variety_name):
    """Extrait la forme à partir du suffixe du nom."""
    suffix = variety_name.split("-")[1] if "-" in variety_name else "default"
    return suffix.capitalize() if suffix != "default" else "Default"

def fetch_pokemon_data(pokemon_id):
    """Récupère les données principales et les formes d'un Pokémon depuis PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur : Impossible de récupérer les données pour le Pokémon {pokemon_id}. Script arrêté.")
        exit(1)

    species_data = response.json()
    varieties = species_data["varieties"]

    forms = []
    for variety in varieties:
        variety_name = variety["pokemon"]["name"]  # Nom complet (ex. rattata-alola)
        base_name = variety_name.split("-")[0].capitalize()  # Récupère le nom principal (avant le suffixe)
        forme = extract_form(variety_name)  # Détecte automatiquement la forme

        # Récupérer l'URL de l'image pour cette forme
        pokemon_url = variety["pokemon"]["url"]
        pokemon_response = requests.get(pokemon_url)
        if pokemon_response.status_code != 200:
            print(f"Erreur : Impossible de récupérer les données pour {variety_name}.")
            continue

        pokemon_data = pokemon_response.json()
        image_url = pokemon_data["sprites"]["front_default"]  # Image spécifique de la forme
        if not image_url:  # Si aucune image disponible, utiliser une URL par défaut
            image_url = "https://via.placeholder.com/96?text=No+Image"

        forms.append({
            "numero": pokemon_id,
            "forme": forme,
            "nom_eng": base_name,
            "image_url": image_url
        })

    return forms


def populate_database():
    """Récupère et insère tous les Pokémon et leurs formes jusqu'à Paldea DLC inclus."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Récupérer tous les Pokémon disponibles
    url = "https://pokeapi.co/api/v2/pokemon?limit=2000"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur : Impossible de récupérer la liste des Pokémon. Script arrêté.")
        exit(1)

    all_pokemon = response.json()["results"]
    for index, pokemon in enumerate(all_pokemon, start=1):
        forms = fetch_pokemon_data(index)

        for form in forms:
            # Vérifier si la forme est déjà présente dans la base
            if is_pokemon_form_in_database(conn, form["numero"], form["forme"]):
                print(f"Forme {form['forme']} du Pokémon {form['nom_eng']} déjà présente, ignorée.")
                continue

            # Insérer les données dans la base
            cursor.execute('''
                INSERT INTO pokemon (numero, forme, image_url, nom_fr, nom_eng, type1, type2, hp, attaque, defense, jeux_disponibles)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                form["numero"],
                form["forme"],  # Cette valeur est dynamiquement détectée
                form["image_url"],
                "",  # Le nom en français sera rempli plus tard
                form["nom_eng"],
                "",  # Types remplis plus tard
                "",  # Types remplis plus tard
                0,   # HP temporaire
                0,   # Attaque temporaire
                0,   # Défense temporaire
                "[]" # Jeux disponibles temporairement vide
            ))

            print(f"Ajouté : {form['nom_eng']} ({form['forme']}) (Numéro {form['numero']})")
            conn.commit()

    conn.close()
    print("Tous les Pokémon et leurs formes ont été ajoutés ou mis à jour dans la base de données.")

if __name__ == "__main__":
    populate_database()
