#!/usr/bin/env python3
"""Audit en lecture seule d'un pont vers le Kristal Catho historique exact."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def audit(catho,bridge_path=ROOT/'federation/catho-legacy-bridge.json'):
 bridge=json.loads(Path(bridge_path).read_text(encoding='utf8'));catho=Path(catho).resolve()
 for name,a in bridge['artifacts'].items():
  p=(catho/a['relative_path']).resolve()
  if not p.is_relative_to(catho) or not p.is_file() or p.is_symlink():raise ValueError('Source historique manquante ou chemin interdit : '+name)
  if hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('Empreinte historique modifiée : '+name)
 people=json.loads((catho/bridge['artifacts']['people']['relative_path']).read_text())
 doctors={p['id'] for p in people['personnes'] if 'docteur_eglise' in p['categories']}
 if doctors!={x['id'] for x in bridge['doctors']}:raise ValueError('Index des docteurs divergent')
 corpus=json.loads((catho/bridge['artifacts']['corpus']['relative_path']).read_text())
 sources={s['source_id'] for s in corpus['source_refs']}
 if sources!={x['source_id'] for x in bridge['source_refs']}:raise ValueError('Index documentaire divergent')
 return {'status':'pinned_historical_artifacts_checked','doctors':len(doctors),'source_refs':len(sources),'limits':'Ce n’est ni une migration ni une équivalence sémantique v11.'}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--catho',required=True,type=Path);args=a.parse_args()
 try:print(json.dumps(audit(args.catho),ensure_ascii=False,indent=2))
 except (ValueError,KeyError,OSError) as e:print('AUDIT REFUSÉ:',e,file=sys.stderr);sys.exit(2)
