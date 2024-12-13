import sqlite3

def list_tables():
    """Affiche les tables existantes dans la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables existantes :")
    for table in tables:
        print(table[0])

    conn.close()

def check_table_structure():
    """Vérifie et affiche la structure de la table 'pokemon'."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Vérifier si la table 'pokemon' existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pokemon';")
    if cursor.fetchone() is None:
        print("La table 'pokemon' n'existe pas dans la base de données.")
        conn.close()
        return

    # Afficher la structure de la table 'pokemon'
    cursor.execute("PRAGMA table_info(pokemon)")
    columns = cursor.fetchall()

    print("Structure de la table 'pokemon' :")
    for column in columns:
        print(f"Nom : {column[1]}, Type : {column[2]}, NULL : {'Non' if column[3] == 1 else 'Oui'}, Default : {column[4]}")

    conn.close()

def print_column_names():
    """Affiche uniquement les noms des colonnes de la table 'pokemon'."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(pokemon)")
    columns = cursor.fetchall()

    print("Noms des colonnes dans la table 'pokemon' :")
    for column in columns:
        print(column[1])  # Affiche le nom de la colonne

    conn.close()

def fetch_first_rows():
    """Récupère et affiche les 10 premières lignes de la table 'pokemon'."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pokemon LIMIT 10;")  # Récupère les 10 premières lignes
    rows = cursor.fetchall()

    print("Premières lignes de la table 'pokemon' :")
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    # Afficher les tables existantes
    list_tables()

    # Vérifier la structure de la table 'pokemon'
    check_table_structure()

    # Afficher uniquement les noms des colonnes
    print_column_names()

    # Récupérer et afficher les premières lignes
    fetch_first_rows()
