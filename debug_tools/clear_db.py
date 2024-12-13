import sqlite3

def reset_table():
    """Vide la table `pokemon` et réinitialise les IDs à 1."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Supprimer toutes les données de la table
    cursor.execute("DELETE FROM pokemon")
    conn.commit()  # Valider les suppressions

    # Réinitialiser l'auto-incrémentation
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='pokemon'")
    conn.commit()  # Valider la réinitialisation

    conn.close()
    print("Table `pokemon` vidée et IDs réinitialisés à 1.")

if __name__ == "__main__":
    reset_table()
