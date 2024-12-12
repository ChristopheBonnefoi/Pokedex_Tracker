from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QCheckBox, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from database import load_pokedex  # Charger les Pokémon depuis la base de données

DEFAULT_IMAGE_PATH = os.path.join("assets", "default_image.png")


class NationalTab(QWidget):  # Garder le nom original
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("Pokedex Tracker")
        self.setGeometry(100, 100, 1200, 600)

        # Configuration du tableau
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["#", "Image", "Nom_FR", "Nom_ENG", "Forme", "Évolution", "Jeux", "Shiny", "Capturé"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)

        # Cacher les numéros à gauche de la colonne `#`
        self.table.verticalHeader().setVisible(False)

        # Charger les données depuis la base de données
        self.load_data()

        # Ajouter le tableau à la disposition principale
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        """Charge les données depuis la base de données et les ajoute au tableau."""
        pokemons = load_pokedex()
        self.table.setRowCount(len(pokemons))

        for row, pokemon in enumerate(pokemons):
            numero, nom_fr, nom_eng, forme, evolution, jeux, shiny_flag, capture_flag, image_path = pokemon

            # Fixer la hauteur de la ligne
            self.table.setRowHeight(row, 96)

            # Colonne numéro (affichage centré)
            item = QTableWidgetItem(str(numero))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)

            # Colonne image
            if not os.path.exists(image_path):
                image_path = DEFAULT_IMAGE_PATH
            pixmap = QPixmap(image_path).scaled(96, 96, Qt.KeepAspectRatio)

            label = QLabel()
            label.setPixmap(pixmap)

            # Centrer l'image avec un layout
            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.setAlignment(Qt.AlignCenter)
            container = QWidget()
            container.setLayout(layout)

            self.table.setCellWidget(row, 1, container)

            # Colonne noms
            item = QTableWidgetItem(nom_fr)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item)

            item = QTableWidgetItem(nom_eng)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item)

            # Colonne forme
            item = QTableWidgetItem(forme)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, item)

            # Colonne évolution
            item = QTableWidgetItem(evolution)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, item)

            # Colonne jeux disponibles
            item = QTableWidgetItem(jeux)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 6, item)

            # Colonne shiny (case à cocher centrée)
            checkbox_shiny = QCheckBox()
            checkbox_shiny.setChecked(bool(shiny_flag))

            layout = QHBoxLayout()
            layout.addWidget(checkbox_shiny)
            layout.setAlignment(Qt.AlignCenter)
            container = QWidget()
            container.setLayout(layout)
            self.table.setCellWidget(row, 7, container)

            # Colonne capturé (case à cocher centrée)
            checkbox_captured = QCheckBox()
            checkbox_captured.setChecked(bool(capture_flag))

            layout = QHBoxLayout()
            layout.addWidget(checkbox_captured)
            layout.setAlignment(Qt.AlignCenter)
            container = QWidget()
            container.setLayout(layout)
            self.table.setCellWidget(row, 8, container)


if __name__ == "__main__":
    app = QApplication([])
    window = NationalTab()
    window.show()
    app.exec_()
