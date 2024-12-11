from tkinter import ttk
from database import load_pokedex  # Charger les Pokémon depuis la base de données

class NationalTab:
    def __init__(self, notebook):
        # Créer le cadre pour cet onglet
        self.frame = ttk.Frame(notebook)

        # Créer une table pour afficher les Pokémon
        self.tree = ttk.Treeview(self.frame, columns=("Numéro", "Nom", "Jeux", "Shiny", "Capturé"), show="headings")
        
        # Configuration des colonnes
        self.tree.heading("Numéro", text="Numéro")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Jeux", text="Jeux Disponibles")
        self.tree.heading("Shiny", text="Shiny")
        self.tree.heading("Capturé", text="Capturé")
        
        self.tree.column("Numéro", width=50, anchor="center")
        self.tree.column("Nom", width=150, anchor="center")
        self.tree.column("Jeux", width=200, anchor="center")
        self.tree.column("Shiny", width=100, anchor="center")
        self.tree.column("Capturé", width=100, anchor="center")

        # Ajouter la table à l'onglet
        self.tree.pack(fill="both", expand=True)

        # Charger les données initiales
        self.refresh_table()

    def refresh_table(self):
        """Recharge les données depuis la base de données et met à jour la table."""
        # Vider les anciennes données
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Charger les Pokémon depuis la base de données
        pokemons = load_pokedex()
        for pokemon in pokemons:
            # Convertir les booléens shiny et capture en symboles ✔️ ou ❌
            shiny = "✔️" if pokemon[3] else "❌"
            capture = "✔️" if pokemon[4] else "❌"
            self.tree.insert("", "end", values=(pokemon[0], pokemon[1], pokemon[2], shiny, capture))
