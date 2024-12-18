import sys
import os
import sqlite3  # Import sqlite3

# Ajouter le chemin racine au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from functions.log_error import log_error

def init_national_dex():
    """Initializes the database and creates the table `national_dex` if it does not exist."""
    try:
        conn = sqlite3.connect('pokedex.sqlite3')  # Database file
        cursor = conn.cursor()

        # Create the `national_dex` table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS national_dex (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL UNIQUE,
                image_url TEXT DEFAULT 'https://via.placeholder.com/96?text=No+Image',
                shiny_image_url TEXT,
                name_fr TEXT NOT NULL,
                name_eng TEXT NOT NULL,
                form TEXT DEFAULT 'Default',
                evolutions_fr TEXT,
                evolutions_eng TEXT,
                type1_fr TEXT NOT NULL,
                type1_eng TEXT NOT NULL,
                type2_fr TEXT,
                type2_eng TEXT,
                games_fr TEXT,
                games_eng TEXT,
                locations_fr TEXT,
                locations_eng TEXT,
                color_fr TEXT,
                color_eng TEXT,
                species_fr TEXT,
                species_eng TEXT,
                description_fr TEXT,
                description_eng TEXT,
                hp INTEGER,
                atk INTEGER,
                def INTEGER,
                atkspe INTEGER,
                defspe INTEGER,
                spd INTEGER,
                shiny INTEGER DEFAULT 0,
                captured INTEGER DEFAULT 0
            );
        ''')
        conn.commit()
        conn.close()
        print("Table `national_dex` created successfully.")
    
    except sqlite3.Error as e:
        log_error("initialize_db_error", f"SQLite Error: {e}")
        print("Error while creating the `national_dex` table.")
    
    except Exception as e:
        log_error("initialize_db_error", f"General Error: {e}")
        print("An unexpected error occurred.")

if __name__ == "__main__":
    init_national_dex()
