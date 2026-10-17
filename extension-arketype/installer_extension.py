#!/usr/bin/env python3
"""Ajouter ARK-20 à une copie locale d'Arketype 1.5; ne modifie jamais les 19 types existants."""
from __future__ import annotations
import argparse,copy,json,shutil,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
SLUG='unite-formation-federee'

def get(path):return json.loads(path.read_text(encoding='utf8'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def install(root:Path,dry:bool=False):
 root=root.resolve();lib=root/'catalogue.json';base=HERE/'overlay'
 if not lib.is_file() or not (root/'arketype.py').is_file():raise ValueError('Le chemin ne pointe pas vers Arketype')
 cat=get(lib)
 if cat.get('version')!='1.5.0':raise ValueError('Extension testée pour Arketype 1.5.0 seulement')
 arch=get(base/'archetypes'/f'{SLUG}.json')
 if any(x['slug']==SLUG or x['id']=='ARK-20' for x in cat['archetypes']):raise ValueError('ARK-20 déjà présent ou ID occupé')
 if (root/'modeles'/SLUG).exists() or (root/'archetypes'/f'{SLUG}.json').exists():raise ValueError('Collision avec un modèle ou archetype existant')
 srcdir=base/'modeles'/SLUG
 if not srcdir.is_dir():raise ValueError('Modèle manquant')
 indexpaths=[lib,root/'inventaires/archetypes-visuels.json',root/'inventaires/diagrammes-situes.json']
 cat['archetypes'].append({'id':'ARK-20','slug':SLUG,'name':arch['name'],'family':arch['family'],'file':'archetypes/'+SLUG+'.json'})
 visuals=get(indexpaths[1]); visuals['archetypes'].append({k:arch[k] for k in ['id','slug','name','family','visual_pattern','secondary_patterns','structure_label','situational_schema','canonical_use_cases'] }|{'file':'archetypes/'+SLUG+'.json'})
 diagrams=get(indexpaths[2]);diagrams['diagrams'].append({'kind':'archetype','slug':SLUG,'pattern':'branching','status':'illustration_non_canonique',
   'caption':'Learning unit keeps its lesson separate from sourced knowledge and derived Ekole presentation.',
   'nodes':[{'id':'u','label':'Learning unit','x':90,'y':123},{'id':'s','label':'Kristal sources','x':255,'y':55},{'id':'a','label':'Activities','x':255,'y':183},{'id':'e','label':'Ekole projection','x':515,'y':125}],
   'edges':[{'from':'u','to':'s'},{'from':'u','to':'a'},{'from':'s','to':'e'},{'from':'a','to':'e'}]})
 if dry:
  print('DRY-RUN: extension ARK-20 admissible dans',root,'(aucune modification)');return
 backups={p:p.read_bytes() for p in indexpaths};copied=[]
 try:
  shutil.copytree(srcdir,root/'modeles'/SLUG);copied.append(root/'modeles'/SLUG)
  shutil.copyfile(base/'archetypes'/f'{SLUG}.json',root/'archetypes'/f'{SLUG}.json');copied.append(root/'archetypes'/f'{SLUG}.json')
  for path,data in zip(indexpaths,[cat,visuals,diagrams]):write(path,data)
 except BaseException:
  for p,v in backups.items():p.write_bytes(v)
  for p in copied:
   if p.is_dir():shutil.rmtree(p)
   elif p.exists():p.unlink()
  raise
 print('ARK-20 installé dans',root,'; vérifier avec : python arketype.py validate --check-kit')
 print('Puis : python arketype.py create --type unite-formation-federee --slug essai --title "Essai" --parent CHEMIN --authoring v11')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--arketype',required=True,type=Path);parser.add_argument('--dry-run',action='store_true')
 args=parser.parse_args()
 try:install(args.arketype,args.dry_run)
 except (ValueError,OSError) as e:print('Installation refusée:',e,file=sys.stderr);sys.exit(2)
