import sqlite3
import json

def init_db():
    """Initializes the database and creates the tables if they do not exist."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL, -- National number
            name_fr TEXT NOT NULL, -- French name
            name_eng TEXT NOT NULL, -- English name
            image_url TEXT DEFAULT 'https://via.placeholder.com/96?text=No+Image', -- Default image
            shiny_image_url TEXT, -- Shiny image
            form TEXT DEFAULT 'Default', -- Specific form of the Pokémon
            gender TEXT DEFAULT 'Neutral',             -- Sexe ('Male', 'Female', 'Neutral')
            evolutions TEXT, -- JSON containing evolutions
            type1_fr TEXT NOT NULL, -- Primary type in French
            type2_fr TEXT, -- Secondary type in French (nullable)
            type1_eng TEXT NOT NULL, -- Primary type in English
            type2_eng TEXT, -- Secondary type in English (nullable)
            games_available TEXT, -- Games where the Pokémon is available (JSON or list)
            locations_per_game TEXT, -- Specific locations per game (JSON or list)
            color TEXT, -- Main color
            category TEXT, -- Pokémon category (species)
            description_fr TEXT, -- Description in French
            description_eng TEXT, -- Description in English
            hp INTEGER, -- Health points
            attack INTEGER, -- Attack
            defense INTEGER, -- Defense
            special_attack INTEGER, -- Special attack
            special_defense INTEGER, -- Special defense
            speed INTEGER, -- Speed
            shiny INTEGER DEFAULT 0, -- Shiny indicator (0 = not shiny, 1 = shiny)
            captured INTEGER DEFAULT 0 -- Captured indicator (0 = not captured, 1 = captured)
        );
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def load_pokedex():
    """Loads all Pokémon from the database and returns a list of formatted tuples."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            number, name_fr, name_eng, form, evolutions, 
            type1_fr, type2_fr, hp, attack, defense, 
            special_attack, special_defense, speed, 
            shiny, captured, image_url
        FROM pokemon
    ''')
    rows = cursor.fetchall()
    conn.close()

    # Format the data for the table
    formatted_rows = [
        (
            row[0],  # number
            row[1] or "Unknown",  # name_fr
            row[2] or "Unknown",  # name_eng
            row[3] or "Default",  # form
            row[4] if row[4] else "No evolution",  # evolutions
            row[5] or "-",  # type1_fr
            row[6] or "-",  # type2_fr
            row[7] or 0,  # hp
            row[8] or 0,  # attack
            row[9] or 0,  # defense
            row[10] or 0,  # special_attack
            row[11] or 0,  # special_defense
            row[12] or 0,  # speed
            row[13],  # shiny
            row[14],  # captured
            row[15]  # image_url
        )
        for row in rows
    ]
    return formatted_rows

if __name__ == "__main__":
    init_db()
