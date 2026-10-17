#!/usr/bin/env python3
"""Installer atomique deux types candidats ARK-20 et ARK-21 dans Arketype 1.5.0.

Ne corrige PAS les anomalies préexistantes du dépôt hôte. Sans remplacement de fichiers existants.
"""
import argparse,copy,json,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
TYPES=('unite-formation-federee','temoin-vertus-sources')

def get(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def install(root,dry=False):
 root=Path(root).resolve();b=HERE/'overlay'
 required=[root/'catalogue.json',root/'inventaires/archetypes-visuels.json',root/'inventaires/diagrammes-situes.json']
 if not (root/'arketype.py').is_file() or not all(p.is_file() for p in required):raise ValueError('Dossier Arketype invalide')
 originals={p:p.read_bytes() for p in required}
 catalog=get(required[0]);v=get(required[1]);diagrams=get(required[2]);seenids={x['id'] for x in catalog['archetypes']};slugs={x['slug'] for x in catalog['archetypes']}
 if catalog.get('version')!='1.5.0':raise ValueError('Version Arketype attendue : 1.5.0')
 arches=[]
 for slug in TYPES:
  arche=get(b/'archetypes'/f'{slug}.json')
  if arche['id'] in seenids or slug in slugs:raise ValueError('Collision ID/slug : '+slug)
  if (root/'modeles'/slug).exists() or (root/'archetypes'/f'{slug}.json').exists():raise ValueError('Fichier déjà présent : '+slug)
  arches.append(arche);seenids.add(arche['id']);slugs.add(slug)
  catalog['archetypes'].append({'id':arche['id'],'slug':slug,'name':arche['name'],'family':arche['family'],'file':'archetypes/'+slug+'.json'})
  v['archetypes'].append({f:arche[f] for f in ('id','slug','name','family','visual_pattern','secondary_patterns','structure_label','situational_schema','canonical_use_cases')}|{'file':'archetypes/'+slug+'.json'})
  diagrams['diagrams'].append({'kind':'archetype','slug':slug,'pattern':arche['visual_pattern'],'status':'illustration_non_canonique','caption':arche['structure_label'],
    'nodes':[{'id':'a','label':'Kristal '+arche['id'],'x':80,'y':140},{'id':'s','label':'Sources typées','x':300,'y':80},{'id':'e','label':'Projection Ekole','x':520,'y':140}],
    'edges':[{'from':'a','to':'s'},{'from':'s','to':'e'}]})
 if dry:
  print('DRY-RUN : ARK-20 + ARK-21 peuvent être ajoutés à',root);return
 created=[]
 try:
  for arch in arches:
   slug=arch['slug'];model=root/'modeles'/slug;dst=root/'archetypes'/f'{slug}.json'
   shutil.copytree(b/'modeles'/slug,model);created.append(model)
   shutil.copy2(b/'archetypes'/f'{slug}.json',dst);created.append(dst)
  for path,obj in zip(required,(catalog,v,diagrams)):write(path,obj)
 except BaseException:
  for path,content in originals.items():path.write_bytes(content)
  for p in reversed(created):
   if p.is_dir():shutil.rmtree(p)
   elif p.exists():p.unlink()
  raise
 print('Ajoutés ARK-20 et ARK-21. Vérifier avec : python arketype.py validate --check-kit (la base hôte doit être saine).')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--arketype',required=True,type=Path);p.add_argument('--dry-run',action='store_true');a=p.parse_args()
 try:install(a.arketype,a.dry_run)
 except (ValueError,OSError,KeyError) as e:print('INSTALLATION REFUSÉE:',e,file=sys.stderr);sys.exit(2)
