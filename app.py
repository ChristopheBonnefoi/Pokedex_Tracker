import tkinter as tk
from tkinter import ttk
from tabs.national import NationalTab

def create_app():
    root = tk.Tk()
    root.title("Pokédex Tracker")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Ajouter l'onglet Pokédex National
    national_tab = NationalTab(notebook)
    notebook.add(national_tab.frame, text="Pokédex National")

    root.mainloop()

if __name__ == "__main__":
    create_app()
