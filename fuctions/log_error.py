import os
from datetime import datetime

# Chemin du dossier des logs
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)  # Crée le dossier logs s'il n'existe pas déjà

def log_error(file_name, message):
    """
    Enregistre une erreur dans un fichier de log.

    Args:
        file_name (str): Nom de base du fichier log (ex. : "db_init_error").
        message (str): Message à enregistrer dans le fichier.
    """
    # Ajout de la date et de l'heure au nom du fichier
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(LOGS_DIR, f"{file_name}_{timestamp}.log")

    # Enregistrement du message d'erreur
    with open(log_file, "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    print(f"Erreur enregistrée dans : {log_file}")
