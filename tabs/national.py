from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QCheckBox, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QHeaderView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from database import load_pokedex

DEFAULT_IMAGE_PATH = os.path.join("assets", "default_image.png")

class NationalTab(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("Pokedex Tracker")
        self.setGeometry(100, 100, 1400, 600)

        # Configuration du tableau
        self.table = QTableWidget()
        self.table.setColumnCount(16)
        self.table.setHorizontalHeaderLabels(
            [
                "#", "Image", "Nom_FR", "Nom_ENG", "Forme", "Évolution", "Type 1", "Type 2",
                "HP", "Attaque", "Défense", "Attaque Spé.", "Défense Spé.", "Vitesse", "Shiny", "Capturé"
            ]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Cacher les numéros de ligne à gauche
        self.table.verticalHeader().setVisible(False)

        # Charger les données depuis la base de données
        self.load_data()

        # Ajouter le tableau à la disposition principale
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        """Charge les données depuis la base de données et les ajoute au tableau."""
        pokemons = load_pokedex()  # Charger toutes les colonnes nécessaires
        self.table.setRowCount(len(pokemons))

        for row, pokemon in enumerate(pokemons):
            (
                numero, nom_fr, nom_eng, forme, evolutions, type1_fr, type2_fr,
                hp, attaque, defense, attaque_special, defense_special, vitesse,
                shiny_flag, capture_flag, image_path
            ) = pokemon

            self.table.setRowHeight(row, 96)

            # Colonne numéro
            item = QTableWidgetItem(str(numero))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)

            # Colonne image
            if not os.path.exists(image_path):
                image_path = DEFAULT_IMAGE_PATH
            pixmap = QPixmap(image_path).scaled(96, 96, Qt.KeepAspectRatio)

            label = QLabel()
            label.setPixmap(pixmap)
            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.setAlignment(Qt.AlignCenter)
            container = QWidget()
            container.setLayout(layout)
            self.table.setCellWidget(row, 1, container)

            # Colonne noms
            self.table.setItem(row, 2, QTableWidgetItem(nom_fr))
            self.table.setItem(row, 3, QTableWidgetItem(nom_eng))

            # Colonne forme
            self.table.setItem(row, 4, QTableWidgetItem(forme))

            # Colonne évolution
            evolution_text = evolutions if evolutions != "Aucune évolution" else "Pas d'évolution"
            item = QTableWidgetItem(evolution_text)
            item.setToolTip(evolution_text)
            self.table.setItem(row, 5, item)

            # Colonne type 1 et type 2
            self.table.setItem(row, 6, QTableWidgetItem(type1_fr))
            self.table.setItem(row, 7, QTableWidgetItem(type2_fr or "-"))

            # Colonnes statistiques
            self.table.setItem(row, 8, QTableWidgetItem(str(hp)))
            self.table.setItem(row, 9, QTableWidgetItem(str(attaque)))
            self.table.setItem(row, 10, QTableWidgetItem(str(defense)))
            self.table.setItem(row, 11, QTableWidgetItem(str(attaque_special)))
            self.table.setItem(row, 12, QTableWidgetItem(str(defense_special)))
            self.table.setItem(row, 13, QTableWidgetItem(str(vitesse)))

            # Colonne shiny
            checkbox_shiny = QCheckBox()
            checkbox_shiny.setChecked(bool(shiny_flag))
            layout = QHBoxLayout()
            layout.addWidget(checkbox_shiny)
            layout.setAlignment(Qt.AlignCenter)
            container = QWidget()
            container.setLayout(layout)
            self.table.setCellWidget(row, 14, container)

            # Colonne capturé
            checkbox_captured = QCheckBox()
            checkbox_captured.setChecked(bool(capture_flag))
            layout = QHBoxLayout()
            layout.addWidget(checkbox_captured)
            layout.setAlignment(Qt.AlignCenter)
            container = QWidget()
            container.setLayout(layout)
            self.table.setCellWidget(row, 15, container)

if __name__ == "__main__":
    app = QApplication([])
    window = NationalTab()
    window.show()
    app.exec_()
