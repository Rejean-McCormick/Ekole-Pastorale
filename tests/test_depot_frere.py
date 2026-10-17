"""Vérifications du dépôt frère et des dérivés sans dépendre d'Ekole Core."""
from __future__ import annotations
import json
from pathlib import Path
import sys, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'outils'))
import projeter_ekole as pe

class DepotFrereTests(unittest.TestCase):
    def test_manifest_root_and_courses(self):
        pack=json.loads((ROOT/'pack.json').read_text(encoding='utf-8'))
        self.assertEqual(pack['id'],'ecole-pastorale')
        self.assertEqual(pack['format'],'ekole.content-pack/0.1')
        self.assertEqual(len(pack['cours']),32)
        self.assertEqual(len(pack['parcours']),7)
        for x in pack['cours']:
            cid=x['id']
            self.assertEqual(json.loads((ROOT/x['fichier']).read_text(encoding='utf-8'))['id'],cid)
            student=json.loads((ROOT/'publications/eleve'/f'{cid}.json').read_text(encoding='utf-8'))
            self.assertEqual(student['id'],cid)
            self.assertFalse(student['publication_autorisee'])
    def test_pack_matches_sources(self):
        with tempfile.TemporaryDirectory() as d:
            fresh=pe.compile_pack(ROOT,Path(d),preflight=False)
            existing=json.loads((ROOT/'pack.json').read_text(encoding='utf-8'))
            self.assertEqual(fresh,existing)
            for x in fresh['cours']:
                for rel in [f"cours/{x['id']}.json",f"publications/eleve/{x['id']}.json"]:
                    self.assertEqual(json.loads((Path(d)/rel).read_text(encoding='utf-8')),json.loads((ROOT/rel).read_text(encoding='utf-8')))
            self.assertEqual(json.loads((Path(d)/'provenance-derivation.json').read_text(encoding='utf-8')),json.loads((ROOT/'provenance-derivation.json').read_text(encoding='utf-8')))

if __name__=='__main__':unittest.main()
