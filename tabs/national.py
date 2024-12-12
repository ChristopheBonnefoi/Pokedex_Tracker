import os
from tkinter import ttk, Label, Toplevel
from PIL import Image, ImageTk
from database import load_pokedex  # Charger les Pokémon depuis la base de données

DEFAULT_IMAGE_PATH = os.path.join("assets", "default_image.png")


class NationalTab:
    def __init__(self, notebook):
        # Créer le cadre pour cet onglet
        self.frame = ttk.Frame(notebook)

        # Créer une table pour afficher les Pokémon
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Numéro", "Nom", "Forme", "Shiny", "Capturé", "Image"),
            show="headings"
        )

        # Configuration des colonnes
        self.tree.heading("Numéro", text="Numéro")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Forme", text="Forme")
        self.tree.heading("Shiny", text="Shiny")
        self.tree.heading("Capturé", text="Capturé")
        self.tree.heading("Image", text="Image")

        self.tree.column("Numéro", width=50, anchor="center")
        self.tree.column("Nom", width=150, anchor="center")
        self.tree.column("Forme", width=150, anchor="center")
        self.tree.column("Shiny", width=100, anchor="center")
        self.tree.column("Capturé", width=100, anchor="center")
        self.tree.column("Image", width=150, anchor="center")

        # Ajouter la table à l'onglet
        self.tree.pack(fill="both", expand=True)

        # Dictionnaire pour stocker les images et éviter qu'elles ne soient supprimées
        self.images = {}

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
            numero, forme, image_path, nom_eng, shiny_flag, capture_flag = pokemon

            # Charger l'image depuis le chemin local
            image = self.fetch_image(image_path)
            if image:
                self.images[numero] = image  # Préserver l'image

            # Convertir les booléens shiny et capture en symboles ✔️ ou ❌
            shiny = "✔️" if shiny_flag else "❌"
            capture = "✔️" if capture_flag else "❌"

            # Ajouter la ligne dans le tableau
            self.tree.insert("", "end", values=(numero, nom_eng, forme, shiny, capture, f"Voir Image {numero}"))

        # Ajouter un événement pour afficher l'image en popup
        self.tree.bind("<ButtonRelease-1>", self.show_image_popup)

    def fetch_image(self, image_path):
        """Charge une image depuis un chemin local ou utilise une image par défaut."""
        try:
            pil_image = Image.open(image_path).resize((96, 96))
            return ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image {image_path} : {e}. Utilisation de l'image par défaut.")
            return self.load_default_image()

    def load_default_image(self):
        """Charge une image par défaut locale."""
        try:
            pil_image = Image.open(DEFAULT_IMAGE_PATH).resize((96, 96))
            return ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image par défaut : {e}")
            return None

    def show_image_popup(self, event):
        """Affiche une image en popup lorsqu'une ligne est cliquée."""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            numero = int(values[0])  # Récupérer le numéro du Pokémon
            image = self.images.get(numero)

            if image:
                popup = Toplevel(self.frame)
                popup.title(f"Image de Pokémon #{numero}")
                label = Label(popup, image=image)
                label.image = image  # Préserver l'image
                label.pack()
