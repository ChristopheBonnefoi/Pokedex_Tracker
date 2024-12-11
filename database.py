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
            type1 TEXT NOT NULL,
            type2 TEXT,
            hp INTEGER,
            attaque INTEGER,
            defense INTEGER,
            evolutions TEXT,  -- Champs JSON pour les évolutions
            jeux_disponibles TEXT,
            shiny INTEGER DEFAULT 0,
            capture INTEGER DEFAULT 0
        )
    ''')

    # Supprimer la colonne `formes` si elle existe
    cursor.execute("PRAGMA table_info(pokemon)")
    columns = [col[1] for col in cursor.fetchall()]
    if "formes" in columns:
        print("Suppression de la colonne `formes`.")        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon_new AS
            SELECT id, numero, image_url, nom_fr, nom_eng, forme, type1, type2, hp, attaque, defense, evolutions, jeux_disponibles, shiny, capture
            FROM pokemon
        ''')
        cursor.execute("DROP TABLE pokemon")
        cursor.execute("ALTER TABLE pokemon_new RENAME TO pokemon")
        print("Colonne `formes` supprimée avec succès.")

    conn.commit()
    conn.close()



if __name__ == "__main__":
    init_db()
    print("Base de données initialisée avec succès.")
