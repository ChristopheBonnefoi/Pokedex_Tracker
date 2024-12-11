import tkinter as tk  # Import de tkinter comme tk
from tkinter import ttk  # Import de ttk pour les widgets avancés
from tabs.national import NationalTab  # Importer l'onglet Pokédex National
from database import init_db, add_pokemon  # Base de données

# Initialisation de la base de données
init_db()

# Ajouter des données de test (si nécessaire)
add_pokemon(1, 'Bulbasaur', 'Red, Blue')
add_pokemon(4, 'Charmander', 'Red, Blue')
add_pokemon(7, 'Squirtle', 'Red, Blue')

def create_app():
    root = tk.Tk()  # Initialisation de la fenêtre principale
    root.title("Pokédex Tracker")  # Titre de l'application

    # Création du Notebook (onglets)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Ajouter l'onglet Pokédex National
    national_tab = NationalTab(notebook)
    notebook.add(national_tab.frame, text="Pokédex National")

    root.mainloop()  # Démarrage de l'application

if __name__ == "__main__":
    create_app()
