"""Vérifie le corpus pastoral frère sans imposer sa taille historique."""
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from launcher import ENGINE, load_pack


class PastoralTests(unittest.TestCase):
    def test_pastorale_pack(self):
        root = ENGINE.parent / 'ecole-pastorale'
        pack = load_pack(root)  # Vérifie les identifiants, fichiers, prérequis et parcours.
        self.assertEqual(pack['id'], 'ecole-pastorale')
        # Les 12 cours / 3 parcours initiaux peuvent être enrichis (32 cours dans
        # le rapport Windows du 2026-10-24), mais ne doivent pas disparaître.
        self.assertGreaterEqual(len(pack['cours']), 12)
        self.assertGreaterEqual(len(pack['parcours']), 3)
        self.assertTrue(all(c['statut'] == 'brouillon_a_valider' for c in pack['cours']))
        for c in pack['cours']:
            with self.subTest(cours=c['id']):
                doc = json.loads((root / c['fichier']).read_text(encoding='utf-8'))
                self.assertEqual(doc['id'], c['id'])
                modules = doc.get('modules')
                self.assertIsInstance(modules, list)
                self.assertGreater(len(modules), 0)
                self.assertTrue(all(isinstance(mod, dict)
                                    and isinstance(mod.get('texte'), str)
                                    and mod['texte'].strip() for mod in modules))


if __name__ == '__main__':
    unittest.main()
