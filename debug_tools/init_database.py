import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db


# Exécuter la fonction init_db pour créer les tables
init_db()
print("Table `pokemon` créée avec succès.")
