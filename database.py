import sqlite3

def init_db():
    """Initialise la base de données et crée les tables si elles n'existent pas."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Création de la table `pokemon` si elle n'existe pas déjà
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL,
            image_url TEXT DEFAULT 'https://via.placeholder.com/96?text=No+Image',  -- Valeur par défaut
            nom_fr TEXT NOT NULL,
            nom_eng TEXT NOT NULL,
            forme TEXT DEFAULT 'Default',  -- Colonne pour gérer les formes
            evolutions TEXT,  -- Champs JSON pour les évolutions
            type1 TEXT NOT NULL,
            type2 TEXT,
            hp INTEGER,
            attaque INTEGER,
            defense INTEGER,
            jeux_disponibles TEXT,
            shiny INTEGER DEFAULT 0,
            capture INTEGER DEFAULT 0
        )
    ''')

def load_pokedex():
    """Charge les Pokémon depuis la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT numero, forme, image_url, nom_eng, shiny, capture
        FROM pokemon
    ''')
    pokemons = cursor.fetchall()
    conn.close()
    return pokemons



if __name__ == "__main__":
    init_db()
    print("Base de données initialisée avec succès.")
