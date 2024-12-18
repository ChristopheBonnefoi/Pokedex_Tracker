import unittest
import sys
import os

# Ajoute le chemin racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from data.data_functions.fetch_types import translate_type_to_french


class TestTypeTranslations(unittest.TestCase):
    def test_known_types(self):
        """Teste les traductions pour des types connus."""
        self.assertEqual(translate_type_to_french("Grass"), "Plante")
        self.assertEqual(translate_type_to_french("Fire"), "Feu")
        self.assertEqual(translate_type_to_french("Water"), "Eau")

    def test_unknown_type(self):
        """Teste les cas où le type est inconnu."""
        self.assertEqual(translate_type_to_french("Unknown"), "Inconnu")
        self.assertEqual(translate_type_to_french("NonExistent"), "Inconnu")

    def test_empty_and_none(self):
        """Teste les cas où le type est None ou une chaîne vide."""
        self.assertEqual(translate_type_to_french(None), "Inconnu")
        self.assertEqual(translate_type_to_french(""), "Inconnu")


if __name__ == "__main__":
    unittest.main()
