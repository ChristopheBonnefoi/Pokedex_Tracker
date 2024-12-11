import sqlite3

import sqlite3

def init_db():
    """Initialise la base de données et crée les tables si elles n'existent pas."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Création de la table `pokemon`
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            nom_fr TEXT NOT NULL,
            nom_eng TEXT NOT NULL,
            type1 TEXT NOT NULL,
            type2 TEXT,
            hp INTEGER,
            attaque INTEGER,
            defense INTEGER,
            formes TEXT,
            evolutions TEXT,
            jeux_disponibles TEXT,
            shiny INTEGER DEFAULT 0,
            capture INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def load_pokedex():
    """Charge tous les Pokémon de la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Récupérer toutes les données de la table `pokemon`
    cursor.execute("SELECT numero, image_url, nom_fr, nom_eng, type1, type2, hp, attaque, defense, shiny, capture FROM pokemon")
    pokemons = cursor.fetchall()
    conn.close()

    # Retourne les données sous forme de liste de tuples
    return pokemons

def add_pokemon(numero, nom_eng, jeux_disponibles):
    """Ajoute un Pokémon à la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pokemon (numero, image_url, nom_fr, nom_eng, type1, type2, hp, attaque, defense, jeux_disponibles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        numero,
        f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png',  # URL de l'image
        nom_eng,  # Nom en français, temporairement rempli avec nom_eng
        nom_eng,  # Nom en anglais
        'Normal',  # Type principal, exemple par défaut
        None,  # Type secondaire
        50,  # HP par défaut
        50,  # Attaque par défaut
        50,  # Défense par défaut
        jeux_disponibles  # Jeux disponibles
    ))
    conn.commit()
    conn.close()
