from PyQt5.QtWidgets import QApplication
from tabs.national import NationalTab

def create_app():
    app = QApplication([])  # Crée une instance d'application PyQt
    window = NationalTab()  # Utilise la classe NationalTab
    window.show()           # Affiche la fenêtre principale
    app.exec_()             # Lance la boucle principale de l'application

if __name__ == "__main__":
    create_app()
