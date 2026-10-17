#!/usr/bin/env python3
"""Lance Ekole Core (neutre) avec le depot de contenu frere ecole-pastorale.
Aucune copie ou modification du moteur n'est effectuee.
"""
from __future__ import annotations

import argparse
import os
import signal
from pathlib import Path
import subprocess
import sys

PASTORALE = Path(__file__).resolve().parent


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Demarrer Ekole Core avec le contenu de l'ecole pastorale catholique"
    )
    p.add_argument('--verifier', action='store_true', help='Verifier le chargement sans demarrer')
    p.add_argument('--sans-navigateur', action='store_true', help='Ne pas ouvrir le navigateur')
    p.add_argument('--sans-editeur', action='store_true', help="Ne demarrer que le portail public")
    p.add_argument('--edition', action='store_true', help="Autoriser l'edition locale des cours")
    p.add_argument('--port', type=int, default=8775, help='Port public (defaut : 8775)')
    p.add_argument('--port-editeur', type=int, default=8776, help='Port enseignant (defaut : 8776)')
    p.add_argument('--core', type=Path, help='Chemin explicite vers ekole/ (sinon dossier frere)')
    args = p.parse_args(argv)

    core = (args.core or Path(os.environ.get('EKOLE_CORE_PATH', PASTORALE.parent / 'ekole'))).expanduser().resolve()
    launcher = core / 'launcher.py'
    if not launcher.is_file():
        print('[PASTORALE] ERREUR : moteur Ekole introuvable : ' + str(launcher), file=sys.stderr)
        print('[PASTORALE] Verifiez que ekole/ et ecole-pastorale/ sont cote a cote.', file=sys.stderr)
        print('[PASTORALE] Ou indiquez --core CHEMIN (ou EKOLE_CORE_PATH).', file=sys.stderr)
        return 2
    if not (PASTORALE/'pack.json').is_file():
        print('[PASTORALE] ERREUR : pack.json absent dans '+str(PASTORALE), file=sys.stderr)
        return 2
    if args.port not in range(1, 65536) or args.port_editeur not in range(1, 65536) or args.port == args.port_editeur:
        print('[PASTORALE] ERREUR : ports invalides ou identiques.', file=sys.stderr)
        return 2
    python = sys.executable
    cmd = [python, str(launcher), '--contenu', str(PASTORALE)]
    print('[PASTORALE] Moteur  :', core, flush=True)
    print('[PASTORALE] Contenu :', PASTORALE, flush=True)

    # Controle via le chargeur du vrai Core: pas de validation partielle inventee.
    preflight = subprocess.run([*cmd, '--verifier'], cwd=str(core), check=False)
    if preflight.returncode != 0 or args.verifier:
        return preflight.returncode

    cmd += ['--port', str(args.port), '--port-editeur', str(args.port_editeur)]
    if args.sans_editeur: cmd.append('--sans-editeur')
    if args.edition: cmd.append('--edition')
    if not args.sans_navigateur: cmd.append('--ouvrir')
    print('[PASTORALE] Accueil : http://127.0.0.1:%d/' % args.port, flush=True)
    if not args.sans_editeur:
        print('[PASTORALE] Espace enseignant : port %d, lien prive affiche par Ekole' % args.port_editeur, flush=True)
    print('[PASTORALE] Arret : Ctrl+C', flush=True)
    child = None
    def stop_on_termination(_signal, _frame):
        raise KeyboardInterrupt
    if os.name != 'nt':
        signal.signal(signal.SIGTERM, stop_on_termination)
    try:
        child = subprocess.Popen(cmd, cwd=str(core))
        return child.wait()
    except KeyboardInterrupt:
        print('\n[PASTORALE] Arret demande.', flush=True)
        if child is not None and child.poll() is None:
            # Le Ctrl+C du terminal est normalement egalement recu par Ekole;
            # le laisser fermer ses serveurs avant un arret force.
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.terminate()
                try:
                    child.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
        return 0
    except OSError as e:
        print('[PASTORALE] Demarrage impossible : '+str(e), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
