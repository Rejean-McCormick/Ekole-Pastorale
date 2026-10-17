# Démarrer Ekole Pastorale avec Ekole Core (v0.4 lancement)

## 1. Disposition des dépôts

```text
Ekole/
├── ekole/              # MOTEUR NEUTRE fourni séparément (snapshot du 17 octobre 2026)
├── ekole-quebec/       # optionnel
└── ecole-pastorale/    # CE dépôt: 32 cours et 7 parcours
```

**Important :** ne lancez pas `ekole/LANCER_EKOLE.bat` : il démarre volontairement le Core **sans contenu**.

## 2. Double-cliquer pour démarrer (Windows)

Dans `ecole-pastorale/`, double-cliquez sur **`LANCER_PASTORALE.bat`** (l'ancien `LANCER.bat` reste un alias).

- Le lanceur trouve `../ekole/launcher.py` automatiquement.
- Il fait vérifier les 32 cours et les 7 parcours par Ekole Core.
- Il démarre le portail sur **http://127.0.0.1:8775/** et l'éditeur enseignant privé sur le port **8776**.
- Les pages sont ouvertes automatiquement dans le navigateur.
- La fenêtre de terminal doit rester ouverte; **Ctrl+C** arrête les serveurs.

Si Python n'est pas trouvé, installer Python 3.10 ou plus récent. Aucune dépendance Python externe n'est requise par le Core.

## 3. macOS / Linux

Dans un terminal :

```bash
cd ecole-pastorale
./lancer-pastorale.sh
```

ou `python3 demarrer_pastorale.py`.

## 4. Vérifier sans démarrer

Windows : `LANCER_PASTORALE.bat --verifier`

macOS / Linux : `./lancer-pastorale.sh --verifier`

## 5. Options de lancement

| Option | Rôle |
| --- | --- |
| `--sans-navigateur` | Ne pas ouvrir les pages automatiquement |
| `--sans-editeur` | N'ouvrir que le portail public |
| `--edition` | Autoriser les modifications locales dans l'éditeur (lecture seule par défaut) |
| `--port 8875 --port-editeur 8876` | Changer les ports si ceux par défaut sont occupés |
| `--core CHEMIN` | Pointer vers un autre emplacement de `ekole/` |
| `--verifier` | Tester le chargement du contenu, puis quitter |

Vous pouvez aussi définir la variable d'environnement `EKOLE_CORE_PATH` vers le répertoire du moteur.

**Sans lanceur**, la commande équivalente est :

```bash
python3 ../ekole/launcher.py --contenu . --port 8775 --port-editeur 8776 --ouvrir
```

## 6. Ce qui reste inchangé

- `ekole` : moteur neutre, aucun fichier à copier dans son dépôt, aucune modification requise.
- `ecole-pastorale` : 32 cours et 7 parcours, sources Kristal v11 et projection Ekole.
- `ekole-quebec` : totalement indépendant et peut utiliser ses propres ports.
- L'éditeur reste en lecture seule par défaut. Les contenus pastoraux restent des maquettes à revoir avant publication.

### Dépannage

- **« Ekole Core introuvable »** : vérifier que les deux dossiers sont frères et orthographiés `ekole` et `ecole-pastorale`.
- **« Port indisponible »** : arrêter une autre instance, ou spécifier deux autres ports.
- **Un écran vide** : consulter la console pour le diagnostic et tester `--verifier`.
- **Le navigateur ne s'ouvre pas** : ouvrir manuellement http://127.0.0.1:8775/ ; le serveur doit continuer à tourner dans le terminal.
