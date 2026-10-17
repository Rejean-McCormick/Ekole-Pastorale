from __future__ import annotations
import importlib.util,json,sys,tempfile,unittest,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('projeteur',ROOT/'outils/projeter_ekole.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
spec2=importlib.util.spec_from_file_location('auditeur',ROOT/'outils/auditer_catho.py');a=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(a)

class TestsPastorale(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.locations=sorted(z for z in (ROOT/'kristals').iterdir() if (z/'kristal.workspace.json').is_file())
  cls.units=[p.load_unit(z,preflight=False) for z in cls.locations]
 def test_32_kristals_v11_and_graphs(self):
  self.assertEqual(len(self.locations),32)
  self.assertEqual(len([z for z in self.units if z['branch']=='message']),20)
  self.assertEqual(len([z for z in self.units if z['branch']=='miracles']),12)
  self.assertEqual(len(set(z['unit']['namespace_id'] for z in self.units)),32)
 def test_native_schema_draft_2020(self):
  try:import jsonschema
  except ImportError:self.skipTest('pip install jsonschema')
  schema=json.loads((ROOT/'contracts/pastorale.unite-native.schema.json').read_text())
  jsonschema.Draft202012Validator.check_schema(schema)
  for unit in self.units:
   with self.subTest(unit=unit['folder'].name):jsonschema.validate(unit['unit'],schema)
 def test_two_branches_are_independent_and_acyclic(self):
  p.assert_dag(self.units)
  by={z['unit']['curriculum_id']:z for z in self.units}
  for x in self.units:
   self.assertTrue(all(by[r]['branch']==x['branch'] for r in x['unit']['prerequis']))
 def test_enriched_assessment_and_safeguarding(self):
  for x in self.units:
   u=x['unit'];self.assertGreaterEqual(len(u['modules']),4)
   self.assertEqual(sum(k['poids'] for k in u['evaluation']['criteres']),100)
   self.assertFalse(u['publication_autorisee']);self.assertFalse(u['approbations']['autorite_ecclesiale'])
   self.assertTrue(u['sauvegarde']['aucune_adhesion_forcee'])
 def test_derived_pack_and_private_teacher_fields(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/'output';pack=p.compile_pack(ROOT,root,preflight=False)
   self.assertEqual(len(pack['cours']),32)
   self.assertEqual(len(pack['parcours']),7)
   for item in pack['cours']:
    cid=item['id'];teacher=json.loads((root/'cours'/f'{cid}.json').read_text());student=json.loads((root/'publications/eleve'/f'{cid}.json').read_text())
    self.assertIn('evaluation',teacher);self.assertNotIn('evaluation',student)
    self.assertEqual(len(teacher['guide_enseignant']['plan_de_seances']),4)
    self.assertEqual(sum(sec['minutes'] for sec in teacher['guide_enseignant']['plan_de_seances']),teacher['duree_minutes'])
    self.assertNotIn('guide_enseignant',student)
    self.assertNotIn('sauvegarde',student)
    self.assertFalse(student['publication_autorisee']);self.assertEqual(len(student['modules']),4)
   prov=json.loads((root/'provenance-derivation.json').read_text())
   self.assertFalse(prov['published']);self.assertFalse(prov['release_approved'])
 def test_edit_after_build_fails(self):
  with tempfile.TemporaryDirectory() as td:
   k=Path(td)/'source';shutil.copytree(ROOT/'kristals/lire-bible',k)
   file=k/'canon/domain/pedagogie/unite.json';x=json.loads(file.read_text());x['objectif']='ALTÉRÉ';file.write_text(json.dumps(x))
   with self.assertRaisesRegex(ValueError,'Canon modifié'):p.load_unit(k,preflight=False)
 def test_no_cross_branch_prerequisites(self):
  units=[dict(x) for x in self.units]
  m=next(x for x in units if x['branch']=='message')
  f=next(x for x in units if x['branch']=='miracles')
  m['unit']=dict(m['unit']);m['unit']['prerequis']=[f['unit']['curriculum_id']]
  with self.assertRaisesRegex(ValueError,'deux branches'):p.assert_dag(units)
 def test_catho_bridge_displays_only_historical_claims(self):
  b=json.loads((ROOT/'federation/catho-legacy-bridge.json').read_text())
  self.assertEqual(len(b['doctors']),38)
  self.assertEqual(len(b['source_refs']),138)
  self.assertEqual(b['status'],'pinned-historical-artifact-not-v11-crosswalk')
  self.assertTrue(all(len(x['sha256'])==64 for x in b['artifacts'].values()))
 def test_separate_witness_kristal_v11(self):
  k=ROOT/'kristals-temoins/francois-assise';u=json.loads((k/'canon/domain/temoignages/temoin.json').read_text())
  self.assertEqual(u['format'],'pastorale.temoin-native/0.1-draft')
  try:
   import jsonschema
   jsonschema.validate(u,json.loads((ROOT/'contracts/pastorale.temoin-native.schema.json').read_text()))
  except ImportError:pass
  self.assertFalse(u['publication_autorisee'])
  self.assertEqual(u['miracles_attribues']['statut'],'hors_champ_du_dossier_des_vertus')
  self.assertTrue((k/'build/v9/state-snapshot.json').exists())
 def test_arketype_two_types_and_templates(self):
  for slug in ['unite-formation-federee','temoin-vertus-sources']:
   root=ROOT/'extension-arketype/overlay'
   self.assertTrue((root/'modeles'/slug/'build/v9/state-snapshot.json').exists())
   self.assertTrue((root/'archetypes'/f'{slug}.json').exists())

if __name__=='__main__':unittest.main()
