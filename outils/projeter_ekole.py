#!/usr/bin/env python3
"""Lecture contrôlée de Kristals Framework v11 pédagogiques -> contenu Ekole.

Produit exclusivement des projections dérivées; zéro mutation des sources, zéro mise en ligne.
Compatible avec Ekole core ekole.content-pack/0.1. Python 3.10+.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
SAFE=re.compile(r'[A-Za-z0-9_-]{1,80}\Z')

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def put(path, data):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def require(condition,description):
 if not condition:raise ValueError(description)
def within(base,path):
 p=(base/path).resolve()
 require(p.is_relative_to(base.resolve()) and not (base/path).is_symlink(),'Chemin hors Kristal ou lien symbolique interdit: '+str(path))
 return p

def verify_snapshot(folder,canonical):
 ws=read(folder/'kristal.workspace.json')
 state=read(folder/'build/v9/state-snapshot.json')
 require(state['state_ref']==ws['state_ref'] and state['logical_commitment'].get('digest'),'État v9 incohérent')
 index=read(folder/'canon/state.index.json')
 members={x['artifact_id']:x['logical_commitment'] for x in state['members']}
 logical={x['artifact_id']:x for x in (read(p) for p in (folder/'build/v9/artifacts').glob('*.logical-artifact.json'))}
 for entry in index['canonical_artifacts']:
  aid=entry['artifact_id'];p=within(folder,Path(entry['path']))
  require(aid in members and aid in logical,'Artifact v9 absent: '+aid)
  require(logical[aid]['logical_commitment']==members[aid],'Engagement par artifact incohérent: '+aid)
  require(logical[aid]['payload']==read(p),'Canon modifié depuis build v9: '+aid)
 require('canon/domain/pedagogie/unite.json' in [e['path'] for e in index['canonical_artifacts']], 'Unité non enregistrée dans le canon')
 return state,{e['path']:hashlib.sha256(within(folder,Path(e['path'])).read_bytes()).hexdigest() for e in index['canonical_artifacts']}

def load_unit(folder,preflight=True):
 require(not folder.is_symlink(),'Lien symbolique Kristal interdit')
 folder=folder.resolve()
 require(folder.is_dir() and not folder.is_symlink(),'Kristal absent ou chemin dangereux')
 if preflight:
  t=folder/'tools/kristal.py'
  require(t.is_file(),'Outil v11 local absent')
  for action in ('check-v11','check'):
   p=subprocess.run([sys.executable,str(t),action,str(folder)],capture_output=True,text=True)
   require(p.returncode==0,action+' échoué pour '+folder.name+': '+p.stderr[-300:]+p.stdout[-300:])
 profile=read(folder/'.kristal/v11/authoring.json')
 require(profile.get('semantic_profile')=='kristal.semantic-identity/11.0','Profil v11 non actif')
 for key in ('graph','registry','catalog','crosswalk'):
  require(within(folder,Path(profile[key])).is_file(),'Artefact v11 absent: '+key)
 graph=read(within(folder,Path(profile['graph'])));registry=read(within(folder,Path(profile['registry'])))
 u=read(folder/'canon/domain/pedagogie/unite.json')
 require(u['format']=='pastorale.unite-native/1.1-draft','Format natif 1.1 exigé')
 require(graph['namespace_id']==registry['namespace_id']==u['namespace_id'],'Namespace non aligné')
 require(u['unite_id'] in graph['entities'] and u['branche_id'] in graph['entities'],'KQ manquant')
 require(u['langue']=='fr-CA','Français canadien exigé pour cette projection')
 require(u.get('publication_autorisee') is False,'Refus de publication automatique (démonstration)')
 require(u['branche_code'] in ('message','miracles'),'Branche hors curriculum')
 require(u['epistemologie']['registre']==u['branche_code'],'Registre épistémologique incohérent')
 if u['branche_code']=='miracles':
  require('enseignement_catholique' in u['registres_documentaires'],'Registre doctrinal obligatoire pour miracles')
 require(u.get('approbations') and not all(u['approbations'].values()),'Démonstration ne peut se déclarer entièrement approuvée')
 require(all({'id','titre','texte'}<=set(x) and x['texte'].strip() for x in u['modules']),'Module incomplet')
 require(len(u['modules'])>=4,'Progression approfondie : quatre séances minimales')
 require(sum(x['poids'] for x in u['evaluation']['criteres'])==100,'Pondération évaluation ≠ 100')
 require(u['duree_minutes']>=120,'Durée anormalement courte')
 require(all(r['id'] in graph['sources'] for r in u['references']),'Sources locales K(S) introuvables')
 assert_branch=any(a['subject']==u['unite_id'] and a['predicate']==u['predicat_appartenance_branche'] and a['object']=={'kind':'entity','id':u['branche_id']} for a in graph['assertions'])
 require(assert_branch,'Lien de branche absent du graphe')
 loc=within(folder,Path(profile['catalog'])).parent/'curated-fr-CA.json'
 labels={x['semantic_id']:x['preferred_term'] for x in read(loc)['entries']}
 require(all(i in labels for i in (u['unite_id'],u['branche_id'])),'Lexique fr-CA incomplet')
 require(SAFE.fullmatch(u['curriculum_id']) is not None,'ID de cours invalide')
 state,sha=verify_snapshot(folder,u)
 return {'folder':folder,'unit':u,'title':labels[u['unite_id']],'branch_title':labels[u['branche_id']],'branch':u['branche_code'],'snapshot':state,'sha':sha}

def assert_dag(units):
 byid={x['unit']['curriculum_id']:x for x in units}
 require(len(byid)==len(units),'IDs de cours dupliqués')
 for cid,x in byid.items():
  for pre in x['unit']['prerequis']:
   require(pre in byid,'Prérequis absent: '+pre)
   require(byid[pre]['branch']==x['branch'],'Prérequis imposé entre deux branches: '+cid+' -> '+pre)
 seen=set();active=set()
 def visit(cid):
  require(cid not in active,'Cycle dans les préalables: '+cid)
  if cid in seen:return
  active.add(cid)
  for pre in byid[cid]['unit']['prerequis']:visit(pre)
  active.remove(cid);seen.add(cid)
 for cid in byid:visit(cid)

def build_paths(units):
 by={x['unit']['curriculum_id']:x for x in units}
 def ids(*slugs):
  slugmap={x['folder'].name:x['unit']['curriculum_id'] for x in units}
  return [slugmap[s] for s in slugs if s in slugmap]
 message=sorted((x for x in units if x['branch']=='message'),key=lambda x:x['unit']['curriculum_id'])
 miracles=sorted((x for x in units if x['branch']=='miracles'),key=lambda x:x['unit']['curriculum_id'])
 base=[
  ('EPC-MESSAGE','Branche I — Message, docteurs et saints',[x['unit']['curriculum_id'] for x in message],'Le message chrétien, la tradition des docteurs, les saints et les responsabilités sociales.'),
  ('EPC-MIRACLES','Branche II — Miracles et mystères',[x['unit']['curriculum_id'] for x in miracles],'Récits, signes, dogmes, méthodes historiques et dialogue sur la foi.'),
  ('EPC-DOCTEURS','Voie des docteurs et du discernement',ids('augustin','thomas-charite','therese-lisieux','catherine-sienne','francois-sales'),'Une tradition de pensée et de vie, à partir d’auteurs identifiés.'),
  ('EPC-SAINTS','Voie des saints : les vertus en actes',ids('francois-assise','vincent-de-paul','marie-incarnation','therese-lisieux'),'Témoignages documentés, vertus, difficultés et contexte historique.'),
  ('EPC-SOCIAL','Voie sociale et intervention',ids('amour-prochain','partage-pauvres','richesse-conversion','doctrine-sociale','accompagnement','projet-terrain'),'Solidarité, justice, pauvreté et gouvernance de l’aide.'),
  ('EPC-FOI-APPRO','Approfondir la foi sans esquiver les questions',ids('resurrection','miracle-science','revelations-privees','miracles-saints','sacrements-mystere'),'Lecture catholique et examen respectueux des différents degrés de certitude.'),
  ('EPC-DECOUVERTE','Découverte libre, deux portes distinctes',ids('lire-bible','pardon','amour-prochain','cana','marche-eau'),'Orientation facultative entre deux branches; les miracles ne sont pas des préalables au message.'),
 ]
 paths=[{'id':ident,'titre':title,'description':desc,'cours_ids':course_ids} for ident,title,course_ids,desc in base]
 require(all(p['cours_ids'] and set(p['cours_ids'])<=set(by) for p in paths),'Parcours incomplet')
 return paths

def compile_pack(root,output,preflight=True):
 root=root.resolve();output=output.resolve()
 require(root==output or not root.is_relative_to(output),'Chemin de sortie interdit')
 require(not output.is_relative_to(root/'kristals'),'Ne jamais écrire dans le canon')
 folders=sorted(p for p in (root/'kristals').iterdir() if (p/'kristal.workspace.json').is_file())
 require(bool(folders),'Aucun Kristal d’unité trouvé')
 units=[load_unit(p,preflight) for p in folders]
 assert_dag(units)
 index=read(root/'curriculum/cours-index.json')
 expected={x['id'] for x in index['cours']}
 require(len(expected)==len(index['cours']) and expected=={x['unit']['curriculum_id'] for x in units},'Index curriculum incomplet ou divergent')
 paths=build_paths(units)
 items=[];prov=[]
 for x in units:
  u=x['unit'];cid=u['curriculum_id']
  require(SAFE.fullmatch(cid) is not None,'ID dangereux')
  items.append({'id':cid,'titre':x['title'],'discipline':x['branch_title'],'objectif':u['objectif'],'preuve':u['preuve'], 'statut':'maquette_non_approuvee','fichier':f'cours/{cid}.json','prerequis':u['prerequis']})
  common={'id':cid,'titre':x['title'],'modules':u['modules'],'niveau':u['niveau'],'duree_minutes':u['duree_minutes']}
  teacher={'format':'ekole.cours/0.1',**common,'statut':'proposition_non_validee','publication_eleve':False,'note':'NON PUBLIÉ — Contenus à relire et approuver.',
           'domaine':x['branch_title'],'objectif':u['objectif'],'preuve':u['preuve'],'prerequis':u['prerequis'],
           'competences':u['competences'],'questions_difficiles':u['questions_difficiles'],'activites':u['activites'],
           'evaluation':u['evaluation'],'guide_enseignant':u['guide_enseignant'],'sauvegarde':u['sauvegarde'],'bibliographie_cible':u['bibliographie_cible'],
           'validation':u['validation'],'approbations':u['approbations'],'references':u['references'],
           'provenance_kristal':{'namespace_id':u['namespace_id'],'logical_state_commitment':x['snapshot']['logical_commitment']['digest'],'state_ref':x['snapshot']['state_ref']}}
  put(output/'cours'/f'{cid}.json',teacher)
  student={'format':'ekole.cours/0.1',**common,'statut_publication':'MAQUETTE_LOCALE_NON_APPROUVEE',
           'avertissement':'Étude locale en préparation, non approuvée pour diffusion publique.',
           'questions_de_reflexion':u['questions_difficiles'],'publication_autorisee':False}
  put(output/'publications/eleve'/f'{cid}.json',student)
  prov.append({'course_id':cid,'source_kristal':x['folder'].name,'state_ref':x['snapshot']['state_ref'],
    'logical_state_commitment':x['snapshot']['logical_commitment']['digest'],'canonical_sha256':x['sha'],
    'native_contract':'pastorale.unite-native/1.1-draft','approval_required':True})
 pack={'format':'ekole.content-pack/0.1','id':'ecole-pastorale','nom':'École catholique pastorale — deux branches et témoins',
  'langue':'fr-CA','statut':'projet_non_publie','description':'Deux branches distinctes; docteurs, saints et action pastorale; curriculum v11 dérivé.',
  'politique_publication':'vues_separees','cours':sorted(items,key=lambda z:z['id']),'parcours':paths,
  'parcours_mis_en_avant':'EPC-MESSAGE','cours_a_decouvrir':['EPC-MSG-001','EPC-FOI-001']}
 put(output/'pack.json',pack)
 bridge=read(root/'federation/catho-legacy-bridge.json')
 put(output/'provenance-derivation.json',{'format':'pastorale.ekole-derivation/1.1','published':False,'release_approved':False,'source_kristals':prov,'catho_legacy_pins':bridge['artifacts'],
   'mise_en_garde':'Pont v8 documenté, pas de résolution sémantique v11. Aucune approbation ecclésiale; ne pas publier automatiquement.'})
 return pack

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--racine',type=Path,default=ROOT)
 p.add_argument('--sortie',type=Path,default=ROOT)
 p.add_argument('--sans-preflight',action='store_true',help='Pour tests rapides uniquement; ne dispense pas des engagements v9')
 a=p.parse_args()
 try:
  pack=compile_pack(a.racine,a.sortie,not a.sans_preflight)
  print('Export contrôlé :',len(pack['cours']),'cours,',len(pack['parcours']),'parcours — statut NON PUBLIÉ')
 except (OSError,ValueError,KeyError,subprocess.SubprocessError) as e:
  print('PROJECTION REFUSÉE:',str(e),file=sys.stderr);sys.exit(2)
