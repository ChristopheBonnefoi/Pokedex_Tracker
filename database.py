import sqlite3
import json

def init_db():
    """Initialise la base de données et crée les tables si elles n'existent pas."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL,
            image_url TEXT DEFAULT 'https://via.placeholder.com/96?text=No+Image',
            shiny_image_url TEXT,
            nom_fr TEXT NOT NULL,
            nom_eng TEXT NOT NULL,
            forme TEXT DEFAULT 'Default',
            evolutions TEXT,
            type1_fr TEXT NOT NULL,
            type1_eng TEXT NOT NULL,
            type2_fr TEXT,
            type2_eng TEXT,
            games_available TEXT,
            locations_per_game TEXT,
            color TEXT,
            category TEXT,
            description_fr TEXT,
            description_eng TEXT,
            hp INTEGER,
            attaque INTEGER,
            defense INTEGER,
            attaque_special INTEGER,
            defense_special INTEGER,
            vitesse INTEGER,
            shiny INTEGER DEFAULT 0,
            capture INTEGER DEFAULT 0
        );
    ''')
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")

def load_pokedex():
    """Charge tous les Pokémon depuis la base de données et retourne une liste de tuples formatés."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            numero, nom_fr, nom_eng, forme, evolutions, 
            type1_fr, type2_fr, hp, attaque, defense, 
            attaque_special, defense_special, vitesse, 
            shiny, capture, image_url
        FROM pokemon
    ''')
    rows = cursor.fetchall()
    conn.close()

    # Formater les données pour le tableau
    formatted_rows = [
        (
            row[0],  # numero
            row[1] or "Inconnu",  # nom_fr
            row[2] or "Unknown",  # nom_eng
            row[3] or "Default",  # forme
            row[4] if row[4] else "Aucune évolution",  # evolutions
            row[5] or "-",  # type1_fr
            row[6] or "-",  # type2_fr
            row[7] or 0,  # hp
            row[8] or 0,  # attaque
            row[9] or 0,  # defense
            row[10] or 0,  # attaque_special
            row[11] or 0,  # defense_special
            row[12] or 0,  # vitesse
            row[13],  # shiny
            row[14],  # capture
            row[15]  # image_url
        )
        for row in rows
    ]
    return formatted_rows

if __name__ == "__main__":
    init_db()
