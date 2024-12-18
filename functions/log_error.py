import os
from datetime import datetime

# Chemin du dossier des logs
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)  # Crée le dossier logs s'il n'existe pas déjà

def log_error(file_name, message):
    """
    Enregistre une erreur dans un fichier de log unique par jour.

    Args:
        file_name (str): Nom du module (utilisé comme préfixe dans le log).
        message (str): Message à enregistrer dans le fichier.
    """
    # Nom du fichier : un fichier par jour
    log_file = os.path.join(LOGS_DIR, f"{file_name}_{datetime.now().strftime('%Y-%m-%d')}.log")

    # Écrit le message dans le fichier de log
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    print(f"Erreur enregistrée : {message}")
