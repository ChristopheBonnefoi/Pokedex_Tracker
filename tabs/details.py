import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import json
import requests
from io import BytesIO

def fetch_pokemon_details(pokemon_name):
    """Récupère les détails d'un Pokémon depuis la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT numero, nom_eng, forme, evolutions, image_url FROM pokemon WHERE nom_eng = ?', (pokemon_name,))
    data = cursor.fetchone()
    conn.close()
    return data

def parse_evolutions(evolutions_json):
    """Convertit les données JSON des évolutions en un format lisible."""
    try:
        evolutions = json.loads(evolutions_json)
        if not evolutions:
            return "Aucune"

        def format_evolution(evo):
            evol_str = evo["name"]
            if evo["evolves_to"]:
                evol_str += f" → {', '.join([format_evolution(sub) for sub in evo['evolves_to']])}"
            return evol_str

        return format_evolution(evolutions)
    except json.JSONDecodeError:
        return "Erreur"

def fetch_image(url):
    """Télécharge une image depuis une URL et la convertit pour Tkinter."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data).resize((96, 96))  # Redimensionner à 96x96 pixels
        return ImageTk.PhotoImage(pil_image)
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        return None

def display_pokemon_details(pokemon_name):
    """Affiche les détails d'un Pokémon dans une fenêtre Tkinter."""
    details = fetch_pokemon_details(pokemon_name)
    if not details:
        print(f"Aucun Pokémon trouvé avec le nom : {pokemon_name}")
        return

    numero, nom_eng, forme, evolutions, image_url = details
    evolutions_text = parse_evolutions(evolutions) if evolutions else "Aucune"

    root = tk.Tk()
    root.title(f"Détails de {pokemon_name}")

    # Télécharger et afficher l'image
    image = fetch_image(image_url)
    if image:
        image_label = tk.Label(root, image=image)
        image_label.image = image  # Nécessaire pour éviter que l'image soit supprimée
        image_label.pack(pady=10)

    # Labels pour afficher les informations
    tk.Label(root, text=f"Numéro : {numero}").pack(anchor="w", padx=10, pady=5)
    tk.Label(root, text=f"Nom : {nom_eng}").pack(anchor="w", padx=10, pady=5)
    tk.Label(root, text=f"Forme : {forme}").pack(anchor="w", padx=10, pady=5)
    tk.Label(root, text=f"Évolutions :").pack(anchor="w", padx=10, pady=5)
    tk.Message(root, text=evolutions_text, width=400).pack(anchor="w", padx=20, pady=5)

    root.mainloop()

if __name__ == "__main__":
    # Changez "Bulbasaur" par le nom du Pokémon que vous souhaitez afficher
    display_pokemon_details("Bulbasaur")
